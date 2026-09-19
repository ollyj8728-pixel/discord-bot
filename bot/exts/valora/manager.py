"""Valora Discord manager setup and permission scanning."""
import discord
from discord.ext import commands
from bot.bot import Bot

MANAGER_ROLES = ("Manager", "Senior Moderator", "Moderator", "Ticket Staff")
MANAGER_CHANNELS = ("tickets", "transcripts", "audit-log", "reports", "appeals")

def setup_allowed(member: discord.Member) -> bool:
    return member.id == member.guild.owner_id or member.guild_permissions.administrator

def permission_label(member: discord.Member) -> str:
    if member.guild_permissions.administrator:
        return "Administrator"
    if member.guild_permissions.manage_guild:
        return "Manage Server"
    if member.guild_permissions.manage_channels:
        return "Manage Channels"
    return "No manager permission"

class Manager(commands.Cog, name="Valora Manager"):
    """Owner/admin setup and read-only Discord permission inspection."""
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def require_setup(self, ctx: commands.Context) -> bool:
        if isinstance(ctx.author, discord.Member) and setup_allowed(ctx.author):
            return True
        await ctx.send("🔒 Setup is restricted to the server owner or a Discord Administrator.")
        return False

    @commands.hybrid_group(name="manager", invoke_without_command=True)
    async def manager(self, ctx: commands.Context) -> None:
        await ctx.send_help(ctx.command)

    @manager.command(name="setup-preview")
    async def setup_preview(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title="🛡️ Valora Manager Setup Preview", colour=discord.Colour.orange())
        embed.add_field(name="Roles", value="\n".join("• " + x for x in MANAGER_ROLES))
        embed.add_field(name="Channels", value="\n".join("• #" + x for x in MANAGER_CHANNELS))
        embed.set_footer(text="Preview only — no Discord changes were made.")
        await ctx.send(embed=embed)

    @manager.command(name="setup-check")
    async def setup_check(self, ctx: commands.Context) -> None:
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return
        roles = [r for r in ctx.guild.roles if r.name in MANAGER_ROLES]
        channels = [c for c in ctx.guild.channels if c.name in MANAGER_CHANNELS]
        staff = []
        for member in ctx.guild.members:
            matching = [r.name for r in member.roles if r.name in MANAGER_ROLES]
            if matching:
                staff.append(f"{member} — {', '.join(matching)} — {permission_label(member)}")
        embed = discord.Embed(title="🔎 Discord Permission Scan", colour=discord.Colour.blurple())
        embed.description = f"Scanned {len(ctx.guild.members)} cached members in **{ctx.guild.name}**."
        embed.add_field(name="Roles found", value="\n".join("✅ " + r.name for r in roles) or "None found")
        embed.add_field(name="Channels found", value="\n".join("✅ #" + c.name for c in channels) or "None found")
        embed.add_field(name="Staff-linked members", value="\n".join(staff)[:1024] or "None found", inline=False)
        embed.set_footer(text="Reads Discord permissions; never bypasses role hierarchy.")
        await ctx.send(embed=embed)

    @manager.command(name="setup-status")
    async def setup_status(self, ctx: commands.Context) -> None:
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return
        roles = {r.name for r in ctx.guild.roles}
        channels = {c.name for c in ctx.guild.channels}
        missing_roles = [x for x in MANAGER_ROLES if x not in roles]
        missing_channels = [x for x in MANAGER_CHANNELS if x not in channels]
        await ctx.send(f"🛡️ **Valora setup**\nRoles ready: {len(MANAGER_ROLES) - len(missing_roles)}/{len(MANAGER_ROLES)}\nChannels ready: {len(MANAGER_CHANNELS) - len(missing_channels)}/{len(MANAGER_CHANNELS)}\nMissing roles: {', '.join(missing_roles) or 'none'}\nMissing channels: {', '.join('#' + x for x in missing_channels) or 'none'}")

    @manager.command(name="setup")
    async def setup(self, ctx: commands.Context) -> None:
        if ctx.guild is None or not await self.require_setup(ctx):
            return
        created = []
        for name in MANAGER_ROLES:
            if discord.utils.get(ctx.guild.roles, name=name) is None:
                await ctx.guild.create_role(name=name, colour=discord.Colour.orange(), reason="Valora manager setup")
                created.append("role:" + name)
        for name in MANAGER_CHANNELS:
            if discord.utils.get(ctx.guild.text_channels, name=name) is None:
                overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
                await ctx.guild.create_text_channel(name, overwrites=overwrites, reason="Valora manager setup")
                created.append("channel:#" + name)
        await ctx.send("✅ **Valora manager system ready**\n" + ("\n".join("• " + x for x in created) if created else "No changes were needed."))

async def setup(bot: Bot) -> None:
    await bot.add_cog(Manager(bot))
