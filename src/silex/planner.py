from __future__ import annotations

import json
import os
import urllib.error
import urllib.request

from silex.wedge import KITTING_STEPS

ALLOWED = list(KITTING_STEPS)


class Proposal:
    def __init__(self, goal: str, steps: list[str], source: str, raw: str = "") -> None:
        self.goal = goal
        self.steps = steps
        self.source = source
        self.raw = raw

    def as_dict(self) -> dict:
        return {"goal": self.goal, "steps": self.steps, "source": self.source, "raw": self.raw}


def _sanitize(steps: list[str]) -> list[str]:
    clean: list[str] = []
    for step in steps:
        name = str(step).strip().lower()
        if name in ALLOWED and name not in clean:
            clean.append(name)
    return clean or list(ALLOWED)


def local_propose(text: str) -> Proposal:
    lowered = text.lower()
    if "inspect" in lowered or "quality only" in lowered:
        steps = ["confirm", "quality"]
    elif "halt" in lowered or "stop" in lowered:
        steps = ["confirm"]
    else:
        steps = list(ALLOWED)
    return Proposal(goal=text.strip() or "kit order-1", steps=_sanitize(steps), source="local")


def llm_propose(text: str) -> Proposal | None:
    url = os.environ.get("SILEX_LLM_URL")
    key = os.environ.get("SILEX_LLM_KEY")
    model = os.environ.get("SILEX_LLM_MODEL", "grok-4")
    if not url or not key:
        return None
    body = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You propose work for Silex. Return JSON only: "
                    '{"goal": string, "steps": string[]}. '
                    f"Steps must be a subset of {ALLOWED}. You cannot execute."
                ),
            },
            {"role": "user", "content": text},
        ],
        "temperature": 0,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None
    content = payload.get("choices", [{}])[0].get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
        steps = _sanitize(list(parsed.get("steps", [])))
        goal = str(parsed.get("goal") or text).strip()
        return Proposal(goal=goal, steps=steps, source="llm", raw=content)
    except (json.JSONDecodeError, TypeError, AttributeError):
        return Proposal(goal=text.strip(), steps=list(ALLOWED), source="llm-fallback", raw=content)


def propose(text: str) -> Proposal:
    return llm_propose(text) or local_propose(text)
