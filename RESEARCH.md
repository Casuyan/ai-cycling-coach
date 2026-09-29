# Quarterly research review

> **Experimental.** Off by default. Turn it on by setting `Research review: on` in
> `athlete/ATHLETE.md` (onboarding asks). Expect rough edges, and tell us how it goes.

Sports science moves. Once a quarter, the coach looks at recent papers, decides whether any of
them should change how you train, and proposes changes. It never applies them on its own.

## When it runs
At the start of a session, if the review is on and the newest entry in `athlete/RESEARCH_LOG.md`
is more than 90 days old, the coach offers to run it. You can say no or ask it to wait. You can
also ask for a review any time.

## What the agent does

**1. Search.** Papers published since the last review (or the last 3 months) on:
- training intensity distribution (polarized, pyramidal, threshold)
- threshold, VO2max and repeated-sprint training in cyclists
- recovery, HRV-guided training, sleep
- fuelling and carbohydrate intake
- anything specific to this athlete's goal, age or history (e.g. masters, return from injury)

Sources: PubMed, SportRxiv, and journals such as *International Journal of Sports Physiology and
Performance*, *Medicine & Science in Sports & Exercise*, *European Journal of Applied Physiology*
and *Sports Medicine*. Use web search if the agent has it. Without web access, say so and stop.

**2. Weigh the evidence.** For each paper worth mentioning, note:
- design (randomised trial, observational, review/meta-analysis, case study)
- sample size, and whether subjects were trained cyclists or untrained people
- the size of the effect, and whether it has been replicated
- whether it applies to this athlete

One small study doesn't change the plan. A meta-analysis or several consistent trials in trained
cyclists might. Preprints are flagged as such.

**3. Write it up.** Append a dated entry to `athlete/RESEARCH_LOG.md`:

```
## 2027-01-10 review (covers 2026-10 → 2027-01)
### Papers
- <authors, year, title, link>: <two-sentence plain summary>. Design: <...>, n=<...>, trained: <y/n>.
  Relevance to me: <high / some / none, and why>.
### Proposed changes
1. <what would change in METHOD.md or the current block>, because <paper(s)>. Confidence: <low/medium/high>.
### Not proposing
- <anything interesting that isn't strong enough yet>
```

Keep it to three proposals at most. "No changes this quarter" is a normal result.

**4. Ask.** Add a one-line pointer to `athlete/CHECKINS.md`, then walk the athlete through the
proposals. Each one gets accepted or rejected.

**5. Apply only what's accepted.** Accepted changes go into `athlete/DECISIONS.md` with the
paper as the reason, then into METHOD.md, ATHLETE.md or the current block as needed. If a change
would apply to everyone using this repo, offer to draft a "research finding" issue for the
upstream project (with no personal data in it).
