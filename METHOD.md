# The method

How the coach decides what you ride. The agent reads this; so should you. If you disagree with
something, change it here and it changes how you're coached.

Part A is about choosing the overall approach for you. Part B is the set of principles that apply
to everyone, and each one comes with the reason it exists. Most of them were learned the hard way
during the season this repo came out of.

## Part A: Choosing the approach

Your goal, the kind of rider you are, your experience and the hours you have decide how the
intensity is spread across the week. The agent picks a default at onboarding, explains it, and
revisits it at the start of every block. You can overrule it.

| Situation | Default approach |
|---|---|
| Long events (granfondo, ultra, long gravel) and 8+ h/week | **Polarized or pyramidal.** Most time in Z2, a small amount of VO2 work, little time at threshold. |
| Time-crunched, under ~6 h/week | **Pyramidal, leaning on sweet spot and threshold.** Not enough hours for volume to do the work alone. |
| Raising FTP for time trials, hill climbs, long climbs | **Threshold-focused blocks** (sweet spot → threshold → over-unders) on top of an aerobic base. |
| Short punchy road races and crits | **Base and threshold first, then VO2 and repeated hard efforts** (30/15s, attacks, sprints) closer to race season. |
| New to structured training | **Consistency first.** Z2 volume and one quality session a week. Most of the gains come from riding regularly. |
| Masters, or returning from injury or a long break | **Same as above with more recovery.** Extra easy days, a slower ramp, and strength work. |
| **Describe yourself** (none fits, or a mix) | Tell the coach about yourself in your own words. It builds an approach from the principles below, says which rows it borrowed from, and logs why. |

Why these defaults:
- **Polarized / pyramidal for long events.** Well-trained endurance athletes tend to spend most
  of their time easy and a small share very hard (Seiler's work on intensity distribution;
  Stöggl & Sperlich 2014 comparing distributions). With enough hours, this builds the aerobic
  engine without piling up fatigue.
- **Threshold-heavy when time is short.** With 4–6 hours there isn't enough easy volume to drive
  adaptation, so a larger share of sweet spot and threshold gets more out of each hour. The cost
  is fatigue, which the load rules below keep in check.
- **Repeated hard efforts for short races.** Races under three hours are decided by surges.
  Short-interval VO2 formats like 30/15s have good evidence in trained cyclists (Rønnestad and
  colleagues).
- **Consistency for beginners.** Almost anything works at first. Missing weeks is what stalls progress.
- **More recovery for masters and returning riders.** Recovery slows with age and after time
  off. Heavy strength training helps cycling performance and bone health (Rønnestad & Mujika 2014).

These are starting points. The quarterly research review (see [RESEARCH.md](RESEARCH.md)) can
propose changes to this table.

## Part B: Principles

**1. The calendar is the plan. Files are the memory.**
Workouts live on the intervals.icu calendar, where your head unit and the analysis already are.
The markdown files in `athlete/` hold what the coach needs to remember between sessions:
your profile, decisions and check-ins. Nothing important should live only in a chat.

**2. Three horizons.**
Season (goals, events, phases), block (3–8 weeks with one purpose), week (check-ins and small
changes). Most coaching happens at the week level, while the season and block keep the week
pointed somewhere.

**3. Pull data before asking.**
The coach looks at your rides, wellness and calendar before it asks you anything. That keeps
questions short and lets you correct what the data gets wrong.

**4. Zones in absolute watts, from the best anchor you have.**
Lab test beats field test, and a field test beats an estimate. Every number carries its source
and date. Where the evidence gives a range, the coach says so. If you've never held a number for
an hour, it takes the conservative end. VO2 targets come from your real 5-minute best rather
than a percentage of FTP, because riders with a strong top end would otherwise be under-targeted.

**5. Use every signal you can get.**
Power, heart rate, sleep, HRV, resting HR, weight, and what you say about legs, stress,
motivation or illness. Each one is noisy on its own. The coach reads trends against your own
baseline over several days. A multi-day HRV drop, or a resting HR that stays up, holds back
intensity even when the legs feel fine. HRV-guided training has shown results in cyclists
(Javaloyes and colleagues, 2019).

**6. Compare heart rate and power only on matched efforts.**
Whole-ride normalized power against whole-ride average heart rate is misleading on a surgy
ride: coasting pulls the heart rate average down while the surges push NP up. For a real read,
take a sustained window (a climb, an interval) and compare its power with its own heart rate.
Over time, lower HR at the same power is one of the clearest signs you're getting fitter.

**7. Load discipline.**
The ratio of acute (7-day) to chronic (42-day) load stays under 1.3. It's a crude guardrail
(the research on it is disputed), but it catches the most common mistake: easy days quietly
becoming medium days, and fatigue building up until form collapses.

**8. Plan around real life.**
Group rides, races and fun days are usually hard. The coach counts them as quality sessions and
reduces the structured intensity that week. The author's own version was one free ride and one
protected long ride every weekend, and it worked because the group ride was never going to be easy.
Yours will look different. Holidays, weddings and bad weeks go on the calendar and the plan
works around them.

**9. Fuel every session.**
Every workout has a carb target. Under-fuelling makes hard sessions worse and long events end
early. With 80–90 g/h (glucose and fructose, trained gut), upper-tempo pacing is sustainable for
hours, so "stay under LT1" only applies to unfuelled or ultra-distance efforts.

**10. Your pushback is data.**
If a number feels wrong, say so. The coach explains its reasoning, and when you're right it
logs the correction as a rule in `DECISIONS.md`. Future sessions follow it.

**11. Adherence beats the ideal plan.**
A plan you actually ride beats a better one you skip. When the two conflict, the coach picks
the one you'll do and says what it costs.

**12. Returning from injury.**
The doctor or physio sets the limits and the plan follows them. Start on the trainer, seated,
in ERG mode, where there's no fall risk. After a concussion, progress only when you've been
free of symptoms for the whole session and the 24 hours after it. If your position is
restricted, trim zones to what you can actually hold and raise them as the position comes back.
Easy volume is the safest thing to build. Intensity waits for clearance.

## Why an agent and plain files

Coaching apps turn your data into a plan with logic you can't see or change. This repo does the
opposite. The whole method is in text files: you can read them, and the agent follows them.

The setup is a small version of patterns from current AI agent work:
- **An agent loop with tools.** The agent reads your data through a small API wrapper, reasons
  about it, and writes back to your calendar. It checks its own writes (`blank_steps()`).
- **Memory in files.** Check-ins and decisions are appended to markdown. Each session starts by
  reading them, so the coach remembers what happened last week and why.
- **A human in the loop.** You approve the plan, push back on numbers, and your corrections
  become rules. The coach is more reliable because you're part of the loop.
- **Instructions as code.** AGENTS.md, ONBOARDING.md and this file are the coach's program. Edit
  them and the behaviour changes. No retraining or settings screens.
