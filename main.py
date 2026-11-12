from psychopy import session, visual, core, gui, data
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

dlg = gui.Dlg(title='Battery')
dlg.addField('participant:', '01')
dlg.addField('session:', '1')
ok = dlg.show()
if not dlg.OK:
    core.quit()

info = {
    'participant': ok[0],
    'session': ok[1],
    'date': data.getDateStr(),
    'expName': 'battery',
    'psychopyVersion': '2026.1.3',
}

win = visual.Window(size=(1920, 1080), fullscr=False, units='height',
                    color=[0, 0, 0], screen=0)

sess = session.Session(
    root=ROOT,
    win=win,
    experiments={
        'corsi': 'corsi/3rdtask.psyexp',
        'math':  'math_task/math_task.psyexp',
    })

# порядок чередуем по чётности номера участника
order = ['corsi', 'math'] if int(info['participant']) % 2 else ['math', 'corsi']

for name in order:
    sess.runExperiment(name, expInfo=info)

win.close()
core.quit()