#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generates corsi_conditions.csv for the Builder version of the Corsi task.

Fixed ladder: 2 trials per sequence length 2..7 = 12 trials, identical
for every participant (so trial counts per load level are balanced for EEG).

Columns:
  sequence   block indices, e.g. "3-7-1-9"
  span       sequence length
  trig_delay trigger code for retention onset (30)
"""
import csv
import random

SEED = 1
LENGTHS = [2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7]
N_BLOCKS = 9

random.seed(SEED)


def make_sequence(n):
    """Random sequence of n distinct blocks, no immediate repeats."""
    return random.sample(range(1, N_BLOCKS + 1), n)


rows = []
for span in LENGTHS:
    seq = make_sequence(span)
    rows.append(dict(
        sequence="-".join(str(x) for x in seq),
        span=span,
        trig_delay=30,
    ))

with open("corsi_conditions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

print(f"corsi_conditions.csv: {len(rows)} trials, spans {sorted(set(LENGTHS))}, seed={SEED}")
for r in rows:
    print(f"  span {r['span']}: {r['sequence']}")