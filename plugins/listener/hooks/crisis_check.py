#!/usr/bin/env python3
"""Listener crisis check — a UserPromptSubmit hook for Claude Code.

Reads the hook payload (JSON) on stdin, looks for signs of suicide or self-harm
risk in the user's message, and if any are found:
  * shows the user a short, calm message with helplines (systemMessage), and
  * adds context telling Claude to follow the Listener crisis protocol.

Design rules:
  * Never block or alter the user's message.
  * Never write anything to disk or the network. No logging of content.
  * Fail open: any error -> exit 0 silently, so Claude Code keeps working.
  * Prefer catching too much over too little; Claude checks gently in context.

Standard library only.
"""
import json
import re
import sys

# --- Patterns -------------------------------------------------------------
# HIGH: explicit suicidal thoughts, intent or action.
HIGH = [
    r"\bkill(ing)?\s+my\s*self\b",
    r"\bend(ing)?\s+(it\s+all|my\s+(own\s+)?life|everything)\b",
    r"\btake\s+my\s+(own\s+)?life\b",
    r"\b(i\s+)?(want|wanna|wish|plan(ning)?)\s+(to\s+)?die\b",
    r"\bi\s+(want|wish)\s+i\s+(was|were)\s+dead\b",
    r"\bbetter\s+off\s+(dead|without\s+me)\b",
    r"\bsuicid(e|al)\b",
    r"\bno\s+reason\s+to\s+(live|go\s+on)\b",
    r"\b(don'?t|do\s+not)\s+want\s+to\s+(live|be\s+alive|exist)\b",
    r"\b(hang|hanging)\s+my\s*self\b",
    r"\boverdos(e|ed|ing)\b",
    r"\btook\s+(a\s+lot\s+of|all\s+(my|the))\s+(pills|tablets)\b",
    r"\bthis\s+is\s+my\s+(final\s+)?goodbye\b",
    r"\bwon'?t\s+be\s+(here|around)\s+(tomorrow|much\s+longer)\b",
    # Hindi / Hinglish (romanised and Devanagari)
    r"\bkhud\s*kushi\b",
    r"\baatma\s*hatya\b|\batmahatya\b",
    r"\bmar(na)?\s+(jaana|jana|jaunga|jaungi|chahta|chahti)\b",
    r"\bjee?na\s+nahi\s+chahta\b|\bjee?na\s+nahi\s+chahti\b",
    r"\bzindagi\s+khatam\b",
    "आत्महत्या",
    "ख़ुदकुशी|खुदकुशी",
    r"मरना\s*चाहता|मरना\s*चाहती|मर\s*जाना",
    r"जीना\s*नहीं\s*चाहता|जीना\s*नहीं\s*चाहती",
]

# ELEVATED: self-harm, deep hopelessness, feeling like a burden.
# Self-harm: never suppressed by technical words.
SELF_HARM = [
    r"\b(hurt|hurting|harm|harming|cut|cutting|burn|burning)\s+my\s*self\b",
    r"\bself[\s-]?harm",
]

# Hopelessness: suppressed when the message is clearly about software.
ELEVATED = [
    r"\bhopeless\b",
    r"\bcan'?t\s+(go\s+on|take\s+(it|this)\s+any\s*more|do\s+this\s+any\s*more)\b",
    r"\b(i'?m|i\s+am)\s+a\s+burden\b|\bburden\s+(to|on)\s+(everyone|my\s+family)\b",
    r"\bno\s+point\s+(in\s+)?(living|anything|going\s+on)\b",
    r"\bdisappear\s+forever\b",
    r"\bnobody\s+would\s+(care|miss\s+me|notice)\b",
]

# Clearly technical uses we should not flag (coding is what Claude Code is for).
TECHNICAL = re.compile(
    r"\b(process|thread|pid|job|container|pod|daemon|server|task|session|loop|"
    r"query|build|branch|program|script|kernel|node|worker)\b",
    re.IGNORECASE,
)

HIGH_RE = [re.compile(p, re.IGNORECASE) for p in HIGH]
SELF_HARM_RE = [re.compile(p, re.IGNORECASE) for p in SELF_HARM]
ELEVATED_RE = [re.compile(p, re.IGNORECASE) for p in ELEVATED]


def assess(text: str) -> str:
    """Return 'high', 'elevated' or 'none'."""
    if not text:
        return "none"
    if any(r.search(text) for r in HIGH_RE):
        return "high"
    if any(r.search(text) for r in SELF_HARM_RE):
        return "elevated"
    if any(r.search(text) for r in ELEVATED_RE):
        # "can't take this anymore" about a flaky build is not a crisis.
        if TECHNICAL.search(text):
            return "none"
        return "elevated"
    return "none"


USER_MESSAGE = (
    "You're not alone. If you are thinking about suicide or are in danger, "
    "please reach out now. India: Tele-MANAS 14416 (free, 24x7) or emergency 112. "
    "US/Canada: call or text 988. UK & Ireland: Samaritans 116 123. "
    "Elsewhere: findahelpline.com or your local emergency number."
)

CONTEXT = {
    "high": (
        "[LISTENER CRISIS CHECK — HIGH] The user's message contains possible signs of "
        "suicidal thoughts or intent. Follow the listener skill's CRISIS PROTOCOL now "
        "(read skills/listener/references/crisis-protocol.md and helplines.md in the "
        "listener plugin). Respond with warmth; ask directly and calmly whether they are "
        "thinking about ending their life and whether they are safe right now; share the "
        "helpline for their country; if danger is immediate, urge emergency services and "
        "getting a person physically with them. Never give method or dosage information. "
        "Do not end or deflect the conversation. If context shows this is clearly not about "
        "the user's own safety (e.g. quoting a book), respond normally but stay attentive."
    ),
    "elevated": (
        "[LISTENER CRISIS CHECK — ELEVATED] The user's message may show self-harm or deep "
        "hopelessness. Respond with warmth and reflective listening, and gently check in on "
        "their safety (you may ask directly about thoughts of suicide or self-harm). If risk "
        "is confirmed, follow the listener skill's CRISIS PROTOCOL. If context shows this is "
        "clearly not about their wellbeing, respond normally."
    ),
}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    prompt = payload.get("prompt") if isinstance(payload, dict) else None
    if not isinstance(prompt, str):
        return 0

    level = assess(prompt)
    if level == "none":
        return 0

    out = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": CONTEXT[level],
        }
    }
    if level == "high":
        out["systemMessage"] = USER_MESSAGE
    print(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
