# ai-cycling-coach

A cycling coach that runs on a coding agent and your intervals.icu account.

The agent reads your rides, wellness data and calendar from intervals.icu, checks in with you
after sessions, and changes the plan directly on your calendar. If intervals.icu is connected to
Garmin or Wahoo, the workouts land on your head unit.

The coaching method is written in plain text ([METHOD.md](METHOD.md)). You can read every
rule and the reason for it, and change any of them by editing a file.

## Why

I built this for myself because I wasn't happy with the "adaptive" training plans I'd tried.
I finally had time to build it in May 2026, when a car decided it needed the lane more than I did.
I broke my shoulder blade, and this helped me through six weeks of indoor rehab, back onto the
road, through a season of fun races, and into the best shape I've been in.

What made the difference was how personal it got. The coach knew my lab curve, my injury, which
days my group rides land on and how hard they really are, the fuelling mistakes I'd made, and
every time I'd told it a number was wrong. A cold, a trip or a bad night's sleep changed the
plan the same day, with a reason I could read. No app I'd used came close to that.

## Requirements

These are non-negotiable. The method depends on them!

- **A power meter** (pedals, crank, hub, or a smart trainer that records power). Zones, load,
  pacing and the HR-vs-power checks all run on power.
- **A free [intervals.icu](https://intervals.icu) account**, synced with your head unit or
  Garmin/Wahoo/Zwift account so rides arrive on their own.
- **A coding agent subscription**: any coding agent, e.g. [Claude Code](https://claude.com/claude-code),
  [Codex](https://openai.com/codex) or [Cursor](https://cursor.com).
- **Python 3.** Standard library only, nothing to install.

Recommended: a heart rate strap, a smart trainer, and a lab lactate test if you can get one.
HRV and sleep data from a watch or ring make the check-ins better.

## Setup

1. Get your API key and athlete ID from intervals.icu → **Settings → Developer**.
2. `cp .env.example .env` and fill in both. `.env` is gitignored.
3. Check the connection: `python3 -m unittest`.
4. Open the folder in your agent and say:
   > Onboard me.

   The agent pulls your last year of data, interviews you in short rounds (goals, time,
   equipment, physiology, health, habits), picks a training approach with you, and puts
   week 1 on your calendar.
5. Optional: in intervals.icu, turn on workout upload to Garmin.

## Daily use

Just talk to it:

- "Check in: legs heavy, slept 6 hours." You get planned vs done, the numbers, how your body is
  doing, and what changes.
- "I'm away Friday to Monday, no bike." It reshapes the week.
- "Analyse yesterday's ride. What was my best 5 minutes?"

Check in after key sessions and tell it about life: travel, bad sleep, a group ride that got
out of hand. Push back when something looks wrong. Your corrections get written down as rules.

## How it works

| File | What it is |
|---|---|
| `AGENTS.md` | The coach's operating manual. Codex and Cursor read it directly; `CLAUDE.md` imports it. |
| `ONBOARDING.md` | The intake interview for your first session. |
| `METHOD.md` | The coaching method: how the approach is chosen and the principles behind it. |
| `RESEARCH.md` | Experimental, opt-in: a quarterly review of new sports science papers. |
| `athlete/` | Your profile, season plan, check-ins and decisions. The coach's memory. |
| `scripts/check_plan.py` | Read-only status: fitness, load, wellness, 14 days planned vs done, the week ahead. |
| `scripts/best_efforts.py` | Best power windows in a ride with their heart rate. |
| `scripts/intervals_common.py` | The small intervals.icu API wrapper the agent uses. |
| `tests/` | `python3 -m unittest`. Live tests run when `.env` is set; `RUN_WRITE_TESTS=1` also checks writing to the calendar. |
| `logs/errors.log` | API errors and problems the agent noticed. Local only. |

The plan itself lives on your intervals.icu calendar.

## Privacy

`athlete/` holds your health data. If you fork this repo, keep your fork private, or add
`athlete/` to `.gitignore`.

Your data also goes to whichever AI provider runs your agent. Turn off training on your
conversations:
- **Claude**: Settings → Privacy → turn off "Help improve Claude".
- **ChatGPT / Codex**: Settings → Data controls → turn off "Improve the model for everyone".
- **Cursor**: Settings → turn on Privacy Mode.

## Not medical advice

This is a training tool, not a doctor. If you're injured or ill, your doctor or physio decides
what you can do, and the plan follows.

## Contributing and contact

Bug reports, method proposals and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).
Questions and setups go in [Discussions](../../discussions).

I'm Francesco. I ride and race in Zürich and work in AI Security / Safety. You can find me on
[Strava](https://www.strava.com/athletes/71763685) and on grouprides with [Zürides](https://zurides.cc/).

MIT licensed.
