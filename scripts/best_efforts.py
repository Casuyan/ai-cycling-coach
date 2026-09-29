"""Best power efforts in one or more rides, with the avg HR of each window (read-only).

Use this for HR-vs-power reads on matched, sustained efforts, and for the onboarding
power profile. Whole-ride numbers hide what happened inside the ride.

Usage:
    python3 scripts/best_efforts.py <activity_id> [<activity_id> ...]
    python3 scripts/best_efforts.py i12345678 --windows 60,300,1200

Activity IDs come from /activities (the "id" field) or the intervals.icu URL.
"""
import sys
from intervals_common import api_get

DEFAULT_WINDOWS = [5, 60, 300, 1200, 3600]


def label(secs):
    return f"{secs}s" if secs < 60 else f"{secs // 60}'"


def best_window(watts, hr, secs):
    """Highest average power over `secs` consecutive samples (1 Hz stream).

    Returns (avg_watts, avg_hr, start_index) or None if the ride is shorter than the window.
    Missing samples (None) count as 0 W, like a coasting gap. avg_hr ignores missing HR.
    """
    w = [x or 0 for x in watts]
    if secs <= 0 or len(w) < secs:
        return None
    run = sum(w[:secs])
    best, best_i = run, 0
    for i in range(secs, len(w)):
        run += w[i] - w[i - secs]
        if run > best:
            best, best_i = run, i - secs + 1
    avg_hr = None
    if hr:
        window_hr = [h for h in hr[best_i:best_i + secs] if h]
        avg_hr = sum(window_hr) / len(window_hr) if window_hr else None
    return best / secs, avg_hr, best_i


def fetch_streams(activity_id):
    """Returns (watts, heartrate) lists for an activity. Either may be empty."""
    data = api_get(f"/activity/{activity_id}/streams?types=time,watts,heartrate") or []
    streams = {s.get("type"): s.get("data") or [] for s in data}
    return streams.get("watts", []), streams.get("heartrate", [])


def main():
    args = sys.argv[1:]
    windows = DEFAULT_WINDOWS
    if "--windows" in args:
        i = args.index("--windows")
        windows = [int(x) for x in args[i + 1].split(",")]
        args = args[:i] + args[i + 2:]
    if not args:
        raise SystemExit(__doc__)

    for aid in args:
        watts, hr = fetch_streams(aid)
        print(f"{aid}:")
        if not watts:
            print("  no power stream")
            continue
        for secs in windows:
            res = best_window(watts, hr, secs)
            if res is None:
                continue
            w, h, start = res
            hr_s = f"avgHR {h:.0f}" if h else "no HR"
            print(f"  best {label(secs):>4}  {w:5.0f} W  {hr_s:>9}  (from {start // 60}:{start % 60:02d})")
        max_hr = max((x for x in hr if x), default=None)
        if max_hr:
            print(f"  max HR {max_hr}")


if __name__ == "__main__":
    main()
