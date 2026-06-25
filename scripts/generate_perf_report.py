import json
from pathlib import Path
from datetime import date

RAW_FILE = Path("reports/perf/raw.json")
report_dir = Path("reports/perf")
report_dir.mkdir(parents=True, exist_ok=True)

report_file = report_dir / f"{date.today()}.md"

def load_records():
    records = []

    with open(RAW_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            records.append(json.loads(line))

    return records


records = load_records()
durations = []

for record in records:
    if record.get("metric") == "http_req_duration":
        if record.get("type") == "Point":
            durations.append(record["data"]["value"])

durations.sort()

p50_index = int(len(durations) * 0.50)
p95_index = int(len(durations) * 0.95)

p50 = durations[p50_index]
p95 = durations[min(p95_index, len(durations) - 1)]

# errors
failed_requests = 0
total_requests = 0

for record in records:
    if record.get("metric") == "http_req_failed":
        if record.get("type") == "Point":
            total_requests += 1

            if record["data"]["value"] == 1:
                failed_requests += 1

error_rate = (
    (failed_requests / total_requests) * 100
    if total_requests
    else 0
)

TEST_DURATION_MINUTES = 3

throughput = total_requests / TEST_DURATION_MINUTES


print(f"Duration samples: {len(durations)}")
print(f"Loaded {len(records)} records")
print(f"P50: {p50:.2f} ms")
print(f"P95: {p95:.2f} ms")
print(f"Failed requests: {failed_requests}")
print(f"Total requests: {total_requests}")
print(f"Error rate: {error_rate:.2f}%")
print(f"Throughput: {throughput:.2f} req/min")


p50_pass = p50 < 4000
p95_pass = p95 < 8000
error_pass = error_rate < 2
throughput_pass = throughput >= 5

overall_pass = (
    p50_pass
    and p95_pass
    and error_pass
    and throughput_pass
)

report = f"""# AWSense Performance Report

Date: {date.today()}

| Metric | Target | Actual | Status |
|----------|----------|----------|----------|
| P50 | < 4s | {p50/1000:.2f}s | {"PASS" if p50_pass else "FAIL"} |
| P95 | < 8s | {p95/1000:.2f}s | {"PASS" if p95_pass else "FAIL"} |
| Error Rate | < 2% | {error_rate:.2f}% | {"PASS" if error_pass else "FAIL"} |
| Throughput | ≥ 5 req/min | {throughput:.2f} req/min | {"PASS" if throughput_pass else "FAIL"} |

## Overall Status

{"PASS" if overall_pass else "FAIL"}
"""

with open(report_file, "w", encoding="utf-8") as f:
    f.write(report)

print(f"Report written to: {report_file}")