# Contributing to tumbleweed-unbound-monitoring

Thank you for your interest in contributing to this project.

## Prerequisites

- openSUSE Tumbleweed (rolling release)
- Unbound DNS resolver (`zypper in unbound`)
- unbound_exporter, Alloy, Loki, Grafana
- Git configured with GPG signing enabled
- Basic knowledge of Prometheus, Grafana, and monitoring concepts

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Validate Alloy config: `alloy fmt /etc/alloy/config.alloy`
Test Unbound: `unbound-checkconf /etc/unbound/unbound.conf`
5. Commit with Conventional Commits format:
   - `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`
6. Push and open a Pull Request

## Commit Style

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`

GPG signing is required on all commits.

## Reporting Bugs

Open a GitHub Issue with:
- Description of the problem
- Your openSUSE Tumbleweed version (`cat /etc/os-release`)
- Relevant config files and logs
