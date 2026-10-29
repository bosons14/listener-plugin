# Safety design

## Scope

Listener offers emotional support. It is not a medical device, and it does not diagnose,
treat or replace professional care. It runs inside Claude Code, so whoever uses it has
access to a terminal. This is a tool for adults.

## Defence in depth

1. **Skill instructions** (`skills/listener/SKILL.md`) set the listening style and a
   mandatory crisis protocol that overrides everything else in the skill.
2. **Deterministic hook** (`hooks/crisis_check.py`) runs on every prompt, whether or not
   a listening session is active, so the safety net doesn't depend on the model noticing.
   - A HIGH match shows the user a helpline banner and tells Claude to follow the
     crisis protocol.
   - An ELEVATED match (self-harm, deep hopelessness) tells Claude to check in gently.
     There's no banner, to avoid alarming people needlessly.
   - It fails open: errors never block Claude Code.
   - It's private: no files, no network calls, no logging.
3. **Claude's own safety training** applies underneath both.

## Known limitations

- **Keyword detection is imperfect.** It misses indirect phrasing and some languages, and
  it sometimes flags harmless text (for example "an overdose of coffee"). The model's
  judgement in context is the main layer; the hook is a backstop.
- **It can't act in the world.** Listener can't call emergency services, alert a contact or
  track location. It can only encourage the person and help them reach help themselves.
- **Helpline numbers change.** They were verified in October 2026. Re-check
  `skills/listener/references/helplines.md` before every release.
- **No clinical validation.** The protocol follows widely used public guidance (direct
  asking, QPR, Stanley–Brown safety planning) but hasn't been reviewed or tested by
  clinicians. A review by a mental-health professional is strongly recommended before
  wide distribution.

## Reporting

If Listener responds unsafely, please open an issue (leave out personal details) so the
patterns and protocol can be improved.
