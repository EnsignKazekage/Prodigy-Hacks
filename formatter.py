"""
Terminal formatting - clean, parent-friendly reports.
"""

import click
from typing import List, Dict


RESET = "\033[0m"; BOLD = "\033[1m"
GREEN = "\033[92m"; RED = "\033[91m"; YELLOW = "\033[93m"
CYAN  = "\033[96m"; BLUE = "\033[94m"; MAGENTA = "\033[95m"
WHITE = "\033[97m"; GRAY = "\033[90m"


def _c(text, color):
    return f"{color}{text}{RESET}"


def _mastery_color(m: float) -> str:
    if m >= 80: return GREEN
    if m >= 50: return YELLOW
    return RED


def _bar(value: float, max_value: float = 100, width: int = 20) -> str:
    filled = int((value / max_value) * width) if max_value else 0
    return "█" * filled + "░" * (width - filled)


def print_banner():
    click.echo(f"""
{CYAN}{BOLD}
  ██████╗ ██████╗  ██████╗ ██████╗ ██╗ ██████╗██╗   ██╗
  ██╔══██╗██╔══██╗██╔═══██╗██╔══██╗██║██╔════╝╚██╗ ██╔╝
  ██████╔╝██████╔╝██║   ██║██║  ██║██║██║  ███╗╚████╔╝
  ██╔═══╝ ██╔══██╗██║   ██║██║  ██║██║██║   ██║ ╚██╔╝
  ██║     ██║  ██║╚██████╔╝██████╔╝██║╚██████╔╝  ██║
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝   ╚═╝
   ██████╗ ██████╗ ███╗   ███╗██████╗  █████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗
  ██╔════╝██╔═══██╗████╗ ████║██╔══██╗██╔══██╗████╗  ██║██║██╔═══██╗████╗  ██║
  ██║     ██║   ██║██╔████╔██║██████╔╝███████║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
  ██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██╔══██║██║╚██╗██║██║██║   ██║██║╚██╗██║
  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ██║  ██║██║ ╚████║██║╚██████╔╝██║ ╚████║
   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
{RESET}{GRAY}  A parent's companion for the Prodigy Math Game
  github.com/EnsignKazekage/Prodigy-Hacks{RESET}
""")


def print_profile(profile: Dict):
    name  = profile.get("name") or profile.get("displayName") or "Student"
    grade = profile.get("grade") or "—"
    title = profile.get("title") or ""
    click.echo()
    click.echo(f"  {_c('Student:', GRAY)} {_c(BOLD + name, CYAN)}")
    click.echo(f"  {_c('Grade:',   GRAY)} {_c(str(grade), WHITE)}")
    if title:
        click.echo(f"  {_c('Title:',   GRAY)} {_c(title, WHITE)}")
    click.echo()


def print_weekly_summary(summary: Dict):
    click.echo(_c(f"\n  Week of {summary['weekStarting']}\n", BOLD + CYAN))
    click.echo(_c("  Activity", BOLD + WHITE))
    click.echo(_c("  " + "─" * 50, GRAY))

    mins  = summary["totalMinutes"]
    hours = mins // 60
    rest  = mins % 60
    click.echo(f"  {_c('Play time:',       GRAY):<22}  {_c(f'{hours}h {rest}m', WHITE)}")
    click.echo(f"  {_c('Sessions:',        GRAY):<22}  {_c(str(summary['sessionCount']), WHITE)}")
    click.echo(f"  {_c('Questions:',       GRAY):<22}  {_c(str(summary['totalQuestions']), WHITE)}")
    click.echo(f"  {_c('Correct answers:', GRAY):<22}  {_c(str(summary['correctAnswers']), GREEN)}")
    acc = summary["accuracyPercent"]
    acolor = _mastery_color(acc)
    click.echo(f"  {_c('Accuracy:',        GRAY):<22}  {_c(f'{acc}%', acolor + BOLD)}  {_c(_bar(acc), acolor)}")
    click.echo()

    strong = summary.get("strongSkills", [])
    weak   = summary.get("weakSkills", [])

    if strong:
        click.echo(_c("  Mastered skills", BOLD + GREEN))
        click.echo(_c("  " + "─" * 50, GRAY))
        for s in strong:
            m = s.get("mastery", 0)
            click.echo(f"  {s.get('name', '—')[:34]:<34}  {_c(_bar(m), GREEN)}  {_c(f'{m}%', GREEN + BOLD)}")
        click.echo()

    if weak:
        click.echo(_c("  Needs practice", BOLD + YELLOW))
        click.echo(_c("  " + "─" * 50, GRAY))
        for s in weak:
            m = s.get("mastery", 0)
            click.echo(f"  {s.get('name', '—')[:34]:<34}  {_c(_bar(m), _mastery_color(m))}  {_c(f'{m}%', _mastery_color(m) + BOLD)}")
        click.echo()

    click.echo(_c("  " + "─" * 50, GRAY))
    if acc >= 80 and mins >= 60:
        msg = "Great week of learning! Strong accuracy and consistent practice."
        click.echo(f"  {_c(msg, GREEN)}\n")
    elif weak:
        msg = "Consider focusing the next sessions on the practice areas above."
        click.echo(f"  {_c(msg, YELLOW)}\n")
    else:
        msg = "Keep going. Steady practice builds long-term mastery."
        click.echo(f"  {_c(msg, CYAN)}\n")


def print_skills_table(skills: List[Dict], filter_mode: str = "all"):
    if not skills:
        click.echo(_c("  No skills data found.", YELLOW))
        return

    if filter_mode == "weak":
        skills = [s for s in skills if s.get("mastery", 0) < 50]
    elif filter_mode == "strong":
        skills = [s for s in skills if s.get("mastery", 0) >= 80]

    skills.sort(key=lambda s: s.get("mastery", 0), reverse=True)

    click.echo(_c(f"\n  {'SKILL':<40}  {'MASTERY':>8}  {'PROGRESS':<22}", BOLD + CYAN))
    click.echo(_c("  " + "─" * 76, GRAY))

    for s in skills:
        name = (s.get("name") or "—")[:38]
        m    = s.get("mastery", 0)
        c    = _mastery_color(m)
        click.echo(f"  {name:<40}  {_c(f'{m}%', c + BOLD):>8}  {_c(_bar(m), c)}")

    click.echo()
    click.echo(f"  {len(skills)} skills displayed\n")


def print_sessions(sessions: List[Dict]):
    if not sessions:
        click.echo(_c("  No sessions in this period.", YELLOW))
        return

    click.echo(_c(f"\n  {'DATE':<12}  {'DURATION':>10}  {'QUESTIONS':>10}  {'ACCURACY':>10}", BOLD + CYAN))
    click.echo(_c("  " + "─" * 50, GRAY))

    for s in sessions:
        from datetime import datetime as dt
        started = s.get("startedAt", "")
        try:
            date_str = dt.fromisoformat(started.replace("Z", "")).strftime("%Y-%m-%d")
        except Exception:
            date_str = started[:10]

        mins = s.get("durationMinutes", 0)
        qs   = s.get("questionsAnswered", 0)
        corr = s.get("questionsCorrect", 0)
        acc  = (corr / qs * 100) if qs else 0
        c    = _mastery_color(acc)

        click.echo(
            f"  {date_str:<12}  "
            f"{_c(f'{mins} min', WHITE):>10}  "
            f"{_c(str(qs), WHITE):>10}  "
            f"{_c(f'{acc:.0f}%', c + BOLD):>10}"
        )
    click.echo()


def print_assignments(assignments: List[Dict]):
    if not assignments:
        click.echo(_c("  No active assignments from teachers.", GRAY))
        return

    click.echo(_c(f"\n  Active teacher assignments ({len(assignments)})\n", BOLD + CYAN))

    for a in assignments:
        title  = a.get("title") or a.get("skillName") or "—"
        due    = str(a.get("dueDate", "—"))[:10]
        prog   = a.get("progressPercent") or 0
        status = a.get("status") or "in progress"

        status_color = GREEN if status == "completed" else (YELLOW if prog > 0 else GRAY)
        click.echo(f"  {_c('•', CYAN)} {_c(title, WHITE)}")
        click.echo(f"      Due: {due}  |  Progress: {_c(f'{prog}%', status_color)}  |  {_c(status, status_color)}")
        click.echo()


def print_screen_time(minutes: int, limit_minutes: int = 60):
    over = minutes > limit_minutes
    color = RED if over else (YELLOW if minutes >= limit_minutes * 0.75 else GREEN)

    click.echo()
    label = "Today's play time:"
    click.echo(f"  {_c(label, GRAY)}  {_c(f'{minutes} min', color + BOLD)}")
    click.echo(f"  {_c('Daily limit:', GRAY):<22}  {_c(f'{limit_minutes} min', WHITE)}")
    click.echo(f"  {_c(_bar(minutes, limit_minutes, 30), color)}")
    if over:
        click.echo(f"\n  {_c('Over the daily limit by ' + str(minutes - limit_minutes) + ' minutes.', RED)}")
    elif minutes >= limit_minutes * 0.75:
        click.echo(f"\n  {_c('Approaching the daily limit.', YELLOW)}")
    else:
        click.echo(f"\n  {_c('Within the daily limit.', GREEN)}")
    click.echo()
