#!/usr/bin/env python3
import subprocess, re, time, sys
from datetime import datetime
from collections import defaultdict

LOG_FILE    = "/var/log/unbound.log"
OUTPUT_FILE = "/var/log/unbound_cache_hits.log"

# (domain, rtype) -> set of IPs
domain_ips = defaultdict(set)

def load_initial_cache():
    try:
        r = subprocess.run(
            ["/usr/sbin/unbound-control", "dump_cache"],
            capture_output=True, text=True, timeout=15
        )
        count = 0
        for line in r.stdout.splitlines():
            m = re.match(r'^(\S+)\s+\d+\s+IN\s+(A|AAAA)\s+(\S+)$', line)
            if m:
                domain = m.group(1).rstrip('.').lower()
                domain_ips[(domain, m.group(2))].add(m.group(3))
                count += 1
        print(f"[startup] {count} entrées A/AAAA chargées depuis le cache", file=sys.stderr, flush=True)
    except Exception as e:
        print(f"[warning] dump_cache initial échoué : {e}", file=sys.stderr, flush=True)

ANSWER_RE = re.compile(r'^(\S+)\s+\d+\s+IN\s+(A|AAAA)\s+(\S+)$')
CACHE_HIT_RE = re.compile(
    r'\] reply: (\S+) (\S+) (A|AAAA) IN NOERROR 0\.000000 1 \d+'
)

def main():
    load_initial_cache()
    with open(OUTPUT_FILE, 'a', buffering=1) as out:
        with open(LOG_FILE, 'r') as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.05)
                    continue
                line = line.rstrip('\n')

                # ANSWER SECTION line (no timestamp) — Quad9 upstream resolution
                m = ANSWER_RE.match(line)
                if m:
                    domain = m.group(1).rstrip('.').lower()
                    domain_ips[(domain, m.group(2))].add(m.group(3))
                    continue

                # Cache hit line
                m = CACHE_HIT_RE.search(line)
                if m:
                    client_ip = m.group(1)
                    domain    = m.group(2).rstrip('.').lower()
                    rtype     = m.group(3)
                    key       = (domain, rtype)
                    if key in domain_ips:
                        ts  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        ips = ', '.join(sorted(domain_ips[key]))
                        out.write(f"{ts}  {client_ip}  {domain}  [{rtype}]  {ips}\n")

if __name__ == '__main__':
    main()
