'''
Last Updated on 5/6/2020
The Sperling's single-ensemble task (Second Version)
*** For Practice Trials with Feedbacks (Based on ver2_experiment.py)
#
Trial Procedure & Time:
fixation screen: 250ms
pre_cue screen: 750ms
gabor_set screen: 200ms
blank screen: 400ms
isi blank screen: 500ms
#
Trial Constructions:
4 Experimental Conditions x
5 Set Ori Tilts (0, +-10, +-20) x
20 Reps (Taken Together in Psychometric Curve)
{
5 Repetitions for Cued Ori Tilts (0, +-10, +-20)
4 Repetition for Postional Changes
}
== 400 trials
#
Break Trials:
1 min Self-Terminated Break (in trial 100 & trial 300)
2 min Mandatory Break (in trial 200)
'''

# import libraries
from datetime import datetime
import numpy as np
import os
import pandas as pd
from psychopy import visual, event, monitors, core, logging, gui
import sys

'''
variables to calibrate the monitor
line_width_in_pixel is only used in the line width of the
precue and postcue, psychopy not supported in deg units
The border width of the circle is 0.2 visual angle
'''

# Setting for the 2 Monitors in RLG307
# monitor_name = 'RLG307
# view_distance = 60
# screen_width = 59.8
# screen_resolution = [3840,2160]
# line_width_in_pixel = 13

# Setting for Home Monitor
monitor_name = 'testMonitor'
view_distance = 60
screen_width = 47.5
screen_resolution = [1680,1050]
line_width_in_pixel = 7

# declare timing variables
fixation_time = 0.25
precue_time = 0.75
gaborset_time = 0.2
blankscreen_time = 0.4
feedback_screen_time = 1
isi_time = 0.5

# declare variables for trial generations
No_of_Trials = 10
conditions = [1,2,3,4]
set_orientations = [0,10,-10,20,-20]
cued_orientations = [0,10,-10,20,-20]
positions = [1,2,3,4,5,6,7,8,9]

# generate the trial list and randomly shuffle
triallist = []
for condition in conditions:
    for set_orientation in set_orientations:
        for cued_orientation in cued_orientations:
            np.random.shuffle(positions)
            for position in positions[0:4]:
                trial = [condition, set_orientation, cued_orientation, position]
                triallist.append(trial)
                np.random.shuffle(triallist)

# clear command output and start logging
os.system('cls' if os.name == 'ht' else 'clear')
logging.console.setLevel(logging.CRITICAL)
print("**************************************")
print("PRACTICE TRIAL - NO SAVE")
print("PSYCHOPY LOGGING set to : CRITICAL")
print(datetime.now())
print("**************************************")

# calibrating monitor and creating window for experiment
mon = monitors.Monitor(monitor_name)
mon.setWidth(screen_width)
mon.setDistance(view_distance)
win = visual.Window(size=screen_resolution, color='#C0C0C0',
                    fullscr=True, monitor=mon, allowGUI = True
                    )


def instruction():
    #  creating the instruction text to shown at the beginning
    instruct_text = \
        "\
PRACTICE TRIAL: NO SAVE\n\
Instructions: \n\
This experiment is about judging the orientation. On each trial, \
A fixation cross will appear, followed by a cueing circle, \
you are required to focus on anything appeared WITHIN this circle. \
After presenting a flash of orientation patches, you will see another \
circle, you will need to judge and report the orientation WITHIN \
this SECOND circle. \n\n\
For a small circle, report the orientation of the single patch; \n\
For a big circle, report the average of all patches within. \n\n\
Press 'f' to indicate an anti-clockwise tilt & \n\
Press 'j' to indicate a clockwise tilt. \n\n\
You are required to complete a total of 400 trials, optional or mandatory \
breaks will be given for every 100 trials (~ 5 minutes).\
The whole experimental procedure is expected to complete within 30 minutes.\n\n\
Important Remarks: \n\
Response ASAP, Stick to you Intuition, & Prevent Overthinking. \n\
Raise your questions now, if there is any. \n\n\
Press 'f' or 'j' to Start the Experiment. \n\
Press 'End' if you want to Terminate the Experiment anytime.\
"

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
    Position Code Refer below
    (1,2,3)
    (4,5,6)
    (7,8,9)
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
    #
    Condition 1 & 2 --> Return single pre-cue
    Condition 3 & 4 --> Return ensemble pre-cue
    """
    singleprecue = visual.Circle(win=win, units = 'deg', radius=0.9,
                                 edges=1000, fillColor='#C0C0C0',
                                 lineColor='black',
                                 lineWidth=line_width_in_pixel, opacity=1
                                 )
    setprecue = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.85,
                              edges=1000, fillColor='#C0C0C0',
                              lineColor='black',
                              lineWidth=line_width_in_pixel, opacity=1
                              )

    if (condition == 1 or condition == 2):
        singleprecue.pos = pos_to_coordinate(position)
        singleprecue.draw()
    elif (condition == 3 or condition == 4):
        setprecue.draw()


def gaborset(set_orientation, cued_orientation, position):
    '''
    creating the 9-gabor set, one central grating surrounded by
    8 flanker gratings, use pos_to_coordinate dict to convert
    only draw the set to memory
    '''
    grating = visual.GratingStim(win = win, units= 'deg',tex='sin',
                                 mask='gauss', ori=0, pos=(0, 0),
                                 size=(1.6,1.6), sf=3, opacity = 1,
                                 blendmode='avg', texRes=128,
                                 interpolate=True, depth=0.0
                                 )
    '''
    Construction of the GaborSet Arrays
    And Randomly Shuffle it
    '''

    pos_array = [1,2,3,4,5,6,7,8,9]
    np.random.shuffle(pos_array)

    ori_array = []
    pos_ori_array = np.array([25,30,35])
    neg_ori_array = -pos_ori_array

    if set_orientation > 0:  # postive ensemble set
        pos_ori_array = pos_ori_array + 2 * set_orientation
        neg_ori_array = neg_ori_array + set_orientation
    elif set_orientation < 0:  # negative ensemble set
        pos_ori_array = pos_ori_array + set_orientation
        neg_ori_array = neg_ori_array + 2 * set_orientation
    else:  # neutral set (0)
        pass

    if cued_orientation == 0:  # To prevent 3 0s when the cued is 0
        ori_array = [0,
                     cued_orientation + 25,
                     -cued_orientation - 25,
                     pos_ori_array[0],
                     pos_ori_array[1],
                     pos_ori_array[2],
                     neg_ori_array[0],
                     neg_ori_array[1],
                     neg_ori_array[2],
                     ]

    else:
        ori_array = [0,
                     cued_orientation,
                     -cued_orientation,
                     pos_ori_array[0],
                     pos_ori_array[1],
                     pos_ori_array[2],
                     neg_ori_array[0],
                     neg_ori_array[1],
                     neg_ori_array[2],
                     ]

    np.random.shuffle(ori_array)

    '''
    Draw the Cued_Orientation and Set position to memory,
    remove the element in the array by value
    '''
    grating.setOri(cued_orientation)
    grating.pos = pos_to_coordinate(position)
    grating.draw()
    pos_array.remove(position)
    ori_array.remove(cued_orientation)

    '''
    this for-loop will set position & orientation from the arrays,
    draw it to memory, and remove drawn element from the arrays
    '''
    for z in range(8):
        grating.pos = pos_to_coordinate(pos_array[0])
        grating.setOri(ori_array[0])
        grating.draw()
        del(pos_array[0])
        del(ori_array[0])


def postcue(condition, position):
    """
    Creating and drawing the post-cue circle to memory
    Condition 1 = single pre-cue congruent trial
    Condition 2 = single pre-cue incongruent trial
    Condition 3 = ensemble pre-cue congruent trial
    Condition 4 = ensemble pre-cue incongruent trial
    #
    Condition 1 & 4--> Return single post-cue
    Condition 2 & 3 --> Return ensemble post-cue
    """

    singlepostcue = visual.Circle(win=win, units = 'deg', radius=0.9,
                                  edges=1000, fillColor='#C0C0C0',
                                  lineColor='black',
                                  lineWidth=line_width_in_pixel,
                                  opacity=1
                                  )
    setpostcue = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.85,
                               edges=1000, fillColor='#C0C0C0',
                               lineColor='black',
                               lineWidth=line_width_in_pixel,
                               opacity=1
                               )

    if (condition == 1 or condition == 4):
        singlepostcue.pos = pos_to_coordinate(position)
        singlepostcue.draw()
    elif (condition == 2 or condition == 3):
        setpostcue.draw()


def feedback(condition, set_orientation, cued_orientation, response):
    # Create Feedback for Practice Trial and draw to memory
    '''
    Draw a green circle for correct, red for wrong
    if 0 in ori: always correct
    '''
    correct_fb = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.5,
                               edges=1000, fillColor='#ADFF2F',
                               lineColor='#ADFF2F',
                               lineWidth=line_width_in_pixel,
                               opacity=1)
    wrong_fb = visual.Circle(win=win, units = 'deg', pos=(0,0), radius=2.5,
                               edges=1000, fillColor='#FF0000',
                               lineColor='#FF0000',
                               lineWidth=line_width_in_pixel,
                               opacity=1)

    if 'f' in response:
        resp_bin = 0
    else:
        resp_bin = 1

    if condition == 1 or condition == 4:
        if cued_orientation > 0:
            answer = 1
        elif cued_orientation == 0:
            answer = resp_bin
        else:
            answer = 0
    else:
        if set_orientation > 0:
            answer = 1
        elif set_orientation == 0:
            answer = resp_bin
        else:
            answer = 0

    if resp_bin == answer:
        correct_fb.draw()
    else:
        wrong_fb.draw()


def debriefing():
    #  Debriefing Note
    debrief_text = \
        "\
End of Practice Trials\
"

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
    '''
    This is the main trial loop
    '''
    for i in range(0, No_of_Trials):
        print(triallist[i])
        # fixation screen
        fixation()
        win.flip()
        core.wait(fixation_time)
        # precue screen
        precue(triallist[i][0], triallist[i][3])
        win.flip()
        core.wait(precue_time)
        # set screen
        gaborset(triallist[i][1], triallist[i][2], triallist[i][3])
        win.flip()
        core.wait(gaborset_time)
        # blankscreen
        win.flip()
        core.wait(blankscreen_time)
        # postcue screen
        postcue(triallist[i][0], triallist[i][3])
        win.flip()

        resp = event.waitKeys(maxWait=1000, keyList=['end','f','j'],
                              clearEvents=True)

        if 'end' in resp:
            # Exit Key
            win.close()
            sys.exit()

        elif any(keylist in resp for keylist in ("f", "j")):
            # Feedback Screen
            feedback(triallist[i][0], triallist[i][1], triallist[i][2], resp)
            win.flip()
            core.wait(feedback_screen_time)
            # ISI
            win.flip()
            core.wait(isi_time)
    '''
    The main trial loop Ends Here.
    '''

    # Debrifing & close all
    debriefing()
    win.close()
    sys.exit()


if __name__ == '__main__':
    main()
