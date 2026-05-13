"""
Prodigy Companion CLI
"""

import asyncio
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import click
from src.api.client import ProdigyCompanion
from src.utils import config as cfg
from src.utils.formatter import (
    print_banner, print_profile, print_weekly_summary,
    print_skills_table, print_sessions, print_assignments,
    print_screen_time,
)


def _client() -> ProdigyCompanion:
    return ProdigyCompanion(session_token=cfg.get_token())


def _resolve_user(user: str = None) -> str:
    return user or cfg.get_default_user() or ""


@click.group()
def cli():
    """Prodigy Companion - track your child's math learning progress"""
    pass


# ── Setup commands ────────────────────────────────────────────────────────────

@cli.command()
@click.option("--token", "-t", required=True, help="Session token from prodigygame.com")
def login(token):
    """Save your Prodigy session token (one-time setup)"""
    cfg.set_token(token)
    click.echo()
    click.echo("  Token saved to ~/.prodigy-companion/config.json")
    click.echo("  This token is used only for read-only API requests to prodigygame.com.")
    click.echo("  Run 'prodigy logout' to remove it.")
    click.echo()


@cli.command()
def logout():
    """Remove your saved session token"""
    c = cfg.load_config()
    c.pop("token", None)
    cfg.save_config(c)
    click.echo("\n  Token removed.\n")


@cli.command()
@click.argument("user_id")
def use(user_id):
    """Set the default child's user ID (so you don't have to pass it every time)"""
    cfg.set_default_user(user_id)
    click.echo(f"\n  Default user set to: {user_id}\n")


@cli.command("set-limit")
@click.argument("minutes", type=int)
def set_limit(minutes):
    """Set the daily screen-time limit in minutes"""
    cfg.set_screen_time_limit(minutes)
    click.echo(f"\n  Daily screen-time limit set to {minutes} minutes.\n")


# ── Reporting commands ────────────────────────────────────────────────────────

@cli.command()
@click.option("--user", "-u", default=None)
def profile(user):
    """Show your child's profile (name, grade, title)"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            data = await c.get_profile(uid)
            print_profile(data)
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command()
@click.option("--user", "-u", default=None)
def week(user):
    """Weekly learning report - the main view for parents"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            click.echo(f"  Building weekly report for {uid[:10]}...\n")
            summary = await c.summarize_week(uid)
            print_weekly_summary(summary)
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command()
@click.option("--user", "-u", default=None)
@click.option("--filter", "-f", "filter_mode", default="all",
              type=click.Choice(["all", "weak", "strong"]),
              help="Show only weak, strong, or all skills")
def skills(user, filter_mode):
    """List math skills with mastery scores"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            click.echo(f"  Loading skill mastery for {uid[:10]}...\n")
            data = await c.get_skill_mastery(uid)
            print_skills_table(data, filter_mode=filter_mode)
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command()
@click.option("--user", "-u", default=None)
@click.option("--days", "-d", default=7)
def sessions(user, days):
    """Show recent play sessions"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            click.echo(f"  Loading last {days} days of sessions...\n")
            data = await c.get_session_history(uid, days=days)
            print_sessions(data)
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command()
@click.option("--user", "-u", default=None)
def assignments(user):
    """Show teacher-assigned practice goals"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            data = await c.get_assignments(uid)
            print_assignments(data)
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command("screen-time")
@click.option("--user", "-u", default=None)
def screen_time(user):
    """Check today's play time against your daily limit"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            minutes = await c.screen_time_today(uid)
            print_screen_time(minutes, limit_minutes=cfg.get_screen_time_limit())
        finally:
            await c.close()

    asyncio.run(_run())


@cli.command()
@click.option("--user", "-u", default=None)
@click.option("--output", "-o", default="report.html", help="Output file path")
def export(user, output):
    """Export the weekly report as a shareable HTML file"""
    print_banner()
    uid = _resolve_user(user)
    if not uid:
        click.echo("  No user set. Run: prodigy use <user_id>")
        return

    async def _run():
        c = _client()
        try:
            from src.reports.html_report import build_html_report
            summary = await c.summarize_week(uid)
            html = build_html_report(summary)
            with open(output, "w", encoding="utf-8") as f:
                f.write(html)
            click.echo(f"\n  Report saved to: {output}\n")
        finally:
            await c.close()

    asyncio.run(_run())


if __name__ == "__main__":
    cli()
