# Python Utility Bot

[![Discord][1]][2]
[![CI][3]][4]
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

This project is a Discord bot specifically for use with the Python Discord server. It provides numerous utilities and other tools to help keep the server running like a well-oiled machine.

## Valora Discord Manager

This fork includes a Discord-only Valora Manager extension at `bot/exts/valora/manager.py`.

Commands:

- `!manager setup-preview` — preview roles and channels without changes.
- `!manager setup-check` — scan real Discord roles, channels, staff, and permissions.
- `!manager setup-status` — show missing roles and channels.
- `!manager setup` — create missing manager roles and private management channels.

Roles: **Manager**, **Senior Moderator**, **Moderator**, **Ticket Staff**.
Channels: **#tickets**, **#transcripts**, **#audit-log**, **#reports**, **#appeals**.

Setup is restricted to the server owner or a Discord Administrator. The extension reads Discord state and never connects to Rust servers, RCON, game state, or secret credentials. It does not bypass Discord’s role hierarchy.

Read the [Contributing Guide](https://pythondiscord.com/pages/contributing/bot/) on our website if you are interested in helping out.

[1]: https://raw.githubusercontent.com/python-discord/branding/main/logos/badge/badge_github.svg
[2]: https://discord.gg/python
[3]: https://github.com/python-discord/bot/actions/workflows/main.yml/badge.svg?branch=main
[4]: https://github.com/python-discord/bot/actions/workflows/main.yml?query=branch%3Amain
