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
