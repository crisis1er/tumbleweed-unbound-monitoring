# Changelog — tumbleweed-unbound-monitoring

---

## [1.0] — 2026-04-25

### Added
- `alloy/pipelines.alloy` — 4 Alloy pipeline fragments for Unbound:
  - `loki.source.file "unbound"` → job="unbound" (all raw lines, panels 30/31/32)
  - `loki.process "unbound_local_replies"` → job="unbound_local" (cache hits + blocked, no Quad9, panel 34)
  - `loki.process "unbound_quad9_replies"` → job="unbound_quad9" (Quad9 server label, panel 35)
  - `loki.source.file "unbound_cache_hits_source"` → job="unbound_cache_hits" (enriched cache hits, panel 35)
- `grafana/unbound-full-v1.json` — Grafana dashboard v78 (34 panels)
  - Stat panels: status, uptime, latency avg/median, cache hit rate, DNSSEC
  - Timeseries: NXDOMAIN / SERVFAIL increase([12h]) with alert thresholds
  - Stat alerts: Bogus DNSSEC + suspicious activity increase([12h]), green=0 / red≥1
  - Live logs: blocked domains, DNS errors, Quad9 upstream, local resolutions, enriched cache hits
  - Bargauge: Quad9 server distribution (IPv4/IPv6)
- `prometheus/unbound-targets.yml` — Prometheus scrape target for unbound_exporter (:9167)
- `scripts/unbound-cache-watcher.py` — Python tail daemon enriching cache hits with resolved IPs
  - At startup: reads `unbound-control dump_cache` to build IP dictionary
  - Continuously tails `/var/log/unbound.log`: ANSWER SECTION → updates dict, cache hit → writes enriched line
  - Output: `YYYY-MM-DD HH:MM:SS  client_ip  domain  [rtype]  resolved_ip1, resolved_ip2`
  - Blocked domains naturally excluded (no ANSWER SECTION for local-zone redirect)
- `scripts/unbound-cache-watcher.service` — systemd unit for the cache watcher daemon
- DEC-010 documentation: LICENSE (GPL-3.0), README, SECURITY, SUPPORT, CONTRIBUTING, CODE_OF_CONDUCT, MAINTAINERS, .gitignore

### Requirements
- openSUSE Tumbleweed
- Unbound DNS resolver with `verbosity: 4` (required for ANSWER SECTION lines)
- unbound_exporter, Grafana Alloy v1.12+, Loki, Grafana, Prometheus
- Python 3, `unbound-control` (included with Unbound)
