"""Tests for the crisis-check hook. Run: python3 -m unittest discover -s tests"""
import json
import pathlib
import subprocess
import sys
import unittest

HOOK = pathlib.Path(__file__).resolve().parents[1] / "hooks" / "crisis_check.py"
sys.path.insert(0, str(HOOK.parent))
from crisis_check import assess  # noqa: E402

HIGH = [
    "I want to kill myself",
    "i've been thinking about ending my life",
    "Honestly everyone would be better off without me",
    "I don't want to live anymore",
    "having suicidal thoughts again tonight",
    "I think I'm going to end it all",
    "there is no reason to live",
    "this is my goodbye",
    "main khudkushi karna chahta hoon",
    "ab jeena nahi chahta",
    "मैं आत्महत्या के बारे में सोच रहा हूँ",
    "मैं मरना चाहता हूँ",
]

ELEVATED = [
    "I've been cutting myself again",
    "I feel completely hopeless",
    "I'm a burden to everyone",
    "I can't go on like this",
    "nobody would miss me",
]

NONE = [
    "kill the process on port 3000",
    "how do I end the session gracefully",
    "my laptop battery is going to die",
    "this build is hopeless, the node worker keeps crashing",
    "I can't take this anymore, the server keeps timing out",
    "refactor the auth module",
    "I'm tired but happy today",
    "",
]


class TestAssess(unittest.TestCase):
    def test_high(self):
        for t in HIGH:
            with self.subTest(t=t):
                self.assertEqual(assess(t), "high")

    def test_elevated(self):
        for t in ELEVATED:
            with self.subTest(t=t):
                self.assertEqual(assess(t), "elevated")

    def test_none(self):
        for t in NONE:
            with self.subTest(t=t):
                self.assertEqual(assess(t), "none")


def run_hook(stdin: str):
    return subprocess.run(
        [sys.executable, str(HOOK)], input=stdin, capture_output=True, text=True, timeout=5
    )


class TestHookIO(unittest.TestCase):
    def test_high_output(self):
        r = run_hook(json.dumps({"prompt": "I want to end my life", "hook_event_name": "UserPromptSubmit"}))
        self.assertEqual(r.returncode, 0)
        out = json.loads(r.stdout)
        self.assertIn("14416", out["systemMessage"])
        self.assertEqual(out["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("CRISIS PROTOCOL", out["hookSpecificOutput"]["additionalContext"])

    def test_elevated_has_no_user_banner(self):
        out = json.loads(run_hook(json.dumps({"prompt": "I feel hopeless"})).stdout)
        self.assertNotIn("systemMessage", out)

    def test_silent_when_nothing_found(self):
        r = run_hook(json.dumps({"prompt": "write a unit test"}))
        self.assertEqual((r.returncode, r.stdout), (0, ""))

    def test_fails_open_on_bad_input(self):
        for bad in ["", "not json", "[]", '{"prompt": 5}']:
            with self.subTest(bad=bad):
                r = run_hook(bad)
                self.assertEqual((r.returncode, r.stdout), (0, ""))


if __name__ == "__main__":
    unittest.main()
