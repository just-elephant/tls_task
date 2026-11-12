#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.1.3),
    on August 06, 2026, at 15:49
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.1.3'
expName = '3rdtask'  # from the Builder filename that created this script
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "welcome_routine" ---
    welcome_text = visual.TextStim(win=win, name='welcome_text',
        text='ЗАДАНИЕ НА ПРОСТРАНСТВЕННУЮ ПАМЯТЬ\n\n\nНа экране — 9 квадратов. \n\nОни будут по очереди загораться жёлтым.\n\n\nВаша задача — запомнить порядок,\nв котором они загорались.\n\n\nПосле короткой паузы кликните мышью\nпо квадратам в том же самом порядке.\n\n\nДлина последовательности будет расти.\n\nЕсли не уверены — отвечайте наугад.\n\n\nСтарайтесь не двигать головой\nи моргать между пробами, а не во время них.\n\nНажмите ПРОБЕЛ, чтобы начать.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.035, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    press_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    # Run 'Begin Experiment' code from lsl_setup
    n_correct = 0
    n_done = 0
    from psychopy import core
    expClock = core.Clock()
    TARGET = 1200.0
    
    class _Dummy:
        def push_sample(self, x): pass
    outlet = _Dummy()
    
    # --- Initialize components for Routine "corsi_show" ---
    blk1 = visual.Rect(
        win=win, name='blk1',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.30, 0.28), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    blk2 = visual.Rect(
        win=win, name='blk2',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.10, 0.36), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    blk3 = visual.Rect(
        win=win, name='blk3',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.36, 0.20), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    blk4 = visual.Rect(
        win=win, name='blk4',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.42, 0.05), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    blk5 = visual.Rect(
        win=win, name='blk5',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.08, 0.10), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-4.0, interpolate=True)
    blk6 = visual.Rect(
        win=win, name='blk6',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.28, -0.02), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    blk7 = visual.Rect(
        win=win, name='blk7',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.34, -0.20), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-6.0, interpolate=True)
    blk8 = visual.Rect(
        win=win, name='blk8',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.02, -0.28), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-7.0, interpolate=True)
    blk9 = visual.Rect(
        win=win, name='blk9',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.40, -0.32), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-8.0, interpolate=True)
    
    # --- Initialize components for Routine "corsi_delay" ---
    fix = visual.TextStim(win=win, name='fix',
        text='+ ',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    # Run 'Begin Experiment' code from mark_delay_2
    win.callOnFlip(outlet.push_sample, ['30'])
    
    # --- Initialize components for Routine "corsi_resp" ---
    rblk1 = visual.Rect(
        win=win, name='rblk1',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.30, 0.28), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=0.0, interpolate=True)
    rblk2 = visual.Rect(
        win=win, name='rblk2',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.10, 0.36), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    rblk3 = visual.Rect(
        win=win, name='rblk3',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.36, 0.20), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    rblk4 = visual.Rect(
        win=win, name='rblk4',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.42, 0.05), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    rblk5 = visual.Rect(
        win=win, name='rblk5',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.08, 0.10), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-4.0, interpolate=True)
    rblk6 = visual.Rect(
        win=win, name='rblk6',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.28, -0.02), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    rblk7 = visual.Rect(
        win=win, name='rblk7',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(-0.34, -0.20), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-6.0, interpolate=True)
    rblk8 = visual.Rect(
        win=win, name='rblk8',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.02, -0.28), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-7.0, interpolate=True)
    rblk9 = visual.Rect(
        win=win, name='rblk9',
        width=(0.09, 0.09)[0], height=(0.09, 0.09)[1],
        ori=0.0, pos=(0.40, -0.32), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-8.0, interpolate=True)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "iti" ---
    text = visual.TextStim(win=win, name='text',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.06, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "goodbye" ---
    bye_text = visual.TextStim(win=win, name='bye_text',
        text='Задание завершено.\n\n\nСпасибо!',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "welcome_routine" ---
    # create an object to store info about Routine welcome_routine
    welcome_routine = data.Routine(
        name='welcome_routine',
        components=[welcome_text, press_resp],
    )
    welcome_routine.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for press_resp
    press_resp.keys = []
    press_resp.rt = []
    _press_resp_allKeys = []
    # store start times for welcome_routine
    welcome_routine.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    welcome_routine.tStart = globalClock.getTime(format='float')
    welcome_routine.status = STARTED
    thisExp.addData('welcome_routine.started', welcome_routine.tStart)
    welcome_routine.maxDuration = None
    # keep track of which components have finished
    welcome_routineComponents = welcome_routine.components
    for thisComponent in welcome_routine.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "welcome_routine" ---
    thisExp.currentRoutine = welcome_routine
    welcome_routine.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *welcome_text* updates
        
        # if welcome_text is starting this frame...
        if welcome_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            welcome_text.frameNStart = frameN  # exact frame index
            welcome_text.tStart = t  # local t and not account for scr refresh
            welcome_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcome_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcome_text.started')
            # update status
            welcome_text.status = STARTED
            welcome_text.setAutoDraw(True)
        
        # if welcome_text is active this frame...
        if welcome_text.status == STARTED:
            # update params
            pass
        
        # *press_resp* updates
        waitOnFlip = False
        
        # if press_resp is starting this frame...
        if press_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            press_resp.frameNStart = frameN  # exact frame index
            press_resp.tStart = t  # local t and not account for scr refresh
            press_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(press_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'press_resp.started')
            # update status
            press_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(press_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(press_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if press_resp.status == STARTED and not waitOnFlip:
            theseKeys = press_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _press_resp_allKeys.extend(theseKeys)
            if len(_press_resp_allKeys):
                press_resp.keys = _press_resp_allKeys[-1].name  # just the last key pressed
                press_resp.rt = _press_resp_allKeys[-1].rt
                press_resp.duration = _press_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=welcome_routine,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            welcome_routine.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if welcome_routine.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in welcome_routine.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "welcome_routine" ---
    for thisComponent in welcome_routine.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for welcome_routine
    welcome_routine.tStop = globalClock.getTime(format='float')
    welcome_routine.tStopRefresh = tThisFlipGlobal
    thisExp.addData('welcome_routine.stopped', welcome_routine.tStop)
    # check responses
    if press_resp.keys in ['', [], None]:  # No response was made
        press_resp.keys = None
    thisExp.addData('press_resp.keys',press_resp.keys)
    if press_resp.keys != None:  # we had a response
        thisExp.addData('press_resp.rt', press_resp.rt)
        thisExp.addData('press_resp.duration', press_resp.duration)
    thisExp.nextEntry()
    # the Routine "welcome_routine" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('corsi_conditions.csv'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial in trials:
        trials.status = STARTED
        if hasattr(thisTrial, 'status'):
            thisTrial.status = STARTED
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "corsi_show" ---
        # create an object to store info about Routine corsi_show
        corsi_show = data.Routine(
            name='corsi_show',
            components=[blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9],
        )
        corsi_show.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from mark_show
        blocks = [blk1, blk2, blk3, blk4, blk5, blk6, blk7, blk8, blk9]
        seq = [int(x) for x in sequence.split('-')]
        last_idx = -1
        # store start times for corsi_show
        corsi_show.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        corsi_show.tStart = globalClock.getTime(format='float')
        corsi_show.status = STARTED
        thisExp.addData('corsi_show.started', corsi_show.tStart)
        corsi_show.maxDuration = None
        # keep track of which components have finished
        corsi_showComponents = corsi_show.components
        for thisComponent in corsi_show.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "corsi_show" ---
        thisExp.currentRoutine = corsi_show
        corsi_show.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *blk1* updates
            
            # if blk1 is starting this frame...
            if blk1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk1.frameNStart = frameN  # exact frame index
                blk1.tStart = t  # local t and not account for scr refresh
                blk1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk1.started')
                # update status
                blk1.status = STARTED
                blk1.setAutoDraw(True)
            
            # if blk1 is active this frame...
            if blk1.status == STARTED:
                # update params
                pass
            
            # *blk2* updates
            
            # if blk2 is starting this frame...
            if blk2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk2.frameNStart = frameN  # exact frame index
                blk2.tStart = t  # local t and not account for scr refresh
                blk2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk2.started')
                # update status
                blk2.status = STARTED
                blk2.setAutoDraw(True)
            
            # if blk2 is active this frame...
            if blk2.status == STARTED:
                # update params
                pass
            
            # *blk3* updates
            
            # if blk3 is starting this frame...
            if blk3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk3.frameNStart = frameN  # exact frame index
                blk3.tStart = t  # local t and not account for scr refresh
                blk3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk3.started')
                # update status
                blk3.status = STARTED
                blk3.setAutoDraw(True)
            
            # if blk3 is active this frame...
            if blk3.status == STARTED:
                # update params
                pass
            
            # *blk4* updates
            
            # if blk4 is starting this frame...
            if blk4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk4.frameNStart = frameN  # exact frame index
                blk4.tStart = t  # local t and not account for scr refresh
                blk4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk4.started')
                # update status
                blk4.status = STARTED
                blk4.setAutoDraw(True)
            
            # if blk4 is active this frame...
            if blk4.status == STARTED:
                # update params
                pass
            
            # *blk5* updates
            
            # if blk5 is starting this frame...
            if blk5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk5.frameNStart = frameN  # exact frame index
                blk5.tStart = t  # local t and not account for scr refresh
                blk5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk5.started')
                # update status
                blk5.status = STARTED
                blk5.setAutoDraw(True)
            
            # if blk5 is active this frame...
            if blk5.status == STARTED:
                # update params
                pass
            
            # *blk6* updates
            
            # if blk6 is starting this frame...
            if blk6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk6.frameNStart = frameN  # exact frame index
                blk6.tStart = t  # local t and not account for scr refresh
                blk6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk6.started')
                # update status
                blk6.status = STARTED
                blk6.setAutoDraw(True)
            
            # if blk6 is active this frame...
            if blk6.status == STARTED:
                # update params
                pass
            
            # *blk7* updates
            
            # if blk7 is starting this frame...
            if blk7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk7.frameNStart = frameN  # exact frame index
                blk7.tStart = t  # local t and not account for scr refresh
                blk7.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk7, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk7.started')
                # update status
                blk7.status = STARTED
                blk7.setAutoDraw(True)
            
            # if blk7 is active this frame...
            if blk7.status == STARTED:
                # update params
                pass
            
            # *blk8* updates
            
            # if blk8 is starting this frame...
            if blk8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk8.frameNStart = frameN  # exact frame index
                blk8.tStart = t  # local t and not account for scr refresh
                blk8.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk8, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk8.started')
                # update status
                blk8.status = STARTED
                blk8.setAutoDraw(True)
            
            # if blk8 is active this frame...
            if blk8.status == STARTED:
                # update params
                pass
            
            # *blk9* updates
            
            # if blk9 is starting this frame...
            if blk9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                blk9.frameNStart = frameN  # exact frame index
                blk9.tStart = t  # local t and not account for scr refresh
                blk9.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blk9, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blk9.started')
                # update status
                blk9.status = STARTED
                blk9.setAutoDraw(True)
            
            # if blk9 is active this frame...
            if blk9.status == STARTED:
                # update params
                pass
            # Run 'Each Frame' code from mark_show
            ON, OFF = 0.6, 0.4
            step = ON + OFF
            idx = int(t // step)
            if idx >= len(seq):
                continueRoutine = False
            else:
                for b in blocks:
                    b.fillColor = 'white'
                if (t % step) < ON:
                    blocks[seq[idx]-1].fillColor = 'yellow'
                    if idx != last_idx:
                        win.callOnFlip(outlet.push_sample, [str(20 + seq[idx])])
                        thisExp.addData(f'onset_blk{idx+1}', globalClock.getTime())
                        last_idx = idx
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=corsi_show,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                corsi_show.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if corsi_show.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in corsi_show.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "corsi_show" ---
        for thisComponent in corsi_show.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for corsi_show
        corsi_show.tStop = globalClock.getTime(format='float')
        corsi_show.tStopRefresh = tThisFlipGlobal
        thisExp.addData('corsi_show.stopped', corsi_show.tStop)
        # the Routine "corsi_show" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "corsi_delay" ---
        # create an object to store info about Routine corsi_delay
        corsi_delay = data.Routine(
            name='corsi_delay',
            components=[fix],
        )
        corsi_delay.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for corsi_delay
        corsi_delay.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        corsi_delay.tStart = globalClock.getTime(format='float')
        corsi_delay.status = STARTED
        thisExp.addData('corsi_delay.started', corsi_delay.tStart)
        corsi_delay.maxDuration = None
        # keep track of which components have finished
        corsi_delayComponents = corsi_delay.components
        for thisComponent in corsi_delay.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "corsi_delay" ---
        thisExp.currentRoutine = corsi_delay
        corsi_delay.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *fix* updates
            
            # if fix is starting this frame...
            if fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                fix.frameNStart = frameN  # exact frame index
                fix.tStart = t  # local t and not account for scr refresh
                fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'fix.started')
                # update status
                fix.status = STARTED
                fix.setAutoDraw(True)
            
            # if fix is active this frame...
            if fix.status == STARTED:
                # update params
                pass
            
            # if fix is stopping this frame...
            if fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > fix.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    fix.tStop = t  # not accounting for scr refresh
                    fix.tStopRefresh = tThisFlipGlobal  # on global time
                    fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'fix.stopped')
                    # update status
                    fix.status = FINISHED
                    fix.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=corsi_delay,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                corsi_delay.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if corsi_delay.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in corsi_delay.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "corsi_delay" ---
        for thisComponent in corsi_delay.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for corsi_delay
        corsi_delay.tStop = globalClock.getTime(format='float')
        corsi_delay.tStopRefresh = tThisFlipGlobal
        thisExp.addData('corsi_delay.stopped', corsi_delay.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if corsi_delay.maxDurationReached:
            routineTimer.addTime(-corsi_delay.maxDuration)
        elif corsi_delay.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "corsi_resp" ---
        # create an object to store info about Routine corsi_resp
        corsi_resp = data.Routine(
            name='corsi_resp',
            components=[rblk1, rblk2, rblk3, rblk4, rblk5, rblk6, rblk7, rblk8, rblk9, mouse],
        )
        corsi_resp.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from mark_delay
        rblocks = [rblk1, rblk2, rblk3, rblk4, rblk5, rblk6, rblk7, rblk8, rblk9]
        clicks = []
        prev = False
        for b in rblocks:
            b.fillColor = 'white'
        # setup some python lists for storing info about the mouse
        mouse.x = []
        mouse.y = []
        mouse.leftButton = []
        mouse.midButton = []
        mouse.rightButton = []
        mouse.time = []
        mouse.clicked_name = []
        gotValidClick = False  # until a click is received
        # store start times for corsi_resp
        corsi_resp.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        corsi_resp.tStart = globalClock.getTime(format='float')
        corsi_resp.status = STARTED
        thisExp.addData('corsi_resp.started', corsi_resp.tStart)
        corsi_resp.maxDuration = None
        # keep track of which components have finished
        corsi_respComponents = corsi_resp.components
        for thisComponent in corsi_resp.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "corsi_resp" ---
        thisExp.currentRoutine = corsi_resp
        corsi_resp.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *rblk1* updates
            
            # if rblk1 is starting this frame...
            if rblk1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk1.frameNStart = frameN  # exact frame index
                rblk1.tStart = t  # local t and not account for scr refresh
                rblk1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk1.started')
                # update status
                rblk1.status = STARTED
                rblk1.setAutoDraw(True)
            
            # if rblk1 is active this frame...
            if rblk1.status == STARTED:
                # update params
                pass
            
            # *rblk2* updates
            
            # if rblk2 is starting this frame...
            if rblk2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk2.frameNStart = frameN  # exact frame index
                rblk2.tStart = t  # local t and not account for scr refresh
                rblk2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk2.started')
                # update status
                rblk2.status = STARTED
                rblk2.setAutoDraw(True)
            
            # if rblk2 is active this frame...
            if rblk2.status == STARTED:
                # update params
                pass
            
            # *rblk3* updates
            
            # if rblk3 is starting this frame...
            if rblk3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk3.frameNStart = frameN  # exact frame index
                rblk3.tStart = t  # local t and not account for scr refresh
                rblk3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk3.started')
                # update status
                rblk3.status = STARTED
                rblk3.setAutoDraw(True)
            
            # if rblk3 is active this frame...
            if rblk3.status == STARTED:
                # update params
                pass
            
            # *rblk4* updates
            
            # if rblk4 is starting this frame...
            if rblk4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk4.frameNStart = frameN  # exact frame index
                rblk4.tStart = t  # local t and not account for scr refresh
                rblk4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk4.started')
                # update status
                rblk4.status = STARTED
                rblk4.setAutoDraw(True)
            
            # if rblk4 is active this frame...
            if rblk4.status == STARTED:
                # update params
                pass
            
            # *rblk5* updates
            
            # if rblk5 is starting this frame...
            if rblk5.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk5.frameNStart = frameN  # exact frame index
                rblk5.tStart = t  # local t and not account for scr refresh
                rblk5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk5.started')
                # update status
                rblk5.status = STARTED
                rblk5.setAutoDraw(True)
            
            # if rblk5 is active this frame...
            if rblk5.status == STARTED:
                # update params
                pass
            
            # *rblk6* updates
            
            # if rblk6 is starting this frame...
            if rblk6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk6.frameNStart = frameN  # exact frame index
                rblk6.tStart = t  # local t and not account for scr refresh
                rblk6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk6, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk6.started')
                # update status
                rblk6.status = STARTED
                rblk6.setAutoDraw(True)
            
            # if rblk6 is active this frame...
            if rblk6.status == STARTED:
                # update params
                pass
            
            # *rblk7* updates
            
            # if rblk7 is starting this frame...
            if rblk7.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk7.frameNStart = frameN  # exact frame index
                rblk7.tStart = t  # local t and not account for scr refresh
                rblk7.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk7, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk7.started')
                # update status
                rblk7.status = STARTED
                rblk7.setAutoDraw(True)
            
            # if rblk7 is active this frame...
            if rblk7.status == STARTED:
                # update params
                pass
            
            # *rblk8* updates
            
            # if rblk8 is starting this frame...
            if rblk8.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk8.frameNStart = frameN  # exact frame index
                rblk8.tStart = t  # local t and not account for scr refresh
                rblk8.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk8, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk8.started')
                # update status
                rblk8.status = STARTED
                rblk8.setAutoDraw(True)
            
            # if rblk8 is active this frame...
            if rblk8.status == STARTED:
                # update params
                pass
            
            # *rblk9* updates
            
            # if rblk9 is starting this frame...
            if rblk9.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rblk9.frameNStart = frameN  # exact frame index
                rblk9.tStart = t  # local t and not account for scr refresh
                rblk9.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rblk9, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rblk9.started')
                # update status
                rblk9.status = STARTED
                rblk9.setAutoDraw(True)
            
            # if rblk9 is active this frame...
            if rblk9.status == STARTED:
                # update params
                pass
            # Run 'Each Frame' code from mark_delay
            now = mouse.getPressed()[0]
            if now and not prev:
                for i, b in enumerate(rblocks, start=1):
                    if b.contains(mouse):
                        clicks.append(i)
                        b.fillColor = 'grey'
                        outlet.push_sample([str(60 + i)])
                        thisExp.addData('onset_delay', globalClock.getTime())
                        break
                if len(clicks) >= len(seq):
                    continueRoutine = False
            prev = now 
            # *mouse* updates
            
            # if mouse is starting this frame...
            if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                mouse.frameNStart = frameN  # exact frame index
                mouse.tStart = t  # local t and not account for scr refresh
                mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('mouse.started', t)
                # update status
                mouse.status = STARTED
                mouse.mouseClock.reset()
                prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
            if mouse.status == STARTED:  # only update if started and not finished!
                buttons = mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        # check if the mouse was inside our 'clickable' objects
                        gotValidClick = False
                        clickableList = environmenttools.getFromNames([rblk1, rblk2, rblk3, rblk4, rblk5, rblk6, rblk7, rblk8, rblk9], namespace=locals())
                        for obj in clickableList:
                            # is this object clicked on?
                            if obj.contains(mouse):
                                gotValidClick = True
                                mouse.clicked_name.append(obj.name)
                        if not gotValidClick:
                            mouse.clicked_name.append(None)
                        x, y = mouse.getPos()
                        mouse.x.append(float(x))
                        mouse.y.append(float(y))
                        buttons = mouse.getPressed()
                        mouse.leftButton.append(buttons[0])
                        mouse.midButton.append(buttons[1])
                        mouse.rightButton.append(buttons[2])
                        mouse.time.append(mouse.mouseClock.getTime())
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=corsi_resp,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                corsi_resp.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if corsi_resp.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in corsi_resp.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "corsi_resp" ---
        for thisComponent in corsi_resp.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for corsi_resp
        corsi_resp.tStop = globalClock.getTime(format='float')
        corsi_resp.tStopRefresh = tThisFlipGlobal
        thisExp.addData('corsi_resp.stopped', corsi_resp.tStop)
        # Run 'End Routine' code from mark_delay
        ok = (clicks == seq)
        n_correct += ok
        thisExp.addData('resp_seq', '-'.join(map(str, clicks)))
        thisExp.addData('corsi_correct', int(ok))
        print(f"[{trials.thisN+1}] span {span}: {seq} -> {clicks} {'OK' if ok else 'WRONG'}")
        # store data for trials (TrialHandler)
        trials.addData('mouse.x', mouse.x)
        trials.addData('mouse.y', mouse.y)
        trials.addData('mouse.leftButton', mouse.leftButton)
        trials.addData('mouse.midButton', mouse.midButton)
        trials.addData('mouse.rightButton', mouse.rightButton)
        trials.addData('mouse.time', mouse.time)
        trials.addData('mouse.clicked_name', mouse.clicked_name)
        # the Routine "corsi_resp" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "iti" ---
        # create an object to store info about Routine iti
        iti = data.Routine(
            name='iti',
            components=[text],
        )
        iti.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for iti
        iti.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        iti.tStart = globalClock.getTime(format='float')
        iti.status = STARTED
        thisExp.addData('iti.started', iti.tStart)
        iti.maxDuration = None
        # keep track of which components have finished
        itiComponents = iti.components
        for thisComponent in iti.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "iti" ---
        thisExp.currentRoutine = iti
        iti.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 1.5:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *text* updates
            
            # if text is starting this frame...
            if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                text.frameNStart = frameN  # exact frame index
                text.tStart = t  # local t and not account for scr refresh
                text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'text.started')
                # update status
                text.status = STARTED
                text.setAutoDraw(True)
            
            # if text is active this frame...
            if text.status == STARTED:
                # update params
                pass
            
            # if text is stopping this frame...
            if text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > text.tStartRefresh + 1.5-frameTolerance:
                    # keep track of stop time/frame for later
                    text.tStop = t  # not accounting for scr refresh
                    text.tStopRefresh = tThisFlipGlobal  # on global time
                    text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'text.stopped')
                    # update status
                    text.status = FINISHED
                    text.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=iti,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                iti.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if iti.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in iti.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "iti" ---
        for thisComponent in iti.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for iti
        iti.tStop = globalClock.getTime(format='float')
        iti.tStopRefresh = tThisFlipGlobal
        thisExp.addData('iti.stopped', iti.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if iti.maxDurationReached:
            routineTimer.addTime(-iti.maxDuration)
        elif iti.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-1.500000)
        # mark thisTrial as finished
        if hasattr(thisTrial, 'status'):
            thisTrial.status = FINISHED
        # if awaiting a pause, pause now
        if trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            trials.status = STARTED
        thisExp.nextEntry()
        
    # completed 1 repeats of 'trials'
    trials.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "goodbye" ---
    # create an object to store info about Routine goodbye
    goodbye = data.Routine(
        name='goodbye',
        components=[bye_text],
    )
    goodbye.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # Run 'Begin Routine' code from bye_code
    bye_text.text = f'Задание завершено.\n\nПравильно: {n_correct} из {trials.nTotal}'
    # store start times for goodbye
    goodbye.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    goodbye.tStart = globalClock.getTime(format='float')
    goodbye.status = STARTED
    thisExp.addData('goodbye.started', goodbye.tStart)
    goodbye.maxDuration = None
    # keep track of which components have finished
    goodbyeComponents = goodbye.components
    for thisComponent in goodbye.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "goodbye" ---
    thisExp.currentRoutine = goodbye
    goodbye.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *bye_text* updates
        
        # if bye_text is starting this frame...
        if bye_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            bye_text.frameNStart = frameN  # exact frame index
            bye_text.tStart = t  # local t and not account for scr refresh
            bye_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(bye_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'bye_text.started')
            # update status
            bye_text.status = STARTED
            bye_text.setAutoDraw(True)
        
        # if bye_text is active this frame...
        if bye_text.status == STARTED:
            # update params
            pass
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=goodbye,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            goodbye.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if goodbye.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in goodbye.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "goodbye" ---
    for thisComponent in goodbye.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for goodbye
    goodbye.tStop = globalClock.getTime(format='float')
    goodbye.tStopRefresh = tThisFlipGlobal
    thisExp.addData('goodbye.stopped', goodbye.tStop)
    thisExp.nextEntry()
    # the Routine "goodbye" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
