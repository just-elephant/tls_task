#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Генерирует conditions.csv для Builder-версии operation span.
Уравнения вида a*b-c с результатом 1..9.

Колонки:
  equation        текст уравнения
  true_result     верный ответ (1-9)
  shown_result    что показывается синим
  is_match        1 = shown совпадает с true
  corrAns         'left' (совпадает) / 'right' (не совпадает)
  dist            |shown - true|, для match равен 0
  trig_eq         код метки на онсет уравнения
  trig_probe      код метки на онсет пробы (41 match / 42 mismatch)
"""
import csv
import random
from collections import defaultdict

N_TRIALS = 40
SEED = 1

# Насколько далеко дистрактор может отстоять от верного ответа.
# Держи узко: при разнице 4+ ответ отвергается по грубой прикидке,
# без реального вычисления, и проба перестаёт мерить то, что нужно.
DIST_MIN, DIST_MAX = 1, 3

# Раскладка ответа. left = «совпадает», right = «не совпадает».
KEY_MATCH = "left"
KEY_MISMATCH = "right"

# Коды меток
TRIG_EQ = 11          # онсет уравнения
TRIG_PROBE_MATCH = 41  # онсет пробы, совпадение
TRIG_PROBE_MISMATCH = 42  # онсет пробы, несовпадение

random.seed(SEED)


def equation_pool():
    """Все уравнения a*b-c с результатом 1..9, сгруппированы по результату."""
    pool = defaultdict(list)
    for a in range(2, 6):
        for b in range(2, 6):
            for c in range(1, 16):
                r = a * b - c
                if 1 <= r <= 9:
                    pool[r].append(f"{a}*{b}-{c}")
    return pool


def pick_distractor(true_res):
    opts = [d for d in range(1, 10)
            if d != true_res and DIST_MIN <= abs(d - true_res) <= DIST_MAX]
    return random.choice(opts)


pool = equation_pool()
results = sorted(pool)

# Результаты раскладываем поровну, чтобы сложность не съехала в одно условие
picks = []
while len(picks) < N_TRIALS:
    batch = results[:]
    random.shuffle(batch)
    picks.extend(batch)
picks = picks[:N_TRIALS]

# Ровно половина match, назначаем ПОСЛЕ выбора уравнений — тогда
# match и mismatch получают одинаковый набор задач по трудности
flags = [1] * (N_TRIALS // 2) + [0] * (N_TRIALS - N_TRIALS // 2)
random.shuffle(flags)

rows = []
for true_res, is_match in zip(picks, flags):
    eq = random.choice(pool[true_res])
    shown = true_res if is_match else pick_distractor(true_res)
    rows.append(dict(
        equation=eq,
        true_result=true_res,
        shown_result=shown,
        is_match=is_match,
        corrAns=KEY_MATCH if is_match else KEY_MISMATCH,
        dist=abs(shown - true_res),
        trig_eq=TRIG_EQ,
        trig_probe=TRIG_PROBE_MATCH if is_match else TRIG_PROBE_MISMATCH,
    ))

with open("conditions.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

n_match = sum(r["is_match"] for r in rows)
print(f"conditions.csv: {len(rows)} проб, match {n_match}, "
      f"mismatch {len(rows)-n_match}, seed={SEED}")
print(f"Ответы: {KEY_MATCH} = совпадает, {KEY_MISMATCH} = не совпадает.")
print("Порядок проб не перемешан — рандомизацией займётся петля Builder.")