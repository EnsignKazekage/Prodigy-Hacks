"""
Prodigy Math Game - Companion API Client
Read-only client for the public Prodigy game API.

Designed for parents and educators to track their child's learning progress.
No account modification, no game state changes - read-only by design.
"""

import httpx
import asyncio
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta


PRODIGY_API     = "https://api.prodigygame.com"
PRODIGY_GAME    = "https://game.prodigygame.com"


class ProdigyCompanion:
    """
    Read-only client wrapping public Prodigy endpoints.

    The child or parent supplies their own session token (obtained by logging
    in normally at prodigygame.com). This client never asks for passwords and
    never performs write operations.
    """

    def __init__(self, session_token: Optional[str] = None, timeout: int = 15):
        headers = {
            "User-Agent": "ProdigyCompanion/1.0 (parental progress tracker)",
            "Accept": "application/json",
        }
        if session_token:
            headers["Authorization"] = f"Bearer {session_token}"
        self._http = httpx.AsyncClient(timeout=timeout, headers=headers)
        self._token = session_token

    async def close(self):
        await self._http.aclose()

    # ── Profile & progress ───────────────────────────────────────────────────

    async def get_profile(self, user_id: str) -> Dict:
        """Get public profile info: name, grade, current goals."""
        r = await self._http.get(f"{PRODIGY_API}/v3/characters/{user_id}")
        r.raise_for_status()
        return r.json()

    async def get_curriculum_progress(self, user_id: str) -> Dict:
        """
        Mathematics curriculum coverage:
        which skills/standards has the child practiced and how well.
        """
        r = await self._http.get(f"{PRODIGY_API}/v3/students/{user_id}/curriculum")
        r.raise_for_status()
        return r.json()

    async def get_session_history(
        self, user_id: str, days: int = 7
    ) -> List[Dict]:
        """Recent play sessions: when, how long, what was practiced."""
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        r = await self._http.get(
            f"{PRODIGY_API}/v3/students/{user_id}/sessions",
            params={"since": since},
        )
        r.raise_for_status()
        return r.json().get("sessions", [])

    async def get_assignments(self, user_id: str) -> List[Dict]:
        """Teacher-assigned practice goals."""
        r = await self._http.get(
            f"{PRODIGY_API}/v3/students/{user_id}/assignments"
        )
        r.raise_for_status()
        return r.json().get("assignments", [])

    async def get_skill_mastery(self, user_id: str) -> List[Dict]:
        """
        Per-skill mastery scores: a number from 0-100 showing how confident
        the system is that the child has mastered each math standard.
        """
        r = await self._http.get(
            f"{PRODIGY_API}/v3/students/{user_id}/skills"
        )
        r.raise_for_status()
        return r.json().get("skills", [])

    # ── Helpers / derived metrics ─────────────────────────────────────────────

    async def summarize_week(self, user_id: str) -> Dict:
        """
        Build a single-page weekly report:
          - total play time
          - questions answered
          - accuracy
          - top skills improved
          - flagged areas needing practice
        """
        sessions = await self.get_session_history(user_id, days=7)
        skills   = await self.get_skill_mastery(user_id)

        total_minutes = sum(s.get("durationMinutes", 0) for s in sessions)
        total_qs      = sum(s.get("questionsAnswered", 0) for s in sessions)
        correct       = sum(s.get("questionsCorrect", 0) for s in sessions)
        accuracy      = (correct / total_qs * 100) if total_qs else 0.0

        strong = sorted(
            [s for s in skills if s.get("mastery", 0) >= 80],
            key=lambda s: s.get("mastery", 0),
            reverse=True,
        )[:5]
        weak = sorted(
            [s for s in skills if s.get("mastery", 0) < 50],
            key=lambda s: s.get("mastery", 0),
        )[:5]

        return {
            "weekStarting":    (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "totalMinutes":    total_minutes,
            "totalQuestions":  total_qs,
            "correctAnswers":  correct,
            "accuracyPercent": round(accuracy, 1),
            "sessionCount":    len(sessions),
            "strongSkills":    [{"name": s.get("name"), "mastery": s.get("mastery")} for s in strong],
            "weakSkills":      [{"name": s.get("name"), "mastery": s.get("mastery")} for s in weak],
        }

    async def screen_time_today(self, user_id: str) -> int:
        """Minutes played today."""
        sessions = await self.get_session_history(user_id, days=1)
        today    = datetime.now().date()
        return sum(
            s.get("durationMinutes", 0) for s in sessions
            if datetime.fromisoformat(s.get("startedAt", "").replace("Z", "")).date() == today
        )
