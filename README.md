# bosons14-plugins

Claude Code plugins by Subhendra Basu ([@bosons14](https://github.com/bosons14)). Add the
marketplace once, then install whichever plugins you want:

```
/plugin marketplace add bosons14/listener-plugin
/plugin install eda-ops@bosons14-plugins
```

| Plugin | What it does | Repo |
|---|---|---|
| **eda-ops** | RTL lint and review, CDC, Yosys QoR, self-checking testbenches, formal verification, OpenSTA timing closure, SDC/XDC review, EDA log triage. 8 skills, 2 agents, an MCP server. | [eda-ops](https://github.com/bosons14/eda-ops) |
| **codereview-ops** | Language-agnostic code review: scoped diffs, linter evidence, parallel independent reviewers, verified findings, security audit, SARIF/CI output. 3 skills, 3 agents. | [codereview-ops](https://github.com/bosons14/codereview-ops) |
| **plainproof** | Ask a number question in plain English; it is tested locally, then proved or refuted by Harmonic's Aristotle and explained without jargon. | [plainproof](https://github.com/bosons14/plainproof) |
| **bosontube** | Curated free AI, ML and Gen AI courses on YouTube, with learning paths and progress tracking. | [bosontube](https://github.com/bosons14/bosontube) |
| **listener** | An ELIZA-inspired compassionate listener with built-in crisis detection (below). | this repo |

```
/plugin install codereview-ops@bosons14-plugins
/plugin install plainproof@bosons14-plugins
/plugin install bosontube@bosons14-plugins
/plugin install listener@bosons14-plugins
```

---

# Listener

A compassionate listener for Claude Code, inspired by ELIZA, the first chatbot to explore the
mental-health space (Joseph Weizenbaum, MIT, 1966). Listener gives you a calm,
non-judgmental space to talk about stress, loneliness, grief or a hard day. It reflects
what you share, asks gentle open questions, and lets you lead.

> **Listener is not a therapist, counsellor, psychologist or psychiatrist, and it does not
> replace one.** It's a comforting presence. It can't contact anyone for you. If you're
> in danger, call your local emergency number (112 in India and the EU, 911 in the US and
> Canada, 999 in the UK).

## Install

```
/plugin marketplace add bosons14/listener-plugin
/plugin install listener@bosons14-plugins
```

## Use

| Command | What it does |
|---|---|
| `/listener:listen [what's on your mind]` | Start a listening session |
| `/listener:crisis-help` | Show crisis helplines and emergency numbers right away |

You can also just start talking about how you feel. The `listener` skill activates on
its own when the conversation turns personal.

## Safety: built in, always on

- **Crisis detection hook.** Every message you send is checked locally on your machine for
  signs of suicide or self-harm risk, in English, Hindi and Hinglish. If it finds any,
  Listener shows helpline numbers straight away and Claude switches to the crisis
  protocol. The hook never blocks your message, never saves it and never sends it
  anywhere.
- **Crisis protocol.** Claude asks directly and calmly about safety, works out how urgent
  things are, shares the right helpline for your country, urges emergency help when the
  danger is immediate, and helps you reach a trusted person and make a short safety plan.
  It keeps talking with you afterwards.
- **Hard limits.** No diagnosis, no medication advice, and never any information about
  methods of self-harm.

See [SAFETY.md](SAFETY.md) for the full design and its limits.

## Helplines

| Where | Who | Number |
|---|---|---|
| India | Tele-MANAS (free, 24×7, 20+ languages) | **14416** / 1-800-891-4416 |
| US / Canada | Suicide & Crisis Lifeline | call or text **988** |
| UK & Ireland | Samaritans | **116 123** |
| Australia | Lifeline | **13 11 14** |
| Anywhere | Find A Helpline | https://findahelpline.com |

## Requirements

Python 3 on your `PATH` as `python3` (for the crisis hook; standard library only). On
Windows, if only `python` is available, edit `hooks/hooks.json`.

## Development

```
python3 -m unittest discover -s tests -v
claude --plugin-dir ./plugins/listener
```

## Licence

MIT. Author: Subhendra Basu ([@bosons14](https://github.com/bosons14)).
