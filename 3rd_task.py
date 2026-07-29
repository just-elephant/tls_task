#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Color-recall (Zhang & Luck). Стрелка -> сторона для запоминания.
Interference: отвлекатели цветные. Non-interference: серые.
Клик по кругу на фазе теста = ответ.
"""

import random
import colorsys
import numpy as np
from psychopy import visual, core, event, data, gui

FULLSCREEN = False
BG = [0, 0, 0]
FG = "black"

SET_SIZE = 4
SQUARE = 0.06
N_TRIALS = 24
HIT_THRESHOLD = 30      # |ошибка| < этого => считаем попаданием

T_FIX = 0.5
T_CUE = 0.5
T_ARRAY = 0.5
T_DELAY = 1.0
T_ITI = 0.3

USE_PARALLEL = False
PARALLEL_ADDR = 0x0378
port = None
if USE_PARALLEL:
    try:
        from psychopy import parallel
        port = parallel.ParallelPort(address=PARALLEL_ADDR)
    except Exception as e:
        print("Порт недоступен:", e)

def trig(code, label=""):
    if port is not None:
        port.setData(code); core.wait(0.002); port.setData(0)
    print(f"  [trigger {code:>3}] {label}")


def hue_to_psychopy(hue_deg):
    r, g, b = colorsys.hsv_to_rgb((hue_deg % 360) / 360.0, 1.0, 1.0)
    return [r*2-1, g*2-1, b*2-1]

def make_wheel_image(size=512, inner=0.72, outer=1.0):
    lut = np.array([hue_to_psychopy(h) for h in range(360)])
    ax = np.linspace(-1, 1, size)
    xx, yy = np.meshgrid(ax, -ax)
    r = np.hypot(xx, yy)
    theta = (np.degrees(np.arctan2(yy, xx)).astype(int)) % 360
    ring = (r >= inner) & (r <= outer)
    return np.where(ring[..., None], lut[theta], 0.0)

def angular_error(reported, target):
    return (reported - target + 180) % 360 - 180

def mouse_to_hue(mx, my):
    return np.degrees(np.arctan2(my, mx)) % 360


info = {"participant": "01", "session": "1"}
if not gui.DlgFromDict(info, title="Color recall").OK:
    core.quit()

win = visual.Window(fullscr=True, color=BG, units="height", allowGUI=False) \
      if FULLSCREEN else \
      visual.Window(size=(900, 900), color=BG, units="height")

def make_text(t="", height=0.05, pos=(0, 0), color=FG):
    return visual.TextStim(win, text=t, height=height, pos=pos, color=color,
                           alignText="center", wrapWidth=1.4)

fixation = make_text("+", 0.05)
arrow = make_text("", 0.08, (0, 0.08))
title_stim = make_text("", 0.07, (0, 0.3))
body_stim = make_text("", 0.045, (0, 0))
footer_stim = make_text("", 0.04, (0, -0.35))

wheel = visual.ImageStim(win, image=make_wheel_image(512), size=(0.9, 0.9))
square = visual.Rect(win, width=SQUARE, height=SQUARE, units="height", lineColor=None)
outline = visual.Rect(win, width=SQUARE, height=SQUARE, units="height",
                      fillColor=None, lineColor="black", lineWidth=2)
mouse = event.Mouse(win=win)


def screen(title, body, footer):
    title_stim.text, body_stim.text, footer_stim.text = title, body, footer
    title_stim.draw(); body_stim.draw(); footer_stim.draw()
    win.flip()
    if "escape" in event.waitKeys(keyList=["space", "escape"]):
        win.close(); core.quit()

def blank(seconds=0.0):
    """Чистый кадр — гасит всё, что оставалось на экране."""
    win.flip()
    if seconds:
        core.wait(seconds)

def wait_for(seconds, draw_fn):
    clock = core.Clock()
    while clock.getTime() < seconds:
        draw_fn()
        win.flip()
        if event.getKeys(keyList=["escape"]):
            win.close(); core.quit()

def random_positions(n, side, xmin=0.12, xmax=0.42, ymax=0.32, gap=0.09):
    sign = 1 if side == "R" else -1
    for _ in range(20):
        pts, tries = [], 0
        while len(pts) < n and tries < 500:
            x = sign * random.uniform(xmin, xmax)
            y = random.uniform(-ymax, ymax)
            if all((x - px)**2 + (y - py)**2 > gap**2 for px, py in pts):
                pts.append((x, y))
            tries += 1
        if len(pts) == n:
            return pts
        gap *= 0.85
    return pts


def build_trials(n):
    trials = []
    for i in range(n):
        interference = i < n // 2
        cue_side = random.choice(["L", "R"])
        other = "R" if cue_side == "L" else "L"
        trials.append(dict(
            interference=interference,
            cue_side=cue_side,
            target_hues=random.sample(range(0, 360, 10), SET_SIZE),
            distr_hues=random.sample(range(0, 360, 10), SET_SIZE),
            target_pos=random_positions(SET_SIZE, cue_side),
            distr_pos=random_positions(SET_SIZE, other),
            probe=random.randrange(SET_SIZE)))
    random.shuffle(trials)
    return trials


def report_phase(tr):
    probe = tr["probe"]
    target_hue = tr["target_hues"][probe]
    clock = core.Clock()

    while mouse.getPressed()[0]:    # ждём отпускания с прошлой пробы
        core.wait(0.01)
    mouse.clickReset()

    while True:
        wheel.draw()
        mx, my = mouse.getPos()
        on_wheel = mx**2 + my**2 > 0.30**2
        for j, pos in enumerate(tr["target_pos"]):
            if j == probe and on_wheel:
                square.fillColor = hue_to_psychopy(mouse_to_hue(mx, my))
                square.pos = pos
                square.draw()
            outline.pos = pos
            outline.lineWidth = 6 if j == probe else 2
            outline.draw()
        fixation.draw()
        win.flip()

        if event.getKeys(keyList=["escape"]):
            win.close(); core.quit()
        if mouse.getPressed()[0] and on_wheel:
            rt = clock.getTime()
            reported = mouse_to_hue(mx, my)
            blank()                 # сразу гасим круг и рамки
            while mouse.getPressed()[0]:
                core.wait(0.01)
            return reported, angular_error(reported, target_hue), rt


exp = data.ExperimentHandler(dataFileName=f"colorrecall_{info['participant']}")
trials = build_trials(N_TRIALS)

screen("COLOR RECALL",
       "Стрелка покажет, какую сторону запоминать.\n"
       "Запомни цвета ВСЕХ квадратов на этой стороне.\n"
       "Потом один квадрат подсветится — кликни его цвет на круге.",
       "ПРОБЕЛ — начать")

trig(200, "experiment_start")
errors, hits = [], []

print(f"\n{'#':>3} {'усл.':<14} {'стор.':>5} {'ошибка,°':>9} {'RT':>5}  итог")
print("-" * 50)

for t, tr in enumerate(trials):
    cond = "interference" if tr["interference"] else "non-interf"

    blank()
    wait_for(T_FIX, lambda: fixation.draw())

    arrow.text = "\u2192" if tr["cue_side"] == "R" else "\u2190"
    def draw_cue():
        fixation.draw(); arrow.draw()
    trig(10, f"cue_t{t}")
    wait_for(T_CUE, draw_cue)

    def draw_array():
        fixation.draw()
        for hue, pos in zip(tr["target_hues"], tr["target_pos"]):
            square.fillColor = hue_to_psychopy(hue)
            square.pos = pos
            square.draw()
        for hue, pos in zip(tr["distr_hues"], tr["distr_pos"]):
            square.fillColor = hue_to_psychopy(hue) if tr["interference"] else [-0.1, -0.1, -0.1]
            square.pos = pos
            square.draw()
    trig(20, f"array_t{t}_{cond}")
    wait_for(T_ARRAY, draw_array)

    blank()
    trig(30, f"delay_t{t}")
    wait_for(T_DELAY, lambda: fixation.draw())

    trig(40, f"test_t{t}")
    reported, err, rt = report_phase(tr)
    trig(50, f"response_t{t}")
    blank(T_ITI)

    hit = abs(err) < HIT_THRESHOLD
    errors.append(abs(err)); hits.append(hit)
    mark = "OK  " if hit else "MISS"
    print(f"{t:>3} {cond:<14} {tr['cue_side']:>5} {err:>+9.1f} {rt:>5.2f}  {mark}")

    exp.addData("trial", t)
    exp.addData("condition", cond)
    exp.addData("cue_side", tr["cue_side"])
    exp.addData("set_size", SET_SIZE)
    exp.addData("target_hue", tr["target_hues"][tr["probe"]])
    exp.addData("reported_hue", round(reported, 1))
    exp.addData("error_deg", round(err, 1))
    exp.addData("abs_error", round(abs(err), 1))
    exp.addData("correct", int(hit))
    exp.addData("rt", round(rt, 3))
    exp.nextEntry()

trig(201, "experiment_end")


def mean(xs): return sum(xs) / len(xs) if xs else 0

def split(key):
    rows = [e for e in exp.entries if e["condition"] == key]
    return [abs(e["error_deg"]) for e in rows], [e["correct"] for e in rows]

int_err, int_hit = split("interference")
non_err, non_hit = split("non-interf")

print("-" * 50)
print(f"Средняя |ошибка|: {mean(errors):.1f}°   попаданий: {100*mean(hits):.0f}%")
print(f"  interference:     {mean(int_err):>5.1f}°   {100*mean(int_hit):>3.0f}%")
print(f"  non-interference: {mean(non_err):>5.1f}°   {100*mean(non_hit):>3.0f}%")

screen("Готово",
       f"Попаданий: {100*mean(hits):.0f}%   ошибка {mean(errors):.0f}°\n"
       f"Interference: {mean(int_err):.0f}° / {100*mean(int_hit):.0f}%\n"
       f"Non-interference: {mean(non_err):.0f}° / {100*mean(non_hit):.0f}%",
       "ПРОБЕЛ — выход")

win.close()
core.quit()