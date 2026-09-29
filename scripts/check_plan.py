"""Daily check-in helper (read-only). Rolling coach view — not tied to any block.

Shows: fitness snapshot + wellness trend, day-by-day planned vs actual for the last
2 weeks (INCLUDING unplanned rides and possible duplicates), and the week ahead.

Usage:
    python3 scripts/check_plan.py            # status as of today
    python3 scripts/check_plan.py 2026-01-15 # pretend "today" is this date

Needs INTERVALS_API_KEY and INTERVALS_ATHLETE_ID in .env (see .env.example).
"""
import sys, csv, datetime
from pathlib import Path
from intervals_common import athlete_get, ROOT

LOOKBACK_DAYS = 14
LOOKAHEAD_DAYS = 7

CURVE_FILE = ROOT / "athlete" / "lactate_curve.csv"


def load_curve(path=CURVE_FILE):
    """Your lab (or field) HR-vs-power curve as [(watts, hr), ...], low -> high.

    Read from athlete/lactate_curve.csv (header: watts,hr). Returns [] if the file is
    missing, and the HR-vs-curve check is then skipped.
    """
    path = Path(path)
    if not path.exists():
        return []
    with path.open() as f:
        pts = [(float(r["watts"]), float(r["hr"])) for r in csv.DictReader(f) if r.get("watts")]
    return sorted(pts)


LACTATE_CURVE = load_curve()


def predicted_hr(watts, pts=None):
    """Interpolate HR at a given power from the curve. None if no curve or no watts."""
    pts = LACTATE_CURVE if pts is None else pts
    if watts is None or not pts:
        return None
    if watts <= pts[0][0]:
        return 60 + (watts / pts[0][0]) * (pts[0][1] - 60)
    for (w1, h1), (w2, h2) in zip(pts, pts[1:]):
        if watts <= w2:
            return h1 + (watts - w1) / (w2 - w1) * (h2 - h1)
    return pts[-1][1]


def load_of(e):
    return e.get("icu_training_load") or 0


def fmt_act(a):
    mins = round((a.get("moving_time") or 0) / 60)
    parts = [f"{mins}min", f"TSS {load_of(a)}"]
    avg_w, np_w = a.get("icu_average_watts"), a.get("icu_weighted_avg_watts")
    hr = a.get("average_heartrate")
    if avg_w:
        parts.append(f"avg {avg_w}W / NP {np_w}W")
    if hr:
        parts.append(f"avgHR {round(hr)}")
    pred = predicted_hr(np_w) if hr else None
    if pred:
        vi = a.get("icu_variability_index") or 1
        # Whole-ride NP vs avg HR is misleading on surgy rides: coasting drags avg HR down.
        caveat = "  surgy, use best_efforts.py" if vi > 1.1 else ""
        parts.append(f"(curve-pred {pred:.0f} @ NP -> {hr - pred:+.0f}{caveat})")
    ef = a.get("icu_efficiency_factor")
    if ef:
        parts.append(f"EF {ef:.2f}")
    return "  ".join(parts)


def possible_duplicates(acts):
    """Pairs of same-day activities with ~same duration (<90 s apart) and TSS (<=3 apart).

    Manual re-uploads show up like this and inflate CTL/ATL/Form.
    """
    pairs = []
    for i in range(len(acts)):
        for j in range(i + 1, len(acts)):
            a, b = acts[i], acts[j]
            if (abs((a.get("moving_time") or 0) - (b.get("moving_time") or 0)) < 90
                    and abs(load_of(a) - load_of(b)) <= 3):
                pairs.append((a, b))
    return pairs


def main():
    today = datetime.date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else datetime.date.today()
    start = today - datetime.timedelta(days=LOOKBACK_DAYS)
    end = today + datetime.timedelta(days=LOOKAHEAD_DAYS)

    # Wellness trend (last 7 days)
    wstart = today - datetime.timedelta(days=6)
    well = athlete_get(f"/wellness?oldest={wstart}&newest={today}") or []
    if well:
        w = well[-1]
        ctl, atl = w.get("ctl") or 0, w.get("atl") or 0
        acwr = atl / ctl if ctl else 0
        flag = "  ** ACWR above 1.3 ceiling **" if acwr > 1.3 else ""
        print(f"Fitness ({today}):  CTL {ctl:.0f}  ATL {atl:.0f}  Form {ctl - atl:+.0f}"
              f"  ACWR {acwr:.2f}{flag}")
        print("Wellness trend:")
        for d in well:
            sleep = d.get("sleepSecs")
            sleep_s = f"sleep {sleep / 3600:.1f}h" if sleep else ""
            print(f"  {d['id']}  restHR {d.get('restingHR') or '-':>3}  "
                  f"HRV {d.get('hrv') or '-':>4}  {sleep_s}")
    print()

    planned = [e for e in (athlete_get(
        f"/events?oldest={start}&newest={end}&category=WORKOUT") or [])
        if e.get("category") == "WORKOUT"]
    plan_by_date = {}
    for e in planned:
        plan_by_date.setdefault(e["start_date_local"][:10], []).append(e)

    acts = athlete_get(f"/activities?oldest={start}&newest={today}") or []
    acts_by_date = {}
    for a in acts:
        acts_by_date.setdefault(a["start_date_local"][:10], []).append(a)

    # Day-by-day: every day with a plan OR an activity (unplanned rides included)
    print(f"LAST {LOOKBACK_DAYS} DAYS (planned vs actual):")
    d = start
    while d <= today:
        ds = d.isoformat()
        plans, dones = plan_by_date.get(ds, []), acts_by_date.get(ds, [])
        if plans or dones:
            plan_s = " + ".join(f"{e['name']} ({load_of(e)} TSS)" for e in plans) or "(nothing planned)"
            print(f"  {ds}  plan: {plan_s}")
            for a in dones:
                print(f"              done: {(a.get('name') or '(unnamed)')[:40]:40}  {fmt_act(a)}")
            if not dones and d < today:
                print("              done: MISSED")
            for _ in possible_duplicates(dones):
                print("              ** POSSIBLE DUPLICATE above — verify before trusting CTL/ATL **")
        d += datetime.timedelta(days=1)

    # Week ahead
    print(f"\nNEXT {LOOKAHEAD_DAYS} DAYS (planned):")
    d = today + datetime.timedelta(days=1)
    any_up = False
    while d <= end:
        for e in plan_by_date.get(d.isoformat(), []):
            print(f"  {d}  {e['name']} ({load_of(e)} TSS)")
            any_up = True
        d += datetime.timedelta(days=1)
    if not any_up:
        print("  (nothing planned — the calendar needs the next block)")


if __name__ == "__main__":
    main()
