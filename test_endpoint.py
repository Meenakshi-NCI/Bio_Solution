# A test script that hits the /predict endpoint with payloads of increasing size.

import json
import random
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8080/predict"


def generate_readings(count: int, humidity_range: tuple[float, float] = (30.0, 100.0)) -> list[dict]:
    """Generate `count` fake weather readings with a configurable humidity range."""
    base_time = datetime(2024, 6, 1)
    readings = []
    for i in range(count):
        readings.append({
            "timestamp": (base_time + timedelta(hours=i)).isoformat() + "Z",
            "temperature": round(random.uniform(5.0, 35.0), 1),
            "humidity":    round(random.uniform(*humidity_range), 1),
            "pressure":    round(random.uniform(980.0, 1040.0), 2),
            "wind_speed":  round(random.uniform(0.0, 60.0), 1),
        })
    return readings


def run_test(name: str, readings: list[dict]) -> bool:
    """Send a prediction request. Returns True if the server appears to have crashed."""
    print(f"\n  {name}")

    body = json.dumps({"readings": readings}).encode()
    req = urllib.request.Request(BASE_URL, data=body, headers={"Content-Type": "application/json"}, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"  Status : {resp.status}")
            print(f"  Body   : {json.dumps(json.loads(resp.read()), indent=4)}")
            return False
    except urllib.error.URLError as exc:
        print(f"  [FAIL] Connection error — server may have crashed!")
        print(f"         {exc}")
        return True
    except TimeoutError:
        print(f"  [FAIL] Request timed out after 15 s")
        return False
    except Exception as exc:
        print(f"  [FAIL] Unexpected error: {exc}")
        return False


# Dataset sizes to cycle through — small ones succeed, large ones will crash the container.
SIZES = [50, 100, 300, 500, 1000, 2000, 4000, 5000]
TIMEOUT_S = 60

if __name__ == "__main__":
    deadline = time.time() + TIMEOUT_S
    iteration = 0

    print(f"Running random tests until the container crashes (timeout: {TIMEOUT_S}s)...")

    while time.time() < deadline:
        iteration += 1
        count = random.choice(SIZES)
        h_low  = random.uniform(30.0, 60.0)
        h_high = random.uniform(61.0, 100.0)

        crashed = run_test(
            f"Iteration {iteration} — {count} readings  (humidity {h_low:.0f}-{h_high:.0f}%)",
            generate_readings(count, humidity_range=(h_low, h_high)),
        )

        if crashed:
            print("\n[!] Container has crashed. Test complete.")
            break

        time.sleep(random.uniform(0.5, 1.5))
    else:
        print("\n[!] Timeout reached without a crash — something may already be wrong.")
