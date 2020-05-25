'''
Last updated on 25/5/2020
The Sperling's single-Ensemble Task

Some Amendments (25/5/2020):
Add 500ms ISI blank screen "done"
Amend to option 2
Take +/- together for the psychometric curve

(
4 Experimental Conditions x
3 Center Orientation Tilts (0, +-10, +-20) x
3 Set Orientation Tilts (0, +-10, +-20) x
2 Configuration (+/-) x
5 Repetitions (Positional Changes???)
) = 360 trials
'''

# import libraries
import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime
from psychopy import visual, event, monitors, core, logging, gui

'''
variables to calibrate the monitor
line_width_in_pixel is only used in the line width of the
precue and postcue, psychopy not supported in deg units
The border width of the circle is 0.2 visual angle
'''

# Setting for both RLG307 Monitors
monitor_name = 'RLG307'
view_distance = 60
screen_width = 59.8
screen_resolution = [3840,2160]
line_width_in_pixel = 13

# Setting for Home Monitor
# monitor_name = 'testMonitor'
# view_distance = 60
# screen_width = 47.5
# screen_resolution = [1680,1050]
# line_width_in_pixel = 7

# declare variables for trial generation
No_of_Trials = 28
conditions = [1,2,3,4]
orientations = [0,5,-5,10,-10,20,-20]
positions = [1,2,3,4,5,6,7,8,9]
configurations = [0,1]  # 0 is coherent, 1 is in coherent
variations = [0,1]  # 0 is first variation, 1 is second variation
breaktrial = [  # for break trials
    ((No_of_Trials / 4) - 1),
    ((No_of_Trials / 2) - 1),
    ((3 * No_of_Trials / 4) - 1)]

# declare timing variables
fixation_time = 0.25
precue_time = 0.75
gaborset_time = 0.2
blankscreen_time = 0.4
isi_time = 0.5
short_break_time = 5
long_break_time = 5

# generating the trial list and randomly shuffle it
triallist = []
for condition in conditions:
    for orientation in orientations:
        np.random.shuffle(positions)
        for position in positions[0:5]:
            for configuration in configurations:
                for variation in variations:
                    trial = [condition, orientation, position, configuration, variation]
                    triallist.append(trial)
                    np.random.shuffle(triallist)

#  generating blank arrays for the output data file below
date_array = []
time_array = []
name_array = []
age_array = []
gender_array = []
hand_array = []
trial_no_array = []
condition_array = []
orientation_array = []
position_array = []
configuration_array = []
variation_array = []
response_array = []
latency_array = []

# Text Variables
instruct_text = \
    "\
Press 'f' or 'j' to Start the Experiment.\n\n\
Press 'End' to Quit now or Terminate the Experiment anytime.\
"

debrief_text = \
    "\
That's the End of the Experiment.\n\
Thank you for your Participation.\
"

may_break_text = \
    "\
Press 'space' to skip break\
"

must_break_text = \
    "\
In must break text\
"

end_break_text = \
    "\
In end break text, \n\
Press 'f' or 'j' to continue.\
"

# clear command output and start logging
os.system('cls' if os.name == 'ht' else 'clear')
logging.console.setLevel(logging.CRITICAL)
print("**************************************")
print("MODIFIED SPERLING'S SINGLE-ENSEMBLE TASK")
print("PSYCHOPY LOGGING set to : CRITICAL")
print(datetime.now())
print("**************************************")

# get current date and time
current_date = datetime.now().strftime("%Y%m%d")
current_time = datetime.now().strftime("%H%M%S")

# get observer's information
info = gui.Dlg(title="Ensemble Perception Experiment", pos = [600,300],
               labelButtonOK="READY", labelButtonCancel=" ")
info.addText("Observer's Info. ")
info.addField('Experiment Date (YMD): ', current_date)
info.addField('Experiment Time (HMS): ', current_time)
info.addField('Name: ')
info.addField('Age: ')
info.addField('Gender:', choices = ['Male', 'Female'])
info.addField('Dominant Hand: ', choices=['Right', 'Left'])
show_info = info.show()

# check info. and create save file name
if info.OK:
    save_file_name = show_info[0] + show_info[1] + '_' + \
        show_info[2] + '_ep_experiment.csv'
else:
    print("User Cancelled")

# Create Save Path
save_path = gui.fileSaveDlg(initFileName=save_file_name, prompt='Select Save File')

# calibrating monitor and creating window for experiment
mon = monitors.Monitor(monitor_name)
mon.setWidth(screen_width)
mon.setDistance(view_distance)

win = visual.Window(size=screen_resolution, color='#C0C0C0',
                    fullscr=True, monitor=mon, allowGUI = True
                    )


def instruction():
    #  creating the instruction text to shown at the beginning
    instruct = visual.TextStim(win = win, text = ' ', font = 'Times New Roman',
                               pos = (0,0), color = 'black', units = 'deg',
                               height = 0.9, wrapWidth=26
                               )

    instruct.setText(instruct_text)
    instruct.draw()
    win.flip()
    instructresp = event.waitKeys(maxWait=1000, keyList=['end','f', 'j'],
                                  clearEvents=True
                                  )

    if 'f' in instructresp or 'j' in instructresp:
        pass
    elif 'end' in instructresp:
        win.close()
        sys.exit()


def break_time(trial_no):
    # Create stimuli and actions in break trials
    break_text = visual.TextStim(win = win, text = ' ', font = 'Times New Roman',
                                 pos = (0,-8), color = 'black', units = 'deg',
                                 height = 0.9, wrapWidth=20
                                 )
    break_timer = visual.TextStim(win = win, text = ' ', font = 'Source Code Pro',
                                  pos = (0,0), color = 'black', units = 'deg',
                                  height = 4, wrapWidth=20
                                  )

    if trial_no == breaktrial[1]:  # Must break
        break_text.setText(must_break_text)
        break_text.draw()
        win.flip()
        timer = core.CountdownTimer(long_break_time)
        while timer.getTime() > 0:
            break_timer.setText(round(timer.getTime(), 1))
            break_text.draw()
            break_timer.draw()
            win.flip()
            if event.getKeys(['end']):
                win.close()
                sys.exit()

    else:  # Self-Terminated Break
        break_text.setText(may_break_text)
        break_text.draw()
        win.flip()
        timer = core.CountdownTimer(short_break_time)
        while timer.getTime() > 0:
            break_timer.setText(round(timer.getTime(), 1))
            break_text.draw()
            break_timer.draw()
            win.flip()
            if event.getKeys(['space']):
                break
            elif event.getKeys(['end']):
                win.close()
                sys.exit()

    break_text.setText(end_break_text)
    break_timer.setText(round(timer.getTime(), 1))
    break_text.draw()
    break_timer.draw()
    win.flip()
    breakresp = event.waitKeys(maxWait=1000, keyList=['end','f', 'j'],
                               clearEvents=True
                               )
    if 'f' in breakresp or 'j' in breakresp:
        pass
    elif 'end' in breakresp:
        win.close()
        sys.exit()


def fixation():
    # creating and drawing fixation cross to memeory
    fix_hori = visual.Rect(win = win, width=0.9, height=0.1, units='deg',
                           lineColor='black', fillColor='black', pos=(0,0)
                           )
    fix_vert = visual.Rect(win = win, width=0.1, height=0.9, units='deg',
                           lineColor='black', fillColor='black', pos=(0,0)
                           )

    fix_hori.draw()
    fix_vert.draw()


def pos_to_coordinate(position):
    '''
    Dictionary to convert position code to coordinates,
    used in precue and postcue as switch function
    '''
    return {1: (-1.4142, 1.4142),
            2: (0, 2),
            3: (1.4142, 1.4142),
            4: (-2, 0),
            5: (0,0),
            6: (2, 0),
            7: (-1.4142, -1.4142),
            8: (0, -2),
            9: (1.4142, -1.4142)}.get(position)


def precue(condition, position):
    """
    Creating and drawing the pre-cue circle to memory
    Condition 1 = single pre-cue congruent trial
    Condition 2 = single pre-cue incongruent trial
    Condition 3 = ensemble pre-cue congruent trial
    Condition 4 = ensemble pre-cue incongruent trial

    Condition 1 & 2 --> Return single pre-cue
    Condition 3 & 4 --> Return ensemble pre-cue
    """

    singleprecue = visual.Circle(win=win, units = 'deg', radius=0.9,
                                 edges=1000, fillColor='#C0C0C0', lineColor='black',
                                 lineWidth=line_width_in_pixel, opacity=1
                                 )
    setprecue = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.85,
                              edges=1000, fillColor='#C0C0C0', lineColor='black',
                              lineWidth=line_width_in_pixel, opacity=1
                              )

    if (condition == 1 or condition == 2):
        singleprecue.pos = pos_to_coordinate(position)
        singleprecue.draw()

    elif (condition == 3 or condition == 4):
        setprecue.draw()


def postcue(condition, position):
    """
    Creating and drawing the post-cue circle to memory
    Condition 1 = single pre-cue congruent trial
    Condition 2 = single pre-cue incongruent trial
    Condition 3 = ensemble pre-cue congruent trial
    Condition 4 = ensemble pre-cue incongruent trial

    Condition 1 & 4--> Return single post-cue
    Condition 2 & 3 --> Return ensemble post-cue
    """
    singlepostcue = visual.Circle(win=win, units = 'deg', radius=0.9,
                                  edges=1000, fillColor='#C0C0C0', lineColor='black',
                                  lineWidth=line_width_in_pixel, opacity=1
                                  )
    setpostcue = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.85,
                               edges=1000, fillColor='#C0C0C0', lineColor='black',
                               lineWidth=line_width_in_pixel, opacity=1
                               )

    if (condition == 1 or condition == 4):
        singlepostcue.pos = pos_to_coordinate(position)
        singlepostcue.draw()

    elif (condition == 2 or condition == 3):
        setpostcue.draw()


def gaborset(orientation, position, configuration, variation):
    '''creating the 9-gabor set, one central grating surrounded by
    8 gratings, the numbers refers to the position,
                (1,2,3)
                (4,5,6)
                (7,8,9)
    & drawing the set to memory
    '''
    grating5 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(0, 0),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating2 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(0, 2),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating8 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(0, -2),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating4 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(-2, 0),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating6 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(2, 0),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating1 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(-1.4142, 1.4142),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating3 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(1.4142, 1.4142),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating7 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(-1.4142, -1.4142),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )
    grating9 = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                  mask='gauss', ori=0, pos=(1.4142, -1.4142),
                                  size=(1.6,1.6), sf=3, opacity = 1,
                                  blendmode='avg', texRes=128, interpolate=True,
                                  depth=0.0
                                  )

    if orientation == 0:
        var0 = [60, 60, 80, 80, -20, -20, -20, -40]
        var1 = [60, 80, 80, 80, -20, -20, -40, -40]
        if position == 1:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + var0[0])
                    grating3.setOri(orientation + var0[1])
                    grating4.setOri(orientation + var0[2])
                    grating5.setOri(orientation + var0[3])
                    grating6.setOri(orientation + var0[4])
                    grating7.setOri(orientation + var0[5])
                    grating8.setOri(orientation + var0[6])
                    grating9.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + var1[0])
                    grating3.setOri(orientation + var1[1])
                    grating4.setOri(orientation + var1[2])
                    grating5.setOri(orientation + var1[3])
                    grating6.setOri(orientation + var1[4])
                    grating7.setOri(orientation + var1[5])
                    grating8.setOri(orientation + var1[6])
                    grating9.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - var0[0])
                    grating3.setOri(orientation - var0[1])
                    grating4.setOri(orientation - var0[2])
                    grating5.setOri(orientation - var0[3])
                    grating6.setOri(orientation - var0[4])
                    grating7.setOri(orientation - var0[5])
                    grating8.setOri(orientation - var0[6])
                    grating9.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - var1[0])
                    grating3.setOri(orientation - var1[1])
                    grating4.setOri(orientation - var1[2])
                    grating5.setOri(orientation - var1[3])
                    grating6.setOri(orientation - var1[4])
                    grating7.setOri(orientation - var1[5])
                    grating8.setOri(orientation - var1[6])
                    grating9.setOri(orientation - var1[7])
        elif position == 2:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + var0[0])
                    grating4.setOri(orientation + var0[1])
                    grating5.setOri(orientation + var0[2])
                    grating6.setOri(orientation + var0[3])
                    grating7.setOri(orientation + var0[4])
                    grating8.setOri(orientation + var0[5])
                    grating9.setOri(orientation + var0[6])
                    grating1.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + var1[0])
                    grating4.setOri(orientation + var1[1])
                    grating5.setOri(orientation + var1[2])
                    grating6.setOri(orientation + var1[3])
                    grating7.setOri(orientation + var1[4])
                    grating8.setOri(orientation + var1[5])
                    grating9.setOri(orientation + var1[6])
                    grating1.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - var0[0])
                    grating4.setOri(orientation - var0[1])
                    grating5.setOri(orientation - var0[2])
                    grating6.setOri(orientation - var0[3])
                    grating7.setOri(orientation - var0[4])
                    grating8.setOri(orientation - var0[5])
                    grating9.setOri(orientation - var0[6])
                    grating1.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - var1[0])
                    grating4.setOri(orientation - var1[1])
                    grating5.setOri(orientation - var1[2])
                    grating6.setOri(orientation - var1[3])
                    grating7.setOri(orientation - var1[4])
                    grating8.setOri(orientation - var1[5])
                    grating9.setOri(orientation - var1[6])
                    grating1.setOri(orientation - var1[7])
        elif position == 3:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + var0[0])
                    grating5.setOri(orientation + var0[1])
                    grating6.setOri(orientation + var0[2])
                    grating7.setOri(orientation + var0[3])
                    grating8.setOri(orientation + var0[4])
                    grating9.setOri(orientation + var0[5])
                    grating1.setOri(orientation + var0[6])
                    grating2.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + var1[0])
                    grating5.setOri(orientation + var1[1])
                    grating6.setOri(orientation + var1[2])
                    grating7.setOri(orientation + var1[3])
                    grating8.setOri(orientation + var1[4])
                    grating9.setOri(orientation + var1[5])
                    grating1.setOri(orientation + var1[6])
                    grating2.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - var0[0])
                    grating5.setOri(orientation - var0[1])
                    grating6.setOri(orientation - var0[2])
                    grating7.setOri(orientation - var0[3])
                    grating8.setOri(orientation - var0[4])
                    grating9.setOri(orientation - var0[5])
                    grating1.setOri(orientation - var0[6])
                    grating2.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - var1[0])
                    grating5.setOri(orientation - var1[1])
                    grating6.setOri(orientation - var1[2])
                    grating7.setOri(orientation - var1[3])
                    grating8.setOri(orientation - var1[4])
                    grating9.setOri(orientation - var1[5])
                    grating1.setOri(orientation - var1[6])
                    grating2.setOri(orientation - var1[7])
        elif position == 4:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + var0[0])
                    grating6.setOri(orientation + var0[1])
                    grating7.setOri(orientation + var0[2])
                    grating8.setOri(orientation + var0[3])
                    grating9.setOri(orientation + var0[4])
                    grating1.setOri(orientation + var0[5])
                    grating2.setOri(orientation + var0[6])
                    grating3.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + var1[0])
                    grating6.setOri(orientation + var1[1])
                    grating7.setOri(orientation + var1[2])
                    grating8.setOri(orientation + var1[3])
                    grating9.setOri(orientation + var1[4])
                    grating1.setOri(orientation + var1[5])
                    grating2.setOri(orientation + var1[6])
                    grating3.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - var0[0])
                    grating6.setOri(orientation - var0[1])
                    grating7.setOri(orientation - var0[2])
                    grating8.setOri(orientation - var0[3])
                    grating9.setOri(orientation - var0[4])
                    grating1.setOri(orientation - var0[5])
                    grating2.setOri(orientation - var0[6])
                    grating3.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - var1[0])
                    grating6.setOri(orientation - var1[1])
                    grating7.setOri(orientation - var1[2])
                    grating8.setOri(orientation - var1[3])
                    grating9.setOri(orientation - var1[4])
                    grating1.setOri(orientation - var1[5])
                    grating2.setOri(orientation - var1[6])
                    grating3.setOri(orientation - var1[7])
        elif position == 5:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + var0[0])
                    grating7.setOri(orientation + var0[1])
                    grating8.setOri(orientation + var0[2])
                    grating9.setOri(orientation + var0[3])
                    grating1.setOri(orientation + var0[4])
                    grating2.setOri(orientation + var0[5])
                    grating3.setOri(orientation + var0[6])
                    grating4.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + var1[0])
                    grating7.setOri(orientation + var1[1])
                    grating8.setOri(orientation + var1[2])
                    grating9.setOri(orientation + var1[3])
                    grating1.setOri(orientation + var1[4])
                    grating2.setOri(orientation + var1[5])
                    grating3.setOri(orientation + var1[6])
                    grating4.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - var0[0])
                    grating7.setOri(orientation - var0[1])
                    grating8.setOri(orientation - var0[2])
                    grating9.setOri(orientation - var0[3])
                    grating1.setOri(orientation - var0[4])
                    grating2.setOri(orientation - var0[5])
                    grating3.setOri(orientation - var0[6])
                    grating4.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - var1[0])
                    grating7.setOri(orientation - var1[1])
                    grating8.setOri(orientation - var1[2])
                    grating9.setOri(orientation - var1[3])
                    grating1.setOri(orientation - var1[4])
                    grating2.setOri(orientation - var1[5])
                    grating3.setOri(orientation - var1[6])
                    grating4.setOri(orientation - var1[7])
        elif position == 6:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + var0[0])
                    grating8.setOri(orientation + var0[1])
                    grating9.setOri(orientation + var0[2])
                    grating1.setOri(orientation + var0[3])
                    grating2.setOri(orientation + var0[4])
                    grating3.setOri(orientation + var0[5])
                    grating4.setOri(orientation + var0[6])
                    grating5.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + var1[0])
                    grating8.setOri(orientation + var1[1])
                    grating9.setOri(orientation + var1[2])
                    grating1.setOri(orientation + var1[3])
                    grating2.setOri(orientation + var1[4])
                    grating3.setOri(orientation + var1[5])
                    grating4.setOri(orientation + var1[6])
                    grating5.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - var0[0])
                    grating8.setOri(orientation - var0[1])
                    grating9.setOri(orientation - var0[2])
                    grating1.setOri(orientation - var0[3])
                    grating2.setOri(orientation - var0[4])
                    grating3.setOri(orientation - var0[5])
                    grating4.setOri(orientation - var0[6])
                    grating5.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - var1[0])
                    grating8.setOri(orientation - var1[1])
                    grating9.setOri(orientation - var1[2])
                    grating1.setOri(orientation - var1[3])
                    grating2.setOri(orientation - var1[4])
                    grating3.setOri(orientation - var1[5])
                    grating4.setOri(orientation - var1[6])
                    grating5.setOri(orientation - var1[7])
        elif position == 7:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + var0[0])
                    grating9.setOri(orientation + var0[1])
                    grating1.setOri(orientation + var0[2])
                    grating2.setOri(orientation + var0[3])
                    grating3.setOri(orientation + var0[4])
                    grating4.setOri(orientation + var0[5])
                    grating5.setOri(orientation + var0[6])
                    grating6.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + var1[0])
                    grating9.setOri(orientation + var1[1])
                    grating1.setOri(orientation + var1[2])
                    grating2.setOri(orientation + var1[3])
                    grating3.setOri(orientation + var1[4])
                    grating4.setOri(orientation + var1[5])
                    grating5.setOri(orientation + var1[6])
                    grating6.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - var0[0])
                    grating9.setOri(orientation - var0[1])
                    grating1.setOri(orientation - var0[2])
                    grating2.setOri(orientation - var0[3])
                    grating3.setOri(orientation - var0[4])
                    grating4.setOri(orientation - var0[5])
                    grating5.setOri(orientation - var0[6])
                    grating6.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - var1[0])
                    grating9.setOri(orientation - var1[1])
                    grating1.setOri(orientation - var1[2])
                    grating2.setOri(orientation - var1[3])
                    grating3.setOri(orientation - var1[4])
                    grating4.setOri(orientation - var1[5])
                    grating5.setOri(orientation - var1[6])
                    grating6.setOri(orientation - var1[7])
        elif position == 8:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + var0[0])
                    grating1.setOri(orientation + var0[1])
                    grating2.setOri(orientation + var0[2])
                    grating3.setOri(orientation + var0[3])
                    grating4.setOri(orientation + var0[4])
                    grating5.setOri(orientation + var0[5])
                    grating6.setOri(orientation + var0[6])
                    grating7.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + var1[0])
                    grating1.setOri(orientation + var1[1])
                    grating2.setOri(orientation + var1[2])
                    grating3.setOri(orientation + var1[3])
                    grating4.setOri(orientation + var1[4])
                    grating5.setOri(orientation + var1[5])
                    grating6.setOri(orientation + var1[6])
                    grating7.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - var0[0])
                    grating1.setOri(orientation - var0[1])
                    grating2.setOri(orientation - var0[2])
                    grating3.setOri(orientation - var0[3])
                    grating4.setOri(orientation - var0[4])
                    grating5.setOri(orientation - var0[5])
                    grating6.setOri(orientation - var0[6])
                    grating7.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - var1[0])
                    grating1.setOri(orientation - var1[1])
                    grating2.setOri(orientation - var1[2])
                    grating3.setOri(orientation - var1[3])
                    grating4.setOri(orientation - var1[4])
                    grating5.setOri(orientation - var1[5])
                    grating6.setOri(orientation - var1[6])
                    grating7.setOri(orientation - var1[7])
        elif position == 9:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + var0[0])
                    grating2.setOri(orientation + var0[1])
                    grating3.setOri(orientation + var0[2])
                    grating4.setOri(orientation + var0[3])
                    grating5.setOri(orientation + var0[4])
                    grating6.setOri(orientation + var0[5])
                    grating7.setOri(orientation + var0[6])
                    grating8.setOri(orientation + var0[7])
                else:
                    np.random.shuffle(var1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + var1[0])
                    grating2.setOri(orientation + var1[1])
                    grating3.setOri(orientation + var1[2])
                    grating4.setOri(orientation + var1[3])
                    grating5.setOri(orientation + var1[4])
                    grating6.setOri(orientation + var1[5])
                    grating7.setOri(orientation + var1[6])
                    grating8.setOri(orientation + var1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(var0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - var0[0])
                    grating2.setOri(orientation - var0[1])
                    grating3.setOri(orientation - var0[2])
                    grating4.setOri(orientation - var0[3])
                    grating5.setOri(orientation - var0[4])
                    grating6.setOri(orientation - var0[5])
                    grating7.setOri(orientation - var0[6])
                    grating8.setOri(orientation - var0[7])
                else:
                    np.random.shuffle(var1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - var1[0])
                    grating2.setOri(orientation - var1[1])
                    grating3.setOri(orientation - var1[2])
                    grating4.setOri(orientation - var1[3])
                    grating5.setOri(orientation - var1[4])
                    grating6.setOri(orientation - var1[5])
                    grating7.setOri(orientation - var1[6])
                    grating8.setOri(orientation - var1[7])
    elif orientation == 5:
        posvar0 = [20, 40, 40, 60, -40, -60, -40, -20]
        posvar1 = [40, 40, 60, -20, -20, -20, -40, -40]
        negvar0 = [10, 20, 20, -20, -20, -20, -40, -40]
        negvar1 = [0, 0, 10, 20, -20, -20, -40, -40]
        if position == 1:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar0[0])
                    grating3.setOri(orientation + posvar0[1])
                    grating4.setOri(orientation + posvar0[2])
                    grating5.setOri(orientation + posvar0[3])
                    grating6.setOri(orientation + posvar0[4])
                    grating7.setOri(orientation + posvar0[5])
                    grating8.setOri(orientation + posvar0[6])
                    grating9.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar1[0])
                    grating3.setOri(orientation + posvar1[1])
                    grating4.setOri(orientation + posvar1[2])
                    grating5.setOri(orientation + posvar1[3])
                    grating6.setOri(orientation + posvar1[4])
                    grating7.setOri(orientation + posvar1[5])
                    grating8.setOri(orientation + posvar1[6])
                    grating9.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + negvar0[0])
                    grating3.setOri(orientation + negvar0[1])
                    grating4.setOri(orientation + negvar0[2])
                    grating5.setOri(orientation + negvar0[3])
                    grating6.setOri(orientation + negvar0[4])
                    grating7.setOri(orientation + negvar0[5])
                    grating8.setOri(orientation + negvar0[6])
                    grating9.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + negvar1[0])
                    grating3.setOri(orientation + negvar1[1])
                    grating4.setOri(orientation + negvar1[2])
                    grating5.setOri(orientation + negvar1[3])
                    grating6.setOri(orientation + negvar1[4])
                    grating7.setOri(orientation + negvar1[5])
                    grating8.setOri(orientation + negvar1[6])
                    grating9.setOri(orientation + negvar1[7])
        elif position == 2:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar0[0])
                    grating4.setOri(orientation + posvar0[1])
                    grating5.setOri(orientation + posvar0[2])
                    grating6.setOri(orientation + posvar0[3])
                    grating7.setOri(orientation + posvar0[4])
                    grating8.setOri(orientation + posvar0[5])
                    grating9.setOri(orientation + posvar0[6])
                    grating1.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar1[0])
                    grating4.setOri(orientation + posvar1[1])
                    grating5.setOri(orientation + posvar1[2])
                    grating6.setOri(orientation + posvar1[3])
                    grating7.setOri(orientation + posvar1[4])
                    grating8.setOri(orientation + posvar1[5])
                    grating9.setOri(orientation + posvar1[6])
                    grating1.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + negvar0[0])
                    grating4.setOri(orientation + negvar0[1])
                    grating5.setOri(orientation + negvar0[2])
                    grating6.setOri(orientation + negvar0[3])
                    grating7.setOri(orientation + negvar0[4])
                    grating8.setOri(orientation + negvar0[5])
                    grating9.setOri(orientation + negvar0[6])
                    grating1.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + negvar1[0])
                    grating4.setOri(orientation + negvar1[1])
                    grating5.setOri(orientation + negvar1[2])
                    grating6.setOri(orientation + negvar1[3])
                    grating7.setOri(orientation + negvar1[4])
                    grating8.setOri(orientation + negvar1[5])
                    grating9.setOri(orientation + negvar1[6])
                    grating1.setOri(orientation + negvar1[7])
        elif position == 3:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar0[0])
                    grating5.setOri(orientation + posvar0[1])
                    grating6.setOri(orientation + posvar0[2])
                    grating7.setOri(orientation + posvar0[3])
                    grating8.setOri(orientation + posvar0[4])
                    grating9.setOri(orientation + posvar0[5])
                    grating1.setOri(orientation + posvar0[6])
                    grating2.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar1[0])
                    grating5.setOri(orientation + posvar1[1])
                    grating6.setOri(orientation + posvar1[2])
                    grating7.setOri(orientation + posvar1[3])
                    grating8.setOri(orientation + posvar1[4])
                    grating9.setOri(orientation + posvar1[5])
                    grating1.setOri(orientation + posvar1[6])
                    grating2.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + negvar0[0])
                    grating5.setOri(orientation + negvar0[1])
                    grating6.setOri(orientation + negvar0[2])
                    grating7.setOri(orientation + negvar0[3])
                    grating8.setOri(orientation + negvar0[4])
                    grating9.setOri(orientation + negvar0[5])
                    grating1.setOri(orientation + negvar0[6])
                    grating2.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + negvar1[0])
                    grating5.setOri(orientation + negvar1[1])
                    grating6.setOri(orientation + negvar1[2])
                    grating7.setOri(orientation + negvar1[3])
                    grating8.setOri(orientation + negvar1[4])
                    grating9.setOri(orientation + negvar1[5])
                    grating1.setOri(orientation + negvar1[6])
                    grating2.setOri(orientation + negvar1[7])
        elif position == 4:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar0[0])
                    grating6.setOri(orientation + posvar0[1])
                    grating7.setOri(orientation + posvar0[2])
                    grating8.setOri(orientation + posvar0[3])
                    grating9.setOri(orientation + posvar0[4])
                    grating1.setOri(orientation + posvar0[5])
                    grating2.setOri(orientation + posvar0[6])
                    grating3.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar1[0])
                    grating6.setOri(orientation + posvar1[1])
                    grating7.setOri(orientation + posvar1[2])
                    grating8.setOri(orientation + posvar1[3])
                    grating9.setOri(orientation + posvar1[4])
                    grating1.setOri(orientation + posvar1[5])
                    grating2.setOri(orientation + posvar1[6])
                    grating3.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + negvar0[0])
                    grating6.setOri(orientation + negvar0[1])
                    grating7.setOri(orientation + negvar0[2])
                    grating8.setOri(orientation + negvar0[3])
                    grating9.setOri(orientation + negvar0[4])
                    grating1.setOri(orientation + negvar0[5])
                    grating2.setOri(orientation + negvar0[6])
                    grating3.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + negvar1[0])
                    grating6.setOri(orientation + negvar1[1])
                    grating7.setOri(orientation + negvar1[2])
                    grating8.setOri(orientation + negvar1[3])
                    grating9.setOri(orientation + negvar1[4])
                    grating1.setOri(orientation + negvar1[5])
                    grating2.setOri(orientation + negvar1[6])
                    grating3.setOri(orientation + negvar1[7])
        elif position == 5:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar0[0])
                    grating7.setOri(orientation + posvar0[1])
                    grating8.setOri(orientation + posvar0[2])
                    grating9.setOri(orientation + posvar0[3])
                    grating1.setOri(orientation + posvar0[4])
                    grating2.setOri(orientation + posvar0[5])
                    grating3.setOri(orientation + posvar0[6])
                    grating4.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar1[0])
                    grating7.setOri(orientation + posvar1[1])
                    grating8.setOri(orientation + posvar1[2])
                    grating9.setOri(orientation + posvar1[3])
                    grating1.setOri(orientation + posvar1[4])
                    grating2.setOri(orientation + posvar1[5])
                    grating3.setOri(orientation + posvar1[6])
                    grating4.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + negvar0[0])
                    grating7.setOri(orientation + negvar0[1])
                    grating8.setOri(orientation + negvar0[2])
                    grating9.setOri(orientation + negvar0[3])
                    grating1.setOri(orientation + negvar0[4])
                    grating2.setOri(orientation + negvar0[5])
                    grating3.setOri(orientation + negvar0[6])
                    grating4.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + negvar1[0])
                    grating7.setOri(orientation + negvar1[1])
                    grating8.setOri(orientation + negvar1[2])
                    grating9.setOri(orientation + negvar1[3])
                    grating1.setOri(orientation + negvar1[4])
                    grating2.setOri(orientation + negvar1[5])
                    grating3.setOri(orientation + negvar1[6])
                    grating4.setOri(orientation + negvar1[7])
        elif position == 6:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar0[0])
                    grating8.setOri(orientation + posvar0[1])
                    grating9.setOri(orientation + posvar0[2])
                    grating1.setOri(orientation + posvar0[3])
                    grating2.setOri(orientation + posvar0[4])
                    grating3.setOri(orientation + posvar0[5])
                    grating4.setOri(orientation + posvar0[6])
                    grating5.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar1[0])
                    grating8.setOri(orientation + posvar1[1])
                    grating9.setOri(orientation + posvar1[2])
                    grating1.setOri(orientation + posvar1[3])
                    grating2.setOri(orientation + posvar1[4])
                    grating3.setOri(orientation + posvar1[5])
                    grating4.setOri(orientation + posvar1[6])
                    grating5.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + negvar0[0])
                    grating8.setOri(orientation + negvar0[1])
                    grating9.setOri(orientation + negvar0[2])
                    grating1.setOri(orientation + negvar0[3])
                    grating2.setOri(orientation + negvar0[4])
                    grating3.setOri(orientation + negvar0[5])
                    grating4.setOri(orientation + negvar0[6])
                    grating5.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + negvar1[0])
                    grating8.setOri(orientation + negvar1[1])
                    grating9.setOri(orientation + negvar1[2])
                    grating1.setOri(orientation + negvar1[3])
                    grating2.setOri(orientation + negvar1[4])
                    grating3.setOri(orientation + negvar1[5])
                    grating4.setOri(orientation + negvar1[6])
                    grating5.setOri(orientation + negvar1[7])
        elif position == 7:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar0[0])
                    grating9.setOri(orientation + posvar0[1])
                    grating1.setOri(orientation + posvar0[2])
                    grating2.setOri(orientation + posvar0[3])
                    grating3.setOri(orientation + posvar0[4])
                    grating4.setOri(orientation + posvar0[5])
                    grating5.setOri(orientation + posvar0[6])
                    grating6.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar1[0])
                    grating9.setOri(orientation + posvar1[1])
                    grating1.setOri(orientation + posvar1[2])
                    grating2.setOri(orientation + posvar1[3])
                    grating3.setOri(orientation + posvar1[4])
                    grating4.setOri(orientation + posvar1[5])
                    grating5.setOri(orientation + posvar1[6])
                    grating6.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + negvar0[0])
                    grating9.setOri(orientation + negvar0[1])
                    grating1.setOri(orientation + negvar0[2])
                    grating2.setOri(orientation + negvar0[3])
                    grating3.setOri(orientation + negvar0[4])
                    grating4.setOri(orientation + negvar0[5])
                    grating5.setOri(orientation + negvar0[6])
                    grating6.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + negvar1[0])
                    grating9.setOri(orientation + negvar1[1])
                    grating1.setOri(orientation + negvar1[2])
                    grating2.setOri(orientation + negvar1[3])
                    grating3.setOri(orientation + negvar1[4])
                    grating4.setOri(orientation + negvar1[5])
                    grating5.setOri(orientation + negvar1[6])
                    grating6.setOri(orientation + negvar1[7])
        elif position == 8:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar0[0])
                    grating1.setOri(orientation + posvar0[1])
                    grating2.setOri(orientation + posvar0[2])
                    grating3.setOri(orientation + posvar0[3])
                    grating4.setOri(orientation + posvar0[4])
                    grating5.setOri(orientation + posvar0[5])
                    grating6.setOri(orientation + posvar0[6])
                    grating7.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar1[0])
                    grating1.setOri(orientation + posvar1[1])
                    grating2.setOri(orientation + posvar1[2])
                    grating3.setOri(orientation + posvar1[3])
                    grating4.setOri(orientation + posvar1[4])
                    grating5.setOri(orientation + posvar1[5])
                    grating6.setOri(orientation + posvar1[6])
                    grating7.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + negvar0[0])
                    grating1.setOri(orientation + negvar0[1])
                    grating2.setOri(orientation + negvar0[2])
                    grating3.setOri(orientation + negvar0[3])
                    grating4.setOri(orientation + negvar0[4])
                    grating5.setOri(orientation + negvar0[5])
                    grating6.setOri(orientation + negvar0[6])
                    grating7.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + negvar1[0])
                    grating1.setOri(orientation + negvar1[1])
                    grating2.setOri(orientation + negvar1[2])
                    grating3.setOri(orientation + negvar1[3])
                    grating4.setOri(orientation + negvar1[4])
                    grating5.setOri(orientation + negvar1[5])
                    grating6.setOri(orientation + negvar1[6])
                    grating7.setOri(orientation + negvar1[7])
        elif position == 9:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar0[0])
                    grating2.setOri(orientation + posvar0[1])
                    grating3.setOri(orientation + posvar0[2])
                    grating4.setOri(orientation + posvar0[3])
                    grating5.setOri(orientation + posvar0[4])
                    grating6.setOri(orientation + posvar0[5])
                    grating7.setOri(orientation + posvar0[6])
                    grating8.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar1[0])
                    grating2.setOri(orientation + posvar1[1])
                    grating3.setOri(orientation + posvar1[2])
                    grating4.setOri(orientation + posvar1[3])
                    grating5.setOri(orientation + posvar1[4])
                    grating6.setOri(orientation + posvar1[5])
                    grating7.setOri(orientation + posvar1[6])
                    grating8.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + negvar0[0])
                    grating2.setOri(orientation + negvar0[1])
                    grating3.setOri(orientation + negvar0[2])
                    grating4.setOri(orientation + negvar0[3])
                    grating5.setOri(orientation + negvar0[4])
                    grating6.setOri(orientation + negvar0[5])
                    grating7.setOri(orientation + negvar0[6])
                    grating8.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + negvar1[0])
                    grating2.setOri(orientation + negvar1[1])
                    grating3.setOri(orientation + negvar1[2])
                    grating4.setOri(orientation + negvar1[3])
                    grating5.setOri(orientation + negvar1[4])
                    grating6.setOri(orientation + negvar1[5])
                    grating7.setOri(orientation + negvar1[6])
                    grating8.setOri(orientation + negvar1[7])
    elif orientation == -5:
        posvar0 = [20, 40, 40, 60, -40, -60, -40, -20]
        posvar1 = [40, 40, 60, -20, -20, -20, -40, -40]
        negvar0 = [10, 20, 20, -20, -20, -20, -40, -40]
        negvar1 = [0, 0, 10, 20, -20, -20, -40, -40]
        if position == 1:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar0[0])
                    grating3.setOri(orientation + posvar0[1])
                    grating4.setOri(orientation + posvar0[2])
                    grating5.setOri(orientation + posvar0[3])
                    grating6.setOri(orientation + posvar0[4])
                    grating7.setOri(orientation + posvar0[5])
                    grating8.setOri(orientation + posvar0[6])
                    grating9.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar1[0])
                    grating3.setOri(orientation + posvar1[1])
                    grating4.setOri(orientation + posvar1[2])
                    grating5.setOri(orientation + posvar1[3])
                    grating6.setOri(orientation + posvar1[4])
                    grating7.setOri(orientation + posvar1[5])
                    grating8.setOri(orientation + posvar1[6])
                    grating9.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - negvar0[0])
                    grating3.setOri(orientation - negvar0[1])
                    grating4.setOri(orientation - negvar0[2])
                    grating5.setOri(orientation - negvar0[3])
                    grating6.setOri(orientation - negvar0[4])
                    grating7.setOri(orientation - negvar0[5])
                    grating8.setOri(orientation - negvar0[6])
                    grating9.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - negvar1[0])
                    grating3.setOri(orientation - negvar1[1])
                    grating4.setOri(orientation - negvar1[2])
                    grating5.setOri(orientation - negvar1[3])
                    grating6.setOri(orientation - negvar1[4])
                    grating7.setOri(orientation - negvar1[5])
                    grating8.setOri(orientation - negvar1[6])
                    grating9.setOri(orientation - negvar1[7])
        elif position == 2:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar0[0])
                    grating4.setOri(orientation + posvar0[1])
                    grating5.setOri(orientation + posvar0[2])
                    grating6.setOri(orientation + posvar0[3])
                    grating7.setOri(orientation + posvar0[4])
                    grating8.setOri(orientation + posvar0[5])
                    grating9.setOri(orientation + posvar0[6])
                    grating1.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar1[0])
                    grating4.setOri(orientation + posvar1[1])
                    grating5.setOri(orientation + posvar1[2])
                    grating6.setOri(orientation + posvar1[3])
                    grating7.setOri(orientation + posvar1[4])
                    grating8.setOri(orientation + posvar1[5])
                    grating9.setOri(orientation + posvar1[6])
                    grating1.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - negvar0[0])
                    grating4.setOri(orientation - negvar0[1])
                    grating5.setOri(orientation - negvar0[2])
                    grating6.setOri(orientation - negvar0[3])
                    grating7.setOri(orientation - negvar0[4])
                    grating8.setOri(orientation - negvar0[5])
                    grating9.setOri(orientation - negvar0[6])
                    grating1.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - negvar1[0])
                    grating4.setOri(orientation - negvar1[1])
                    grating5.setOri(orientation - negvar1[2])
                    grating6.setOri(orientation - negvar1[3])
                    grating7.setOri(orientation - negvar1[4])
                    grating8.setOri(orientation - negvar1[5])
                    grating9.setOri(orientation - negvar1[6])
                    grating1.setOri(orientation - negvar1[7])
        elif position == 3:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar0[0])
                    grating5.setOri(orientation + posvar0[1])
                    grating6.setOri(orientation + posvar0[2])
                    grating7.setOri(orientation + posvar0[3])
                    grating8.setOri(orientation + posvar0[4])
                    grating9.setOri(orientation + posvar0[5])
                    grating1.setOri(orientation + posvar0[6])
                    grating2.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar1[0])
                    grating5.setOri(orientation + posvar1[1])
                    grating6.setOri(orientation + posvar1[2])
                    grating7.setOri(orientation + posvar1[3])
                    grating8.setOri(orientation + posvar1[4])
                    grating9.setOri(orientation + posvar1[5])
                    grating1.setOri(orientation + posvar1[6])
                    grating2.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - negvar0[0])
                    grating5.setOri(orientation - negvar0[1])
                    grating6.setOri(orientation - negvar0[2])
                    grating7.setOri(orientation - negvar0[3])
                    grating8.setOri(orientation - negvar0[4])
                    grating9.setOri(orientation - negvar0[5])
                    grating1.setOri(orientation - negvar0[6])
                    grating2.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - negvar1[0])
                    grating5.setOri(orientation - negvar1[1])
                    grating6.setOri(orientation - negvar1[2])
                    grating7.setOri(orientation - negvar1[3])
                    grating8.setOri(orientation - negvar1[4])
                    grating9.setOri(orientation - negvar1[5])
                    grating1.setOri(orientation - negvar1[6])
                    grating2.setOri(orientation - negvar1[7])
        elif position == 4:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar0[0])
                    grating6.setOri(orientation + posvar0[1])
                    grating7.setOri(orientation + posvar0[2])
                    grating8.setOri(orientation + posvar0[3])
                    grating9.setOri(orientation + posvar0[4])
                    grating1.setOri(orientation + posvar0[5])
                    grating2.setOri(orientation + posvar0[6])
                    grating3.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar1[0])
                    grating6.setOri(orientation + posvar1[1])
                    grating7.setOri(orientation + posvar1[2])
                    grating8.setOri(orientation + posvar1[3])
                    grating9.setOri(orientation + posvar1[4])
                    grating1.setOri(orientation + posvar1[5])
                    grating2.setOri(orientation + posvar1[6])
                    grating3.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - negvar0[0])
                    grating6.setOri(orientation - negvar0[1])
                    grating7.setOri(orientation - negvar0[2])
                    grating8.setOri(orientation - negvar0[3])
                    grating9.setOri(orientation - negvar0[4])
                    grating1.setOri(orientation - negvar0[5])
                    grating2.setOri(orientation - negvar0[6])
                    grating3.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - negvar1[0])
                    grating6.setOri(orientation - negvar1[1])
                    grating7.setOri(orientation - negvar1[2])
                    grating8.setOri(orientation - negvar1[3])
                    grating9.setOri(orientation - negvar1[4])
                    grating1.setOri(orientation - negvar1[5])
                    grating2.setOri(orientation - negvar1[6])
                    grating3.setOri(orientation - negvar1[7])
        elif position == 5:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar0[0])
                    grating7.setOri(orientation + posvar0[1])
                    grating8.setOri(orientation + posvar0[2])
                    grating9.setOri(orientation + posvar0[3])
                    grating1.setOri(orientation + posvar0[4])
                    grating2.setOri(orientation + posvar0[5])
                    grating3.setOri(orientation + posvar0[6])
                    grating4.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar1[0])
                    grating7.setOri(orientation + posvar1[1])
                    grating8.setOri(orientation + posvar1[2])
                    grating9.setOri(orientation + posvar1[3])
                    grating1.setOri(orientation + posvar1[4])
                    grating2.setOri(orientation + posvar1[5])
                    grating3.setOri(orientation + posvar1[6])
                    grating4.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - negvar0[0])
                    grating7.setOri(orientation - negvar0[1])
                    grating8.setOri(orientation - negvar0[2])
                    grating9.setOri(orientation - negvar0[3])
                    grating1.setOri(orientation - negvar0[4])
                    grating2.setOri(orientation - negvar0[5])
                    grating3.setOri(orientation - negvar0[6])
                    grating4.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - negvar1[0])
                    grating7.setOri(orientation - negvar1[1])
                    grating8.setOri(orientation - negvar1[2])
                    grating9.setOri(orientation - negvar1[3])
                    grating1.setOri(orientation - negvar1[4])
                    grating2.setOri(orientation - negvar1[5])
                    grating3.setOri(orientation - negvar1[6])
                    grating4.setOri(orientation - negvar1[7])
        elif position == 6:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar0[0])
                    grating8.setOri(orientation + posvar0[1])
                    grating9.setOri(orientation + posvar0[2])
                    grating1.setOri(orientation + posvar0[3])
                    grating2.setOri(orientation + posvar0[4])
                    grating3.setOri(orientation + posvar0[5])
                    grating4.setOri(orientation + posvar0[6])
                    grating5.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar1[0])
                    grating8.setOri(orientation + posvar1[1])
                    grating9.setOri(orientation + posvar1[2])
                    grating1.setOri(orientation + posvar1[3])
                    grating2.setOri(orientation + posvar1[4])
                    grating3.setOri(orientation + posvar1[5])
                    grating4.setOri(orientation + posvar1[6])
                    grating5.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - negvar0[0])
                    grating8.setOri(orientation - negvar0[1])
                    grating9.setOri(orientation - negvar0[2])
                    grating1.setOri(orientation - negvar0[3])
                    grating2.setOri(orientation - negvar0[4])
                    grating3.setOri(orientation - negvar0[5])
                    grating4.setOri(orientation - negvar0[6])
                    grating5.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - negvar1[0])
                    grating8.setOri(orientation - negvar1[1])
                    grating9.setOri(orientation - negvar1[2])
                    grating1.setOri(orientation - negvar1[3])
                    grating2.setOri(orientation - negvar1[4])
                    grating3.setOri(orientation - negvar1[5])
                    grating4.setOri(orientation - negvar1[6])
                    grating5.setOri(orientation - negvar1[7])
        elif position == 7:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar0[0])
                    grating9.setOri(orientation + posvar0[1])
                    grating1.setOri(orientation + posvar0[2])
                    grating2.setOri(orientation + posvar0[3])
                    grating3.setOri(orientation + posvar0[4])
                    grating4.setOri(orientation + posvar0[5])
                    grating5.setOri(orientation + posvar0[6])
                    grating6.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar1[0])
                    grating9.setOri(orientation + posvar1[1])
                    grating1.setOri(orientation + posvar1[2])
                    grating2.setOri(orientation + posvar1[3])
                    grating3.setOri(orientation + posvar1[4])
                    grating4.setOri(orientation + posvar1[5])
                    grating5.setOri(orientation + posvar1[6])
                    grating6.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - negvar0[0])
                    grating9.setOri(orientation - negvar0[1])
                    grating1.setOri(orientation - negvar0[2])
                    grating2.setOri(orientation - negvar0[3])
                    grating3.setOri(orientation - negvar0[4])
                    grating4.setOri(orientation - negvar0[5])
                    grating5.setOri(orientation - negvar0[6])
                    grating6.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - negvar1[0])
                    grating9.setOri(orientation - negvar1[1])
                    grating1.setOri(orientation - negvar1[2])
                    grating2.setOri(orientation - negvar1[3])
                    grating3.setOri(orientation - negvar1[4])
                    grating4.setOri(orientation - negvar1[5])
                    grating5.setOri(orientation - negvar1[6])
                    grating6.setOri(orientation - negvar1[7])
        elif position == 8:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar0[0])
                    grating1.setOri(orientation + posvar0[1])
                    grating2.setOri(orientation + posvar0[2])
                    grating3.setOri(orientation + posvar0[3])
                    grating4.setOri(orientation + posvar0[4])
                    grating5.setOri(orientation + posvar0[5])
                    grating6.setOri(orientation + posvar0[6])
                    grating7.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar1[0])
                    grating1.setOri(orientation + posvar1[1])
                    grating2.setOri(orientation + posvar1[2])
                    grating3.setOri(orientation + posvar1[3])
                    grating4.setOri(orientation + posvar1[4])
                    grating5.setOri(orientation + posvar1[5])
                    grating6.setOri(orientation + posvar1[6])
                    grating7.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - negvar0[0])
                    grating1.setOri(orientation - negvar0[1])
                    grating2.setOri(orientation - negvar0[2])
                    grating3.setOri(orientation - negvar0[3])
                    grating4.setOri(orientation - negvar0[4])
                    grating5.setOri(orientation - negvar0[5])
                    grating6.setOri(orientation - negvar0[6])
                    grating7.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - negvar1[0])
                    grating1.setOri(orientation - negvar1[1])
                    grating2.setOri(orientation - negvar1[2])
                    grating3.setOri(orientation - negvar1[3])
                    grating4.setOri(orientation - negvar1[4])
                    grating5.setOri(orientation - negvar1[5])
                    grating6.setOri(orientation - negvar1[6])
                    grating7.setOri(orientation - negvar1[7])
        elif position == 9:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar0[0])
                    grating2.setOri(orientation + posvar0[1])
                    grating3.setOri(orientation + posvar0[2])
                    grating4.setOri(orientation + posvar0[3])
                    grating5.setOri(orientation + posvar0[4])
                    grating6.setOri(orientation + posvar0[5])
                    grating7.setOri(orientation + posvar0[6])
                    grating8.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar1[0])
                    grating2.setOri(orientation + posvar1[1])
                    grating3.setOri(orientation + posvar1[2])
                    grating4.setOri(orientation + posvar1[3])
                    grating5.setOri(orientation + posvar1[4])
                    grating6.setOri(orientation + posvar1[5])
                    grating7.setOri(orientation + posvar1[6])
                    grating8.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - negvar0[0])
                    grating2.setOri(orientation - negvar0[1])
                    grating3.setOri(orientation - negvar0[2])
                    grating4.setOri(orientation - negvar0[3])
                    grating5.setOri(orientation - negvar0[4])
                    grating6.setOri(orientation - negvar0[5])
                    grating7.setOri(orientation - negvar0[6])
                    grating8.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - negvar1[0])
                    grating2.setOri(orientation - negvar1[1])
                    grating3.setOri(orientation - negvar1[2])
                    grating4.setOri(orientation - negvar1[3])
                    grating5.setOri(orientation - negvar1[4])
                    grating6.setOri(orientation - negvar1[5])
                    grating7.setOri(orientation - negvar1[6])
                    grating8.setOri(orientation - negvar1[7])
    elif orientation == 10 or orientation == 20:
        posvar0 = [20, 40, 40, 60, -20, -40, -40, -60]
        posvar1 = [40, 40, 60, -20, -20, -20, -40, -40]
        negvar0 = [0, 20, 20, -40, -40, -40, -40, -60]
        negvar1 = [0, 0, 0, 20, -40, -40, -60, -60]
        if position == 1:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar0[0])
                    grating3.setOri(orientation + posvar0[1])
                    grating4.setOri(orientation + posvar0[2])
                    grating5.setOri(orientation + posvar0[3])
                    grating6.setOri(orientation + posvar0[4])
                    grating7.setOri(orientation + posvar0[5])
                    grating8.setOri(orientation + posvar0[6])
                    grating9.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar1[0])
                    grating3.setOri(orientation + posvar1[1])
                    grating4.setOri(orientation + posvar1[2])
                    grating5.setOri(orientation + posvar1[3])
                    grating6.setOri(orientation + posvar1[4])
                    grating7.setOri(orientation + posvar1[5])
                    grating8.setOri(orientation + posvar1[6])
                    grating9.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + negvar0[0])
                    grating3.setOri(orientation + negvar0[1])
                    grating4.setOri(orientation + negvar0[2])
                    grating5.setOri(orientation + negvar0[3])
                    grating6.setOri(orientation + negvar0[4])
                    grating7.setOri(orientation + negvar0[5])
                    grating8.setOri(orientation + negvar0[6])
                    grating9.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + negvar1[0])
                    grating3.setOri(orientation + negvar1[1])
                    grating4.setOri(orientation + negvar1[2])
                    grating5.setOri(orientation + negvar1[3])
                    grating6.setOri(orientation + negvar1[4])
                    grating7.setOri(orientation + negvar1[5])
                    grating8.setOri(orientation + negvar1[6])
                    grating9.setOri(orientation + negvar1[7])
        elif position == 2:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar0[0])
                    grating4.setOri(orientation + posvar0[1])
                    grating5.setOri(orientation + posvar0[2])
                    grating6.setOri(orientation + posvar0[3])
                    grating7.setOri(orientation + posvar0[4])
                    grating8.setOri(orientation + posvar0[5])
                    grating9.setOri(orientation + posvar0[6])
                    grating1.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar1[0])
                    grating4.setOri(orientation + posvar1[1])
                    grating5.setOri(orientation + posvar1[2])
                    grating6.setOri(orientation + posvar1[3])
                    grating7.setOri(orientation + posvar1[4])
                    grating8.setOri(orientation + posvar1[5])
                    grating9.setOri(orientation + posvar1[6])
                    grating1.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + negvar0[0])
                    grating4.setOri(orientation + negvar0[1])
                    grating5.setOri(orientation + negvar0[2])
                    grating6.setOri(orientation + negvar0[3])
                    grating7.setOri(orientation + negvar0[4])
                    grating8.setOri(orientation + negvar0[5])
                    grating9.setOri(orientation + negvar0[6])
                    grating1.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + negvar1[0])
                    grating4.setOri(orientation + negvar1[1])
                    grating5.setOri(orientation + negvar1[2])
                    grating6.setOri(orientation + negvar1[3])
                    grating7.setOri(orientation + negvar1[4])
                    grating8.setOri(orientation + negvar1[5])
                    grating9.setOri(orientation + negvar1[6])
                    grating1.setOri(orientation + negvar1[7])
        elif position == 3:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar0[0])
                    grating5.setOri(orientation + posvar0[1])
                    grating6.setOri(orientation + posvar0[2])
                    grating7.setOri(orientation + posvar0[3])
                    grating8.setOri(orientation + posvar0[4])
                    grating9.setOri(orientation + posvar0[5])
                    grating1.setOri(orientation + posvar0[6])
                    grating2.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar1[0])
                    grating5.setOri(orientation + posvar1[1])
                    grating6.setOri(orientation + posvar1[2])
                    grating7.setOri(orientation + posvar1[3])
                    grating8.setOri(orientation + posvar1[4])
                    grating9.setOri(orientation + posvar1[5])
                    grating1.setOri(orientation + posvar1[6])
                    grating2.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + negvar0[0])
                    grating5.setOri(orientation + negvar0[1])
                    grating6.setOri(orientation + negvar0[2])
                    grating7.setOri(orientation + negvar0[3])
                    grating8.setOri(orientation + negvar0[4])
                    grating9.setOri(orientation + negvar0[5])
                    grating1.setOri(orientation + negvar0[6])
                    grating2.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + negvar1[0])
                    grating5.setOri(orientation + negvar1[1])
                    grating6.setOri(orientation + negvar1[2])
                    grating7.setOri(orientation + negvar1[3])
                    grating8.setOri(orientation + negvar1[4])
                    grating9.setOri(orientation + negvar1[5])
                    grating1.setOri(orientation + negvar1[6])
                    grating2.setOri(orientation + negvar1[7])
        elif position == 4:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar0[0])
                    grating6.setOri(orientation + posvar0[1])
                    grating7.setOri(orientation + posvar0[2])
                    grating8.setOri(orientation + posvar0[3])
                    grating9.setOri(orientation + posvar0[4])
                    grating1.setOri(orientation + posvar0[5])
                    grating2.setOri(orientation + posvar0[6])
                    grating3.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar1[0])
                    grating6.setOri(orientation + posvar1[1])
                    grating7.setOri(orientation + posvar1[2])
                    grating8.setOri(orientation + posvar1[3])
                    grating9.setOri(orientation + posvar1[4])
                    grating1.setOri(orientation + posvar1[5])
                    grating2.setOri(orientation + posvar1[6])
                    grating3.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + negvar0[0])
                    grating6.setOri(orientation + negvar0[1])
                    grating7.setOri(orientation + negvar0[2])
                    grating8.setOri(orientation + negvar0[3])
                    grating9.setOri(orientation + negvar0[4])
                    grating1.setOri(orientation + negvar0[5])
                    grating2.setOri(orientation + negvar0[6])
                    grating3.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + negvar1[0])
                    grating6.setOri(orientation + negvar1[1])
                    grating7.setOri(orientation + negvar1[2])
                    grating8.setOri(orientation + negvar1[3])
                    grating9.setOri(orientation + negvar1[4])
                    grating1.setOri(orientation + negvar1[5])
                    grating2.setOri(orientation + negvar1[6])
                    grating3.setOri(orientation + negvar1[7])
        elif position == 5:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar0[0])
                    grating7.setOri(orientation + posvar0[1])
                    grating8.setOri(orientation + posvar0[2])
                    grating9.setOri(orientation + posvar0[3])
                    grating1.setOri(orientation + posvar0[4])
                    grating2.setOri(orientation + posvar0[5])
                    grating3.setOri(orientation + posvar0[6])
                    grating4.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar1[0])
                    grating7.setOri(orientation + posvar1[1])
                    grating8.setOri(orientation + posvar1[2])
                    grating9.setOri(orientation + posvar1[3])
                    grating1.setOri(orientation + posvar1[4])
                    grating2.setOri(orientation + posvar1[5])
                    grating3.setOri(orientation + posvar1[6])
                    grating4.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + negvar0[0])
                    grating7.setOri(orientation + negvar0[1])
                    grating8.setOri(orientation + negvar0[2])
                    grating9.setOri(orientation + negvar0[3])
                    grating1.setOri(orientation + negvar0[4])
                    grating2.setOri(orientation + negvar0[5])
                    grating3.setOri(orientation + negvar0[6])
                    grating4.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + negvar1[0])
                    grating7.setOri(orientation + negvar1[1])
                    grating8.setOri(orientation + negvar1[2])
                    grating9.setOri(orientation + negvar1[3])
                    grating1.setOri(orientation + negvar1[4])
                    grating2.setOri(orientation + negvar1[5])
                    grating3.setOri(orientation + negvar1[6])
                    grating4.setOri(orientation + negvar1[7])
        elif position == 6:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar0[0])
                    grating8.setOri(orientation + posvar0[1])
                    grating9.setOri(orientation + posvar0[2])
                    grating1.setOri(orientation + posvar0[3])
                    grating2.setOri(orientation + posvar0[4])
                    grating3.setOri(orientation + posvar0[5])
                    grating4.setOri(orientation + posvar0[6])
                    grating5.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar1[0])
                    grating8.setOri(orientation + posvar1[1])
                    grating9.setOri(orientation + posvar1[2])
                    grating1.setOri(orientation + posvar1[3])
                    grating2.setOri(orientation + posvar1[4])
                    grating3.setOri(orientation + posvar1[5])
                    grating4.setOri(orientation + posvar1[6])
                    grating5.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + negvar0[0])
                    grating8.setOri(orientation + negvar0[1])
                    grating9.setOri(orientation + negvar0[2])
                    grating1.setOri(orientation + negvar0[3])
                    grating2.setOri(orientation + negvar0[4])
                    grating3.setOri(orientation + negvar0[5])
                    grating4.setOri(orientation + negvar0[6])
                    grating5.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + negvar1[0])
                    grating8.setOri(orientation + negvar1[1])
                    grating9.setOri(orientation + negvar1[2])
                    grating1.setOri(orientation + negvar1[3])
                    grating2.setOri(orientation + negvar1[4])
                    grating3.setOri(orientation + negvar1[5])
                    grating4.setOri(orientation + negvar1[6])
                    grating5.setOri(orientation + negvar1[7])
        elif position == 7:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar0[0])
                    grating9.setOri(orientation + posvar0[1])
                    grating1.setOri(orientation + posvar0[2])
                    grating2.setOri(orientation + posvar0[3])
                    grating3.setOri(orientation + posvar0[4])
                    grating4.setOri(orientation + posvar0[5])
                    grating5.setOri(orientation + posvar0[6])
                    grating6.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar1[0])
                    grating9.setOri(orientation + posvar1[1])
                    grating1.setOri(orientation + posvar1[2])
                    grating2.setOri(orientation + posvar1[3])
                    grating3.setOri(orientation + posvar1[4])
                    grating4.setOri(orientation + posvar1[5])
                    grating5.setOri(orientation + posvar1[6])
                    grating6.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + negvar0[0])
                    grating9.setOri(orientation + negvar0[1])
                    grating1.setOri(orientation + negvar0[2])
                    grating2.setOri(orientation + negvar0[3])
                    grating3.setOri(orientation + negvar0[4])
                    grating4.setOri(orientation + negvar0[5])
                    grating5.setOri(orientation + negvar0[6])
                    grating6.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + negvar1[0])
                    grating9.setOri(orientation + negvar1[1])
                    grating1.setOri(orientation + negvar1[2])
                    grating2.setOri(orientation + negvar1[3])
                    grating3.setOri(orientation + negvar1[4])
                    grating4.setOri(orientation + negvar1[5])
                    grating5.setOri(orientation + negvar1[6])
                    grating6.setOri(orientation + negvar1[7])
        elif position == 8:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar0[0])
                    grating1.setOri(orientation + posvar0[1])
                    grating2.setOri(orientation + posvar0[2])
                    grating3.setOri(orientation + posvar0[3])
                    grating4.setOri(orientation + posvar0[4])
                    grating5.setOri(orientation + posvar0[5])
                    grating6.setOri(orientation + posvar0[6])
                    grating7.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar1[0])
                    grating1.setOri(orientation + posvar1[1])
                    grating2.setOri(orientation + posvar1[2])
                    grating3.setOri(orientation + posvar1[3])
                    grating4.setOri(orientation + posvar1[4])
                    grating5.setOri(orientation + posvar1[5])
                    grating6.setOri(orientation + posvar1[6])
                    grating7.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + negvar0[0])
                    grating1.setOri(orientation + negvar0[1])
                    grating2.setOri(orientation + negvar0[2])
                    grating3.setOri(orientation + negvar0[3])
                    grating4.setOri(orientation + negvar0[4])
                    grating5.setOri(orientation + negvar0[5])
                    grating6.setOri(orientation + negvar0[6])
                    grating7.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + negvar1[0])
                    grating1.setOri(orientation + negvar1[1])
                    grating2.setOri(orientation + negvar1[2])
                    grating3.setOri(orientation + negvar1[3])
                    grating4.setOri(orientation + negvar1[4])
                    grating5.setOri(orientation + negvar1[5])
                    grating6.setOri(orientation + negvar1[6])
                    grating7.setOri(orientation + negvar1[7])
        elif position == 9:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar0[0])
                    grating2.setOri(orientation + posvar0[1])
                    grating3.setOri(orientation + posvar0[2])
                    grating4.setOri(orientation + posvar0[3])
                    grating5.setOri(orientation + posvar0[4])
                    grating6.setOri(orientation + posvar0[5])
                    grating7.setOri(orientation + posvar0[6])
                    grating8.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar1[0])
                    grating2.setOri(orientation + posvar1[1])
                    grating3.setOri(orientation + posvar1[2])
                    grating4.setOri(orientation + posvar1[3])
                    grating5.setOri(orientation + posvar1[4])
                    grating6.setOri(orientation + posvar1[5])
                    grating7.setOri(orientation + posvar1[6])
                    grating8.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + negvar0[0])
                    grating2.setOri(orientation + negvar0[1])
                    grating3.setOri(orientation + negvar0[2])
                    grating4.setOri(orientation + negvar0[3])
                    grating5.setOri(orientation + negvar0[4])
                    grating6.setOri(orientation + negvar0[5])
                    grating7.setOri(orientation + negvar0[6])
                    grating8.setOri(orientation + negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + negvar1[0])
                    grating2.setOri(orientation + negvar1[1])
                    grating3.setOri(orientation + negvar1[2])
                    grating4.setOri(orientation + negvar1[3])
                    grating5.setOri(orientation + negvar1[4])
                    grating6.setOri(orientation + negvar1[5])
                    grating7.setOri(orientation + negvar1[6])
                    grating8.setOri(orientation + negvar1[7])
    elif orientation == -10 or orientation == -20:
        posvar0 = [20, 40, 40, 60, -20, -40, -40, -60]
        posvar1 = [40, 40, 60, -20, -20, -20, -40, -40]
        negvar0 = [0, 20, 20, -40, -40, -40, -40, -60]
        negvar1 = [0, 0, 0, 20, -40, -40, -60, -60]
        if position == 1:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar0[0])
                    grating3.setOri(orientation + posvar0[1])
                    grating4.setOri(orientation + posvar0[2])
                    grating5.setOri(orientation + posvar0[3])
                    grating6.setOri(orientation + posvar0[4])
                    grating7.setOri(orientation + posvar0[5])
                    grating8.setOri(orientation + posvar0[6])
                    grating9.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation + posvar1[0])
                    grating3.setOri(orientation + posvar1[1])
                    grating4.setOri(orientation + posvar1[2])
                    grating5.setOri(orientation + posvar1[3])
                    grating6.setOri(orientation + posvar1[4])
                    grating7.setOri(orientation + posvar1[5])
                    grating8.setOri(orientation + posvar1[6])
                    grating9.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - negvar0[0])
                    grating3.setOri(orientation - negvar0[1])
                    grating4.setOri(orientation - negvar0[2])
                    grating5.setOri(orientation - negvar0[3])
                    grating6.setOri(orientation - negvar0[4])
                    grating7.setOri(orientation - negvar0[5])
                    grating8.setOri(orientation - negvar0[6])
                    grating9.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating1.setOri(orientation)
                    grating2.setOri(orientation - negvar1[0])
                    grating3.setOri(orientation - negvar1[1])
                    grating4.setOri(orientation - negvar1[2])
                    grating5.setOri(orientation - negvar1[3])
                    grating6.setOri(orientation - negvar1[4])
                    grating7.setOri(orientation - negvar1[5])
                    grating8.setOri(orientation - negvar1[6])
                    grating9.setOri(orientation - negvar1[7])
        elif position == 2:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar0[0])
                    grating4.setOri(orientation + posvar0[1])
                    grating5.setOri(orientation + posvar0[2])
                    grating6.setOri(orientation + posvar0[3])
                    grating7.setOri(orientation + posvar0[4])
                    grating8.setOri(orientation + posvar0[5])
                    grating9.setOri(orientation + posvar0[6])
                    grating1.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation + posvar1[0])
                    grating4.setOri(orientation + posvar1[1])
                    grating5.setOri(orientation + posvar1[2])
                    grating6.setOri(orientation + posvar1[3])
                    grating7.setOri(orientation + posvar1[4])
                    grating8.setOri(orientation + posvar1[5])
                    grating9.setOri(orientation + posvar1[6])
                    grating1.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - negvar0[0])
                    grating4.setOri(orientation - negvar0[1])
                    grating5.setOri(orientation - negvar0[2])
                    grating6.setOri(orientation - negvar0[3])
                    grating7.setOri(orientation - negvar0[4])
                    grating8.setOri(orientation - negvar0[5])
                    grating9.setOri(orientation - negvar0[6])
                    grating1.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating2.setOri(orientation)
                    grating3.setOri(orientation - negvar1[0])
                    grating4.setOri(orientation - negvar1[1])
                    grating5.setOri(orientation - negvar1[2])
                    grating6.setOri(orientation - negvar1[3])
                    grating7.setOri(orientation - negvar1[4])
                    grating8.setOri(orientation - negvar1[5])
                    grating9.setOri(orientation - negvar1[6])
                    grating1.setOri(orientation - negvar1[7])
        elif position == 3:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar0[0])
                    grating5.setOri(orientation + posvar0[1])
                    grating6.setOri(orientation + posvar0[2])
                    grating7.setOri(orientation + posvar0[3])
                    grating8.setOri(orientation + posvar0[4])
                    grating9.setOri(orientation + posvar0[5])
                    grating1.setOri(orientation + posvar0[6])
                    grating2.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation + posvar1[0])
                    grating5.setOri(orientation + posvar1[1])
                    grating6.setOri(orientation + posvar1[2])
                    grating7.setOri(orientation + posvar1[3])
                    grating8.setOri(orientation + posvar1[4])
                    grating9.setOri(orientation + posvar1[5])
                    grating1.setOri(orientation + posvar1[6])
                    grating2.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - negvar0[0])
                    grating5.setOri(orientation - negvar0[1])
                    grating6.setOri(orientation - negvar0[2])
                    grating7.setOri(orientation - negvar0[3])
                    grating8.setOri(orientation - negvar0[4])
                    grating9.setOri(orientation - negvar0[5])
                    grating1.setOri(orientation - negvar0[6])
                    grating2.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating3.setOri(orientation)
                    grating4.setOri(orientation - negvar1[0])
                    grating5.setOri(orientation - negvar1[1])
                    grating6.setOri(orientation - negvar1[2])
                    grating7.setOri(orientation - negvar1[3])
                    grating8.setOri(orientation - negvar1[4])
                    grating9.setOri(orientation - negvar1[5])
                    grating1.setOri(orientation - negvar1[6])
                    grating2.setOri(orientation - negvar1[7])
        elif position == 4:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar0[0])
                    grating6.setOri(orientation + posvar0[1])
                    grating7.setOri(orientation + posvar0[2])
                    grating8.setOri(orientation + posvar0[3])
                    grating9.setOri(orientation + posvar0[4])
                    grating1.setOri(orientation + posvar0[5])
                    grating2.setOri(orientation + posvar0[6])
                    grating3.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation + posvar1[0])
                    grating6.setOri(orientation + posvar1[1])
                    grating7.setOri(orientation + posvar1[2])
                    grating8.setOri(orientation + posvar1[3])
                    grating9.setOri(orientation + posvar1[4])
                    grating1.setOri(orientation + posvar1[5])
                    grating2.setOri(orientation + posvar1[6])
                    grating3.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - negvar0[0])
                    grating6.setOri(orientation - negvar0[1])
                    grating7.setOri(orientation - negvar0[2])
                    grating8.setOri(orientation - negvar0[3])
                    grating9.setOri(orientation - negvar0[4])
                    grating1.setOri(orientation - negvar0[5])
                    grating2.setOri(orientation - negvar0[6])
                    grating3.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating4.setOri(orientation)
                    grating5.setOri(orientation - negvar1[0])
                    grating6.setOri(orientation - negvar1[1])
                    grating7.setOri(orientation - negvar1[2])
                    grating8.setOri(orientation - negvar1[3])
                    grating9.setOri(orientation - negvar1[4])
                    grating1.setOri(orientation - negvar1[5])
                    grating2.setOri(orientation - negvar1[6])
                    grating3.setOri(orientation - negvar1[7])
        elif position == 5:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar0[0])
                    grating7.setOri(orientation + posvar0[1])
                    grating8.setOri(orientation + posvar0[2])
                    grating9.setOri(orientation + posvar0[3])
                    grating1.setOri(orientation + posvar0[4])
                    grating2.setOri(orientation + posvar0[5])
                    grating3.setOri(orientation + posvar0[6])
                    grating4.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation + posvar1[0])
                    grating7.setOri(orientation + posvar1[1])
                    grating8.setOri(orientation + posvar1[2])
                    grating9.setOri(orientation + posvar1[3])
                    grating1.setOri(orientation + posvar1[4])
                    grating2.setOri(orientation + posvar1[5])
                    grating3.setOri(orientation + posvar1[6])
                    grating4.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - negvar0[0])
                    grating7.setOri(orientation - negvar0[1])
                    grating8.setOri(orientation - negvar0[2])
                    grating9.setOri(orientation - negvar0[3])
                    grating1.setOri(orientation - negvar0[4])
                    grating2.setOri(orientation - negvar0[5])
                    grating3.setOri(orientation - negvar0[6])
                    grating4.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating5.setOri(orientation)
                    grating6.setOri(orientation - negvar1[0])
                    grating7.setOri(orientation - negvar1[1])
                    grating8.setOri(orientation - negvar1[2])
                    grating9.setOri(orientation - negvar1[3])
                    grating1.setOri(orientation - negvar1[4])
                    grating2.setOri(orientation - negvar1[5])
                    grating3.setOri(orientation - negvar1[6])
                    grating4.setOri(orientation - negvar1[7])
        elif position == 6:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar0[0])
                    grating8.setOri(orientation + posvar0[1])
                    grating9.setOri(orientation + posvar0[2])
                    grating1.setOri(orientation + posvar0[3])
                    grating2.setOri(orientation + posvar0[4])
                    grating3.setOri(orientation + posvar0[5])
                    grating4.setOri(orientation + posvar0[6])
                    grating5.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation + posvar1[0])
                    grating8.setOri(orientation + posvar1[1])
                    grating9.setOri(orientation + posvar1[2])
                    grating1.setOri(orientation + posvar1[3])
                    grating2.setOri(orientation + posvar1[4])
                    grating3.setOri(orientation + posvar1[5])
                    grating4.setOri(orientation + posvar1[6])
                    grating5.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - negvar0[0])
                    grating8.setOri(orientation - negvar0[1])
                    grating9.setOri(orientation - negvar0[2])
                    grating1.setOri(orientation - negvar0[3])
                    grating2.setOri(orientation - negvar0[4])
                    grating3.setOri(orientation - negvar0[5])
                    grating4.setOri(orientation - negvar0[6])
                    grating5.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating6.setOri(orientation)
                    grating7.setOri(orientation - negvar1[0])
                    grating8.setOri(orientation - negvar1[1])
                    grating9.setOri(orientation - negvar1[2])
                    grating1.setOri(orientation - negvar1[3])
                    grating2.setOri(orientation - negvar1[4])
                    grating3.setOri(orientation - negvar1[5])
                    grating4.setOri(orientation - negvar1[6])
                    grating5.setOri(orientation - negvar1[7])
        elif position == 7:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar0[0])
                    grating9.setOri(orientation + posvar0[1])
                    grating1.setOri(orientation + posvar0[2])
                    grating2.setOri(orientation + posvar0[3])
                    grating3.setOri(orientation + posvar0[4])
                    grating4.setOri(orientation + posvar0[5])
                    grating5.setOri(orientation + posvar0[6])
                    grating6.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation + posvar1[0])
                    grating9.setOri(orientation + posvar1[1])
                    grating1.setOri(orientation + posvar1[2])
                    grating2.setOri(orientation + posvar1[3])
                    grating3.setOri(orientation + posvar1[4])
                    grating4.setOri(orientation + posvar1[5])
                    grating5.setOri(orientation + posvar1[6])
                    grating6.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - negvar0[0])
                    grating9.setOri(orientation - negvar0[1])
                    grating1.setOri(orientation - negvar0[2])
                    grating2.setOri(orientation - negvar0[3])
                    grating3.setOri(orientation - negvar0[4])
                    grating4.setOri(orientation - negvar0[5])
                    grating5.setOri(orientation - negvar0[6])
                    grating6.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating7.setOri(orientation)
                    grating8.setOri(orientation - negvar1[0])
                    grating9.setOri(orientation - negvar1[1])
                    grating1.setOri(orientation - negvar1[2])
                    grating2.setOri(orientation - negvar1[3])
                    grating3.setOri(orientation - negvar1[4])
                    grating4.setOri(orientation - negvar1[5])
                    grating5.setOri(orientation - negvar1[6])
                    grating6.setOri(orientation - negvar1[7])
        elif position == 8:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar0[0])
                    grating1.setOri(orientation + posvar0[1])
                    grating2.setOri(orientation + posvar0[2])
                    grating3.setOri(orientation + posvar0[3])
                    grating4.setOri(orientation + posvar0[4])
                    grating5.setOri(orientation + posvar0[5])
                    grating6.setOri(orientation + posvar0[6])
                    grating7.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation + posvar1[0])
                    grating1.setOri(orientation + posvar1[1])
                    grating2.setOri(orientation + posvar1[2])
                    grating3.setOri(orientation + posvar1[3])
                    grating4.setOri(orientation + posvar1[4])
                    grating5.setOri(orientation + posvar1[5])
                    grating6.setOri(orientation + posvar1[6])
                    grating7.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - negvar0[0])
                    grating1.setOri(orientation - negvar0[1])
                    grating2.setOri(orientation - negvar0[2])
                    grating3.setOri(orientation - negvar0[3])
                    grating4.setOri(orientation - negvar0[4])
                    grating5.setOri(orientation - negvar0[5])
                    grating6.setOri(orientation - negvar0[6])
                    grating7.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating8.setOri(orientation)
                    grating9.setOri(orientation - negvar1[0])
                    grating1.setOri(orientation - negvar1[1])
                    grating2.setOri(orientation - negvar1[2])
                    grating3.setOri(orientation - negvar1[3])
                    grating4.setOri(orientation - negvar1[4])
                    grating5.setOri(orientation - negvar1[5])
                    grating6.setOri(orientation - negvar1[6])
                    grating7.setOri(orientation - negvar1[7])
        elif position == 9:
            if configuration == 0:
                if variation == 0:
                    np.random.shuffle(posvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar0[0])
                    grating2.setOri(orientation + posvar0[1])
                    grating3.setOri(orientation + posvar0[2])
                    grating4.setOri(orientation + posvar0[3])
                    grating5.setOri(orientation + posvar0[4])
                    grating6.setOri(orientation + posvar0[5])
                    grating7.setOri(orientation + posvar0[6])
                    grating8.setOri(orientation + posvar0[7])
                else:
                    np.random.shuffle(posvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation + posvar1[0])
                    grating2.setOri(orientation + posvar1[1])
                    grating3.setOri(orientation + posvar1[2])
                    grating4.setOri(orientation + posvar1[3])
                    grating5.setOri(orientation + posvar1[4])
                    grating6.setOri(orientation + posvar1[5])
                    grating7.setOri(orientation + posvar1[6])
                    grating8.setOri(orientation + posvar1[7])
            elif configuration == 1:
                if variation == 0:
                    np.random.shuffle(negvar0)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - negvar0[0])
                    grating2.setOri(orientation - negvar0[1])
                    grating3.setOri(orientation - negvar0[2])
                    grating4.setOri(orientation - negvar0[3])
                    grating5.setOri(orientation - negvar0[4])
                    grating6.setOri(orientation - negvar0[5])
                    grating7.setOri(orientation - negvar0[6])
                    grating8.setOri(orientation - negvar0[7])
                else:
                    np.random.shuffle(negvar1)
                    grating9.setOri(orientation)
                    grating1.setOri(orientation - negvar1[0])
                    grating2.setOri(orientation - negvar1[1])
                    grating3.setOri(orientation - negvar1[2])
                    grating4.setOri(orientation - negvar1[3])
                    grating5.setOri(orientation - negvar1[4])
                    grating6.setOri(orientation - negvar1[5])
                    grating7.setOri(orientation - negvar1[6])
                    grating8.setOri(orientation - negvar1[7])

    grating1.draw()
    grating2.draw()
    grating3.draw()
    grating4.draw()
    grating5.draw()
    grating6.draw()
    grating7.draw()
    grating8.draw()
    grating9.draw()


def debriefing():
    #  Debriefing Note
    debrief = visual.TextStim(win = win, text = ' ', font = 'Times New Roman',
                              pos = (0,0), color = 'black', units = 'deg',
                              height = 0.9, wrapWidth=20
                              )

    debrief.setText(debrief_text)
    debrief.draw()
    win.flip()
    core.wait(5)


def main():
    instruction()
    """
    This is the main trial loop.
    """
    for i in range(0, No_of_Trials):
        date_array.append(show_info[0])
        time_array.append(show_info[1])
        name_array.append(show_info[2])
        age_array.append(show_info[3])
        gender_array.append(show_info[4])
        hand_array.append(show_info[5])
        trial_no_array.append(i)
        condition_array.append(triallist[i][0])
        orientation_array.append(triallist[i][1])
        position_array.append(triallist[i][2])
        configuration_array.append(triallist[i][3])
        variation_array.append(triallist[i][4])

        fixation()
        win.flip()
        core.wait(fixation_time)

        precue(triallist[i][0], triallist[i][2])
        print(triallist[i])
        win.flip()
        core.wait(precue_time)

        gaborset(triallist[i][1], triallist[i][2], triallist[i][3], triallist[i][4])
        win.flip()
        core.wait(gaborset_time)

        win.flip()
        core.wait(blankscreen_time)

        postcue(triallist[i][0], triallist[i][2])
        win.flip()

        start_time = core.getTime(applyZero = True)

        resp = event.waitKeys(maxWait=1000, keyList=['end','f','j'],
                              clearEvents=True)
        print(resp)

        if 'end' in resp:
            # Exit Key
            # resp_time = core.getTime(applyZero = True) - start_time
            # response_array.append(resp[0])
            # latency_array.append(resp_time)
            # break
            win.close()
            sys.exit()

        elif 'f' in resp:
            # Anticlockwise response)
            resp_time = core.getTime(applyZero = True) - start_time
            response_array.append(resp[0])
            latency_array.append(resp_time)
            win.flip()
            core.wait(isi_time)
            if i in breaktrial:
                break_time(i)
                continue

        elif 'j' in resp:
            # Clockwise response
            resp_time = core.getTime(applyZero = True) - start_time
            response_array.append(resp[0])
            latency_array.append(resp_time)
            win.flip()
            core.wait(isi_time)
            if i in breaktrial:
                break_time(i)
                continue

    '''
    The main trial loop Ends Here.
    '''
    #  Creating the DataFrame & Save it
    outputfile = pd.DataFrame({'Exp_Date': date_array,
                               'Exp_Time': time_array,
                               'Sub_Name': name_array,
                               'Age': age_array,
                               'Gender': gender_array,
                               'Dominant_Hand': hand_array,
                               'Trial_No': trial_no_array,
                               'Condition': condition_array,
                               'Orientation': orientation_array,
                               'Position': position_array,
                               'Configuration': configuration_array,
                               'Variation': variation_array,
                               'Response': response_array,
                               'Latency': latency_array
                               })

    outputfile.to_csv(save_path, sep=',', index=False)

    debriefing()
    win.close()
    sys.exit()


if __name__ == '__main__':
    main()
