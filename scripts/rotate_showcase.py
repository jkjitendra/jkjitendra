#!/usr/bin/env python3
"""Alternate the animated network and terminal, using the Asia/Kolkata calendar.

On network days the profile terminal is also shown below featured projects.
On terminal days it appears only as the main showcase, avoiding duplicates.
Assets are checked in; the scheduled workflow selects the active image and
updates its cache-busting URL to encourage GitHub to display the latest version.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import shutil
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = date(2026, 11, 11)  # Day 0 network, day 1 terminal, repeat.
TERMINAL_START = '<!-- STATIC_TERMINAL_START -->'
TERMINAL_END = '<!-- STATIC_TERMINAL_END -->'
TERMINAL_BELOW_PROJECTS = '''### 💻 Who's behind the code?

<p align="center">
  <img src="https://raw.githubusercontent.com/jkjitendra/jkjitendra/main/assets/terminal.svg" width="100%" alt="Terminal profile with Jitendra's custom JK logo, experience, and engineering highlights" />
</p>
'''


def mode_for(day: date) -> str:
    return 'network' if (day - ANCHOR).days % 2 == 0 else 'terminal'


def update(day: date) -> None:
    mode = mode_for(day)
    source = ROOT / 'assets' / f'{mode}.svg'
    if not source.is_file():
        raise FileNotFoundError(source)
    dest = ROOT / 'assets' / 'showcase.svg'
    if not dest.exists() or dest.read_bytes() != source.read_bytes():
        shutil.copyfile(source, dest)

    readme = ROOT / 'README.md'
    original = readme.read_text(encoding='utf-8')
    url_pattern = r'(https://raw\.githubusercontent\.com/jkjitendra/jkjitendra/main/assets/showcase\.svg\?v=)(\d{4}-\d{2}-\d{2})'
    updated, count = re.subn(url_pattern, lambda m: m.group(1) + day.isoformat(), original)
    if count != 1:
        raise ValueError(f'Expected one dated showcase image URL, found {count}')

    marker_pattern = re.compile(re.escape(TERMINAL_START) + r'.*?' + re.escape(TERMINAL_END), re.DOTALL)
    content = TERMINAL_BELOW_PROJECTS if mode == 'network' else ''
    replacement = f'{TERMINAL_START}\n{content}{TERMINAL_END}'
    updated, count = marker_pattern.subn(lambda _: replacement, updated)
    if count != 1:
        raise ValueError('Missing or duplicate static terminal section markers in README')

    updated = re.sub(
        r'<!-- Daily showcase: .*? -->',
        '<!-- Daily showcase: network on even days since 2026-11-11; terminal on odd days. -->',
        updated,
        count=1,
    )
    updated = updated.replace(
        'Animated JK project constellation and engineering stack, rotating on alternate days',
        'Animated JK project constellation and terminal profile, rotating on alternate days',
    ).replace(
        'Network signals ↔ tech stack · automatically alternates each day',
        'Project network ↔ developer terminal · automatically alternates each day',
    )

    if original != updated:
        readme.write_text(updated, encoding='utf-8')
    print(f'{day.isoformat()} (Asia/Kolkata) -> {mode}; README changed: {original != updated}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', type=date.fromisoformat, help='Render a YYYY-MM-DD date (default: today in IST)')
    args = parser.parse_args()
    update(args.date or datetime.now(ZoneInfo('Asia/Kolkata')).date())


if __name__ == '__main__':
    main()
