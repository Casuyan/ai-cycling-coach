# ai-cycling-coach

![ai-cycling-coach: a power trace of four 3-minute intervals ending in the workout step "3m 420W"](docs/cover.png)

**Your coach is a coding agent and a text file.**

It reads your rides, sleep and HRV from intervals.icu, talks through each session with you, and
rewrites your plan straight on your calendar. Connect intervals.icu to Garmin or Wahoo and
tomorrow's workout is on your head unit before you wake up.

The coaching method is plain text in [METHOD.md](METHOD.md). Every rule comes with its reason,
and if you disagree with one, you edit it.

## Why I built it

I'd tried the "adaptive" training apps, and none of them adapted to me. In May 2026 a car
decided it needed the lane more than I did, broke my shoulder blade, and gave me the time to
build something better. This coach got me through six weeks of hands-free indoor rehab, back on
the road, through a season of fun races, and into the best shape of my life.

What made it work was how well it knew me: my lab curve, my injury, the Thursday group ride that
always turns into a race, the granfondo where I ran out of fuel, and every time I'd told it a
number was wrong. A cold, a trip or a bad night's sleep changed the plan the same day, with the
reasoning written out.

I'm also not the most organised person. The coach let me move things around as much as I needed,
and still held me to account: a skipped session got asked about, an easy day ridden hard got
called out. That mix of flexibility and accountability is what kept me in my lane (the car
notwithstanding).

## Zoomed in and zoomed out

This is the part I'd miss most if I went back to an app. The coach plans on three horizons at
once and keeps them honest with each other.

- **Season.** Your goal, your races, holidays and busy months, planned backwards from the event
  that matters most. It sits in `athlete/SEASON_PLAN.md` and as race and note markers on your calendar.
- **Block.** Three to eight weeks with one job: build the base, raise threshold, sharpen for
  racing. Each block has a written design and a reason for it.
- **Day.** Every check-in: what was planned, what you actually did, how your body is doing, and
  what changes.

The day never loses sight of the season. Skip a session after four hours of sleep and the coach
knows whether it mattered for this block, so it moves it or drops it. It works upwards too: when
the daily numbers say you're ahead or behind, the block gets redesigned and the season goal gets
a second look. Each of those decisions is logged, so next month's coach knows why.

When something comes up last minute (a meeting runs late, the weather turns, friends call a
ride), the coach rebuilds the rest of the week around the sessions that matter most for your
goal right now, and lets the others go. You get the most training out of the time you actually have.

## Requirements

Non-negotiable. The method is built on these!

- **A power meter** (pedals, crank, hub, or a smart trainer that records power). Zones, load,
  pacing and the HR-vs-power checks all run on power.
- **A free [intervals.icu](https://intervals.icu) account**, synced with your head unit or
  Garmin/Wahoo/Zwift account so rides arrive on their own.
- **A coding agent subscription**: any coding agent, e.g. [Claude Code](https://claude.com/claude-code),
  [Codex](https://openai.com/codex) or [Cursor](https://cursor.com).
- **Python 3.** Standard library only, nothing to install.

Worth having: a heart rate strap, a smart trainer, and a lab lactate test if you can get one.
HRV and sleep data from a watch or ring make every check-in sharper.

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
- "Is my season goal still realistic? Plan the next block."

Check in after key sessions and tell it about life: travel, bad sleep, a group ride that got
out of hand. Argue when something looks wrong. It's usually worth it, and your corrections
become rules the coach follows from then on.

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

<sub>progressive ciclismo</sub>
