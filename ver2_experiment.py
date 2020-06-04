'''
Last Updated on 4/6/2020
The Sperling's single-ensemble task (Second Version)
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
isi_time = 0.5
short_break_time = 30
long_break_time = 5

# declare variables for trial generations
No_of_Trials = 12
conditions = [1,2,3,4]
set_orientations = [0,10,-10,20,-20]
cued_orientations = [0,10,-10,20,-20]
positions = [1,2,3,4,5,6,7,8,9]
breaktrial = [  # for break trials
    ((No_of_Trials / 4) - 1),
    ((No_of_Trials / 2) - 1),
    ((3 * No_of_Trials / 4) - 1)]

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

# generate blank arrays for the output data file
date_array = []
time_array = []
name_array = []
age_array = []
gender_array = []
hand_array = []
trial_no_array = []
condition_array = []
set_orientation_array = []
cued_orientation_array = []
position_array = []
response_array = []
latency_array = []

# Text Variables - All Instruction text
instruct_text = \
    "\
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

debrief_text = \
    "\
That's the End of the Experiment.\n\
Thank you for your Participation.\
"
may_break_text = \
    "\
You have completed 100 trials, you may take a 1-minute break, \n\n\
If you don't need to, \n\
Press 'Spacebar' to Skip. \n\
"
must_break_text = \
    "\
You have completed 200 trials, Take a 2-minute break.\
"
end_break_text = \
    "\
Break Ended, \nPress 'f' or 'j' to Continue the experiment.\
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

# Create a data director, check info. and create save file name
try:
    os.mkdir('data')
    print("Directory Created!")
except FileExistsError:
    print("Directory Exist!")

if info.OK:
    save_file_name = 'data/' + show_info[0] + show_info[1] + '_' + \
        show_info[2] + '_ep_experiment.csv'
    save_file_name_backup = 'data/' + show_info[0] + show_info[1] + '_' + \
        show_info[2] + '_backup_orientation.csv'
else:
    print("User Cancelled")

# Create Save Path
save_path = gui.fileSaveDlg(initFileName=save_file_name,
                            prompt='Select Save File'
                            )
# Create a Backup file for all orientation in the set
# Refer to the gaborset function
backup_file = open(save_file_name_backup, 'w')

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
    ori_array_list_to_string = ','.join([str(element) for element in ori_array])
    backup_file.write(ori_array_list_to_string)
    backup_file.write("\n")

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


def break_time(trial_no):
    # Create stimuli and actions in break trials
    break_text = visual.TextStim(win = win, text = ' ',
                                 font = 'Times New Roman',
                                 pos = (0,-8), color = 'black',
                                 units = 'deg', height = 0.9,
                                 wrapWidth=20
                                 )
    break_timer = visual.TextStim(win = win, text = ' ',
                                  font = 'Source Code Pro',
                                  pos = (0,0), color = 'black',
                                  units = 'deg', height = 4,
                                  wrapWidth=20
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
    '''
    This is the main trial loop
    '''
    for i in range(0, No_of_Trials):
        '''Write data into dataframe for save '''
        date_array.append(show_info[0])
        time_array.append(show_info[1])
        name_array.append(show_info[2])
        age_array.append(show_info[3])
        gender_array.append(show_info[4])
        hand_array.append(show_info[5])
        trial_no_array.append(i + 1)
        condition_array.append(triallist[i][0])
        set_orientation_array.append(triallist[i][1])
        cued_orientation_array.append(triallist[i][2])
        position_array.append(triallist[i][3])

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

        start_time = core.getTime(applyZero = True)
        resp = event.waitKeys(maxWait=1000, keyList=['end','f','j'],
                              clearEvents=True)

        if 'end' in resp:
            # Exit Key
            resp_time = core.getTime(applyZero = True) - start_time
            response_array.append(resp[0])
            latency_array.append(resp_time)
            break

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

    # Create the DataFrame & Save it to csv
    outputfile = pd.DataFrame({'Exp_Date': date_array,
                               'Exp_Time': time_array,
                               'Sub_Name': name_array,
                               'Age': age_array,
                               'Gender': gender_array,
                               'Dominant_Hand': hand_array,
                               'Trial_No': trial_no_array,
                               'Condition': condition_array,
                               'Cued_Orientation': cued_orientation_array,
                               'Set_Orientation': set_orientation_array,
                               'Position': position_array,
                               'Response': response_array,
                               'Latency': latency_array
                               })
    outputfile.to_csv(save_path, sep=',', index=False)
    # Debrifing & close all
    debriefing()
    win.close()
    backup_file.close()
    sys.exit()


if __name__ == '__main__':
    main()
