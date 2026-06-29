#!/usr/bin/env python3
"""Refresh data/snapshot.json from the backend."""
import json, os, sys, time, urllib.request, urllib.error

BASE = "http://43.161.221.88:16888"
TOKEN = os.environ.get("API_TOKEN") or "eWa4S7L51xQJ0DAVwP68XGN2BM9HnFrU"


def fetch(path, retries=5):
    sep = "&" if "?" in path else "?"
    url = f"{BASE}{path}{sep}token={TOKEN}&_={int(time.time() * 1000)}"
    last = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                return json.loads(r.read())
        except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError) as e:
            last = e
            time.sleep(0.4 * (2 ** i))
    if last is None:
        raise RuntimeError("fetch failed without exception (impossible)")
    raise last


def main():
    ports = fetch("/api/portfolios")
    ids = list(ports["data"].keys())
    bundle = {
        "portfolios": ports["data"],
        "infos": {},
        "positions": {},
        "profit_charts": {},
        "generated_at": int(time.time()),
    }
    for pid in ids:
        bundle["infos"][pid] = fetch(f"/api/portfolio-info?portfolio_id={pid}")["data"]
        bundle["positions"][pid] = fetch(f"/api/portfolio-position?portfolio_id={pid}")["data"]
        chart = fetch(f"/api/profit-chart?portfolio_id={pid}")
        try:
            bundle["profit_charts"][pid] = chart["data"][0]["indexItems"][0]["item"][:200]
        except Exception:
            bundle["profit_charts"][pid] = []
        time.sleep(0.15)
    out = os.path.join(os.path.dirname(__file__), "..", "data", "snapshot.json")
    out = os.path.abspath(out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {out}: {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()