# Contributing

Thanks for helping. There are three useful ways in.

## Report a bug
Something broke: a script error, a workout that parsed wrong on the calendar, the agent
misreading an API field. Open a **bug report** issue. The last lines of `logs/errors.log`
usually help; they are already stripped of your API key and athlete ID.

## Propose a change to the method
You think a rule in `METHOD.md` or `AGENTS.md` is wrong, or something is missing. Open a
**method proposal** issue with:
- what should change
- the evidence: a paper, or a clear before/after from your own training
- who it applies to (everyone, or a type of rider)

If your quarterly research review turned up something, use the **research finding** template.

## Send a pull request
- Keep scripts to the Python standard library. Nobody should need to `pip install` anything.
- Run `python3 -m unittest` before opening the PR. Add a test for new script logic.
- Keep the docs short and plain. The agent reads them on every session, so every line costs
  context.

## Never post
- Your API key or athlete ID.
- Personal health data (lab reports, injury details, full check-in logs). Summarise instead.
