#!/usr/bin/env python3
# coding: utf-8


def parse_percent(s: str) -> float:
    if not s[-1] == '%':
        return 0.0
    return float(s[0:-1])
