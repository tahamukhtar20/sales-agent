"""Usage limits for the public demo, so one visitor can't use up the API budget.

Two caps, both set by environment variables (0 turns a cap off):
- SESSION_BRIEF_LIMIT: briefs per browser session (default 2)
- DAILY_BRIEF_LIMIT: briefs per UTC day across all visitors (default 10)

The daily count lives in the server process, so it resets when the app restarts.
The workspace spend limit on the API key is the hard backstop.
"""

import os
import threading
from datetime import datetime, timezone

import streamlit as st


def _env_int(name: str, default: int) -> int:
    try:
        return max(0, int(os.getenv(name, default)))
    except ValueError:
        return default


@st.cache_resource
def _daily_counter() -> dict:
    return {"day": None, "count": 0, "lock": threading.Lock()}


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def check() -> str | None:
    """None if a brief may run now, otherwise the reason it can't."""
    session_limit = _env_int("SESSION_BRIEF_LIMIT", 2)
    if session_limit and st.session_state.get("briefs_run", 0) >= session_limit:
        return f"This demo allows {session_limit} briefs per visit. Run it locally with your own API key for more (see the README)."
    daily_limit = _env_int("DAILY_BRIEF_LIMIT", 10)
    counter = _daily_counter()
    with counter["lock"]:
        if counter["day"] != _today():
            counter["day"], counter["count"] = _today(), 0
        if daily_limit and counter["count"] >= daily_limit:
            return "The demo has reached today's limit. Try again tomorrow, or run it locally with your own API key."
    return None


def record() -> None:
    """Count a brief that is about to run."""
    st.session_state["briefs_run"] = st.session_state.get("briefs_run", 0) + 1
    counter = _daily_counter()
    with counter["lock"]:
        if counter["day"] != _today():
            counter["day"], counter["count"] = _today(), 0
        counter["count"] += 1
