#!/usr/bin/env python3
"""Flip the public profile between network and tech stack every calendar day in IST.

Creates assets/showcase.svg, and changes the README asset URL each day to
avoid GitHub's image proxy serving an old cached version of the SVG.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime
from pathlib import Path
import re
import shutil
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
ANCHOR = date(2026, 11, 11)  # Day 0: network. Day 1: stack. Repeat.


def mode_for(day: date) -> str:
    return 'network' if (day - ANCHOR).days % 2 == 0 else 'stack'


def update(day: date):
    mode = mode_for(day)
    source = ROOT / 'assets' / f'{mode}.svg'
    if not source.is_file():
        raise FileNotFoundError(source)
    dest = ROOT / 'assets' / 'showcase.svg'
    if not dest.exists() or dest.read_bytes() != source.read_bytes():
        shutil.copyfile(source, dest)

    readme = ROOT / 'README.md'
    if not readme.is_file():
        raise FileNotFoundError(readme)
    original = readme.read_text(encoding='utf-8')
    pattern = r'(https://raw\.githubusercontent\.com/jkjitendra/jkjitendra/main/assets/showcase\.svg\?v=)(\d{4}-\d{2}-\d{2})'
    updated, count = re.subn(pattern,lambda m: m.group(1)+day.isoformat(), original)
    if count != 1:
        raise ValueError(f'Expected exactly one showcase image URL in README; found {count}')
    if original != updated:
        readme.write_text(updated, encoding='utf-8')
    print(f'{day.isoformat()} ({ZoneInfo("Asia/Kolkata")}) -> {mode} | Updated: {original != updated}')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--date', type=date.fromisoformat, help='Preview or render for YYYY-MM-DD; otherwise today in IST')
    args=parser.parse_args()
    update(args.date or datetime.now(ZoneInfo('Asia/Kolkata')).date())


if __name__ == '__main__':
    main()
