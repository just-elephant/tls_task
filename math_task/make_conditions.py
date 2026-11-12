#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Генерирует conditions.csv для Builder-версии operation span.
Уравнения из трёх членов, результат 1..9.

Колонки:
  equation        текст уравнения
  eq_form         тип уравнения (для анализа по сложности)
  true_result     верный ответ (1-9)
  shown_result    что показывается синим
  is_match        1 = shown совпадает с true
  corrAns         'right' (совпадает) / 'left' (не совпадает)
  dist            |shown - true|, для match равен 0
  trig_eq         код метки на онсет уравнения
  trig_probe      код метки на онсет пробы (41 match / 42 mismatch)
"""
import csv
import random
from collections import defaultdict, deque

N_TRIALS = 40
SEED = 1

# Насколько далеко дистрактор может отстоять от верного ответа.
# Держи узко: при разнице 4+ ответ отвергается по грубой прикидке,
# без реального вычисления, и проба перестаёт мерить то, что нужно.
DIST_MIN, DIST_MAX = 1, 3

# Раскладка ответа. right = «совпадает», left = «не совпадает».
KEY_MATCH = "right"
KEY_MISMATCH = "left"

# Коды меток
TRIG_EQ = 31               # онсет уравнения
TRIG_PROBE_MATCH = 32      # онсет пробы, совпадение
TRIG_PROBE_MISMATCH = 33   # онсет пробы, несовпадение

random.seed(SEED)


# --- формы уравнений -------------------------------------------------
# Множители от 3: с двойкой проба решается узнаванием, а не счётом.
# Все промежуточные значения положительные, деление только нацело.

def form_mul_add_sub():
    """a*b+c-d"""
    out = []
    for a in range(3, 10):
        for b in range(3, 10):
            for c in range(2, 10):
                d = a * b + c
                for r in range(1, 10):
                    if 2 <= d - r <= 99:
                        out.append((f"{a}*{b}+{c}-{d - r}", r))
    return out


def form_sum_mul_sub():
    """(a+b)*c-d"""
    out = []
    for a in range(2, 10):
        for b in range(2, 10):
            for c in range(3, 10):
                base = (a + b) * c
                for r in range(1, 10):
                    if 2 <= base - r <= 99:
                        out.append((f"({a}+{b})*{c}-{base - r}", r))
    return out


def form_div_add_sub():
    """a*b/c+d  — деление нацело"""
    out = []
    for a in range(3, 10):
        for b in range(3, 10):
            for c in range(2, 10):
                if (a * b) % c:
                    continue
                q = a * b // c
                for d in range(2, 10):
                    r = q + d
                    if 1 <= r <= 9 and q >= 2:
                        out.append((f"{a}*{b}/{c}+{d}", r))
                for d in range(2, 10):
                    r = q - d
                    if 1 <= r <= 9:
                        out.append((f"{a}*{b}/{c}-{d}", r))
    return out


def form_mul_mul_sub():
    """a*b-c*d"""
    out = []
    for a in range(3, 10):
        for b in range(3, 10):
            for c in range(2, 10):
                for d in range(2, 10):
                    r = a * b - c * d
                    if 1 <= r <= 9 and c * d >= 6:
                        out.append((f"{a}*{b}-{c}*{d}", r))
    return out


FORMS = {
    'mul_add_sub': form_mul_add_sub,
    'sum_mul_sub': form_sum_mul_sub,
    'div_add_sub': form_div_add_sub,
    'mul_mul_sub': form_mul_mul_sub,
}


def build_pool():
    """{(результат, форма): [уравнения]}"""
    pool = defaultdict(list)
    for name, fn in FORMS.items():
        for eq, r in fn():
            pool[(r, name)].append(eq)
    return pool


def pick_distractor(true_res):
    opts = [d for d in range(1, 10)
            if d != true_res and DIST_MIN <= abs(d - true_res) <= DIST_MAX]
    return random.choice(opts)


pool = build_pool()
results = list(range(1, 10))
form_names = list(FORMS)

# Результаты раскладываем поровну, чтобы сложность не съехала в одно условие
picks = []
while len(picks) < N_TRIALS:
    batch = results[:]
    random.shuffle(batch)
    picks.extend(batch)
picks = picks[:N_TRIALS]

# Формы тоже по кругу — иначе одна форма может занять половину проб
form_cycle = deque(form_names * (N_TRIALS // len(form_names) + 1))
random.shuffle(form_cycle)

# Ровно половина match, назначаем ПОСЛЕ выбора уравнений — тогда
# match и mismatch получают одинаковый набор задач по трудности
flags = [1] * (N_TRIALS // 2) + [0] * (N_TRIALS - N_TRIALS // 2)
random.shuffle(flags)

used = set()
rows = []

for true_res, is_match in zip(picks, flags):
    eq = None
    for _ in range(len(form_cycle)):
        form = form_cycle.popleft()
        form_cycle.append(form)
        cands = [e for e in pool[(true_res, form)] if e not in used]
        if cands:
            eq = random.choice(cands)
            break
    if eq is None:
        raise RuntimeError(f'Нет свободных уравнений для результата {true_res}')

    used.add(eq)
    shown = true_res if is_match else pick_distractor(true_res)

    rows.append(dict(
        equation=eq,
        eq_form=form,
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
by_form = defaultdict(int)
for r in rows:
    by_form[r["eq_form"]] += 1

print(f"conditions.csv: {len(rows)} проб, match {n_match}, "
      f"mismatch {len(rows)-n_match}, seed={SEED}")
print("По формам:", dict(by_form))
print(f"Ответы: {KEY_MATCH} = совпадает, {KEY_MISMATCH} = не совпадает.")
print("Порядок проб не перемешан — рандомизацией займётся петля Builder.")