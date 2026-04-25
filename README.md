# tumbleweed-unbound-monitoring

> Unbound DNS resolver monitoring for openSUSE Tumbleweed

Prometheus metrics, Loki log pipelines, Grafana dashboard, and a cache enrichment script for Unbound DNS.

---

## What is monitored

| Signal | Source | Tool |
|---|---|---|
| DNS query rates, cache hit/miss, DNSSEC, SERVFAIL, NXDOMAIN | unbound_exporter (:9167) | Prometheus |
| Blocked domains (OISD/custom-blocks) | `/var/log/unbound.log` | Loki / Alloy |
| DNS errors (NXDOMAIN, SERVFAIL, REFUSED) | `/var/log/unbound.log` | Loki / Alloy |
| Upstream Quad9 resolutions | `/var/log/unbound.log` | Loki / Alloy |
| Cache hits with resolved IPs | `/var/log/unbound_cache_hits.log` | Loki / Alloy |
| Quad9 server used (IPv4/IPv6) | `/var/log/unbound.log` | Loki / Alloy |

---

## Contents

```
tumbleweed-unbound-monitoring/
├── alloy/
│   └── pipelines.alloy          # Alloy pipeline fragments for Unbound
├── grafana/
│   └── unbound-full-v1.json     # Grafana dashboard export
├── scripts/
│   ├── unbound-cache-watcher.py # Cache hit enrichment script
│   └── unbound-cache-watcher.service  # systemd unit
├── prometheus/
│   └── unbound-targets.yml      # Prometheus scrape target
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── MAINTAINERS
├── README.md
├── RELEASE
├── SECURITY.md
└── SUPPORT.md
```

---

## Alloy pipelines

| Job (Loki) | Source | Content |
|---|---|---|
| `unbound` | `/var/log/unbound.log` | All raw lines — used by panels blocked/errors/upstream |
| `unbound_local` | `/var/log/unbound.log` | `reply:` with latency=0 only (cache hits + blocked, no Quad9) |
| `unbound_quad9` | `/var/log/unbound.log` | `info: reply from <.>` only — label `quad9_server` |
| `unbound_cache_hits` | `/var/log/unbound_cache_hits.log` | Cache hits enriched with resolved IPs (from script) |

---

## unbound-cache-watcher.py

A Python tail daemon that enriches cache hit log lines with resolved IPs:

1. At startup: reads `unbound-control dump_cache` to populate an IP dictionary
2. Continuously tails `/var/log/unbound.log`:
   - ANSWER SECTION lines (verbosity 4, no timestamp) → updates the dictionary
   - Cache hit lines → writes enriched entry to `/var/log/unbound_cache_hits.log`
3. Output format: `YYYY-MM-DD HH:MM:SS  client_ip  domain  [rtype]  resolved_ip1, resolved_ip2`

**Requirement**: `verbosity: 4` in `unbound.conf` (for ANSWER SECTION lines).

---

## Grafana dashboard — unbound-full-v1

Key panels:

| Panel | Type | Content |
|---|---|---|
| Statut / Uptime | stat | Unbound service health |
| NXDOMAIN / SERVFAIL | timeseries | increase([12h]), alert thresholds |
| Réponses Bogus DNSSEC | stat | increase([12h]), green=0 / red≥1 |
| Activité suspecte | stat | unwanted queries increase([12h]) |
| Live Bloqués | logs | Blocked domains (OISD + custom) |
| Live erreurs DNS | logs | NXDOMAIN, SERVFAIL, REFUSED with client IP |
| Live résolutions upstream | logs | Quad9 upstream resolutions |
| Live résolutions locales | logs | Cache hits + blocked (without Quad9) |
| Cache hits — IPs résolues | logs | Enriched cache hits with resolved IPs |
| Serveurs Quad9 utilisés | bargauge | IPv4/IPv6 Quad9 server distribution |

---

## Requirements

- openSUSE Tumbleweed
- Unbound DNS resolver (`zypper in unbound`)
- unbound_exporter
- Grafana Alloy v1.12+
- Loki, Grafana
- Python 3 (for cache watcher script)
- `unbound-control` (included with Unbound)

## License

GNU General Public License v3.0 — see [LICENSE](./LICENSE)
