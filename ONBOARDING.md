# Onboarding: instructions for the agent

Run this the first time the athlete says "onboard me" or when `athlete/ATHLETE.md` is blank.
By the end, `athlete/ATHLETE.md` and `athlete/SEASON_PLAN.md` are filled in, the training
approach is chosen, and week 1 is on the calendar. You're a coach doing an intake interview.
Don't hand out a form.

## Rules
- **Pull data before asking.** Never ask for something the API can answer.
- **Ask in rounds of 3–5 questions**, one topic per round. Wait for answers before moving on.
- **Show what the data says, then ask them to confirm or correct it.** For example: "your best
  20' this year is 312 W on 4 June. Was that a real all-out effort?"
- **Don't overfit one number.** A range with a stated source beats false precision.
- If they don't know something, write "unknown" and move on.

## Step 0: Non-negotiables
1. Run `python3 -m unittest tests.test_integration`. If it fails on credentials, help them fix
   `.env` (intervals.icu → Settings → Developer). Don't continue until it passes.
2. The activities test checks that recent rides carry power. **No power data means stop.**
   Explain that the whole method runs on power: zones, load, HR-vs-power, pacing. Heart rate
   alone lags and drifts too much to prescribe from. Tell them what's needed (a power meter or a
   smart trainer that records power, synced to intervals.icu) and pick up again once it's there.
3. Check whether they have intervals.icu synced to their head unit or Garmin/Wahoo account.
   If not, point them to intervals.icu → Settings → Connections.

## Step 1: What intervals.icu already knows (no questions yet)
Run `python3 scripts/check_plan.py`, then use `athlete_get`:
- `""` (athlete profile): weight, FTP, LTHR, max HR, resting HR, zones, bikes,
  `icu_garmin_upload_workouts`.
- `/activities?oldest=<12 months ago>&newest=<today>`: hours and TSS per week, riding days per
  week, usual long-ride length, indoor (`VirtualRide`) vs outdoor share, races, and whether rides
  have power and HR.
- `/wellness?oldest=<90 days ago>&newest=<today>`: CTL/ATL trend, and **which wellness signals
  exist**: HRV, resting HR, sleep, weight, soreness/fatigue/stress/mood fields. List what's
  missing and suggest connecting a source in intervals.icu (Garmin, Oura, Whoop, Apple Health,
  etc.). More signals mean better decisions, but none of them is required.
- **Best efforts**: pick the ~10 hardest rides of the last 3–6 months and run
  `python3 scripts/best_efforts.py <id> <id> ...`. Note the best 5 s, 1', 5', 20' and 60' with
  their avg HR, and the highest HR seen.

Summarise this in about 10 lines and show it before round 1. It shows you've looked and gives
the conversation an anchor.

## Step 2: Interview rounds

**Round 1: Who and why**
- Start open: **"Describe yourself as a rider, in your own words."** Read the answer and only ask
  follow-ups for what's missing below.
- Experience: how many years riding? Have they trained with structure or a coach before?
- What do they enjoy: climbing, racing, group rides, long days, gravel?
- The goal for the next 6–12 months: named events with dates, or a type (road races,
  granfondos, crits, gravel, TT, "just get faster")?
- Which event matters most (A), and which are for training or fun (B/C)?

**Round 2: Time and life**
- Realistic hours per week, and the limit on weekdays vs weekends?
- Fixed days (work, family)? Any regular group rides or club races, and how hard are they?
- Known trips, holidays or busy periods in the next months? (These become NOTE events.)
- A rigid plan, or one that adapts week to week?

**Round 3: Equipment**
- Power meter (which one), and on which bikes? HR strap or wrist HR?
- Indoor trainer? Smart trainer with ERG? Zwift or similar? How much indoor riding can they stand?
- Head unit (Garmin/Wahoo)? Do they want workouts pushed to it?

**Round 4: Physiology** (confirm the Step 1 numbers)
- Weight now, and is it changing?
- Any lab lactate or ramp test? Ask for the numbers or the PDF: power and HR at LT1/LT2, max,
  and the full step table if they have it.
- Where did the FTP in intervals.icu come from, and when? Could they actually hold it for ~60'?
- Highest HR ever seen, and resting HR.
- Do the Step 1 best efforts look right, or were some on descents, in a draft, or glitches?

**Round 5: Health and recovery**
- Current or past injuries: knees, back, crashes, concussion? Anything a doctor or physio restricts?
- Sleep on average? Do they track HRV?
- What happens when they overdo it: getting sick, sleeping badly, legs dead for days?
- Their usual failure mode: easy days too hard, skipping rest, or losing motivation?

**Round 6: Habits and preferences**
- Fuelling: how many g/h of carbs on long or hard rides? Stomach issues? Past bonks?
- Strength training: doing it, want to, or not now?
- Other sports?
- Coaching style: blunt or gentle, full numbers or the headline, how often they'll check in.
- **Research review (experimental):** "Once a quarter I can look at recent sports science papers
  and suggest changes to how we train. Nothing changes without your OK. Want that on?"

## Step 3: Write it down
1. **Choose the approach.** Use the table in `METHOD.md` ("Choosing the approach") with their
   goal, rider type, experience and hours. If none fits, build one from their own description and
   say which rows you borrowed from. Explain the choice in two or three sentences and let them
   push back.
2. **ATHLETE.md**: every field. Each number gets its source and date, e.g.
   "FTP 300 (20' test × 0.92, 2026-05-10)".
3. **Zones** in absolute watts, from the best source available:
   - lab LT1/LT2 if they have them
   - otherwise a field FTP (or the baseline test below)
   - VO2 targets from the real 5' best (~90–95% of it)
   - Z2 capped at LT1, or ~0.75 × FTP without a lab test
4. **`athlete/lactate_curve.csv`**: same format as `lactate_curve.example.csv` (header `watts,hr`), with the lab points. With no lab test,
   fill it from matched steady efforts found with `best_efforts.py`, and write in ATHLETE.md
   that the curve is estimated. With no reliable HR data, leave the file out.
5. **intervals.icu FTP**: if it differs from the agreed working FTP, ask them to change it in the
   UI (Settings → sport settings). The API can't write it.
6. **SEASON_PLAN.md**: goal, A/B/C events, phases planned back from the A event.
7. **Calendar anchors**: POST each race (RACE) and each trip or no-bike period (NOTE).
8. **DECISIONS.md**: log the approach, working FTP and zones, the season goal and the block
   design, each with its reason.
9. **CHECKINS.md**: first entry, "Onboarding", with the baseline (CTL, weekly hours, key numbers).

## Step 4: Baseline test (if needed)
If there's no lab test and no recent all-out effort they trust, week 1 includes a field test.
Pick one and put it on the calendar as a proper workout:
- **20' test** after a 5' hard opener. The standard. Multiplier by rider type (see AGENTS.md).
- **Ramp test**. Quick and easy to pace indoors. Overestimates FTP for punchy riders.
- **3' + 12' test**. Gives a rough power profile as well as an FTP estimate.

Newer riders do better with the ramp test. Riders who know how to pace suit the 20' test. Put a
retest on the calendar every 6–8 weeks, or at the end of each block.

## Step 5: First block
- Write `athlete/BLOCK_<name>.md` (3–6 weeks). If fitness is unclear, start conservative:
  - build week 1 from their recent actual volume, not their ambitions
  - one hard weekday session at most if they have a hard group ride that week
  - ACWR under 1.3
  - a real rest day
- Put the sessions on the calendar with `create_workout`. Follow the step-syntax gotchas in
  AGENTS.md, add a `Fuel:` line to every workout, then re-fetch and check `blank_steps()` is empty.
- Show them week 1 and ask what doesn't fit their life before building the rest.

Done when ATHLETE.md has no blank fields (or they're marked "unknown"), the approach is chosen
and logged, the season goal and anchors are on the calendar, and they've agreed to week 1.
