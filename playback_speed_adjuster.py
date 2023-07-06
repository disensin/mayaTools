"""
Author: Isai Calderon III
To launch this tool, open the Script Editor in Maya, paste this code into it, and Run the script.
"""
from maya import cmds as mc
from pymel import all as pm

# Speed muiltipliers for the UI to use. A button will be created for each one.
AVAILABLE_SPEEDS = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]

# Available FPS' that the tool will search for.
# If the desired FPS doesn't exist, create a new entry for it, and reload the tool
DEFAULT_FPS = { 'game': 15,
                'film': 24,
                'pal': 25,
                '29.07fps':29.07,
                'ntsc':30,
                'show': 48,
                'palf': 50,
                'ntscf':60}

def get_unit():
    '''
    Gets the current FPS unit in the scene.
    '''
    current_unit = mc.currentUnit(q=1,t=1).split('fps')[0].split('df')[0]
    print( 'Unit is: ' , current_unit)
    try:
        return float(current_unit)
    except :
        return DEFAULT_FPS[current_unit]

def _change_playbackSpeed(new_speed = 1, printout = 0):
    '''
    Command to change the Playback Speed.
    :param new_speed:
      Speed multiplier.
    :param printout:
      Print the new Speed.
    '''
    current_fps = get_unit() # Get the current FPS Unit
    mc.playbackOptions(playbackSpeed=new_speed) # Change the playback speed
    mc.setFocus('MayaWindow') # Set focus back in the Maya Viewport so User can continue interacting normally
    if printout:
        warning_text = 'Playback Speed changed to '
        if new_speed == 0:
            warning_text += 'Every Frame, Real Time'
        else:
            warning_text += '{}x Real Time'
        mc.warning(warning_text.format(str(new_speed)))

def _change_commands(this_slider, specific_value=False, value=1, printout= False):
    '''
    Apply the Value change to both the Playback Speed and the UI
    :param this_slider: Slider UI object.
    :param specific_value: Boolean if specific value should be applied.
    :param value: Playback Multiplier value.
    :param printout: If True, print out the new Value.
    '''
    if specific_value: this_slider.setValue(value)
    _change_playbackSpeed(this_slider.getValue(), printout=printout)

def speed_adjuster_ui():
    '''
    UI Makin' Time!
    '''
    playbackSpeed_window_name = 'playbackspeed_window'
    if pm.window(playbackSpeed_window_name, q=1, exists=1): # Delete the UI if it exists.
        pm.deleteUI(playbackSpeed_window_name)
    with pm.window(playbackSpeed_window_name, title= 'Playback Speed Adjuster'):
        with pm.columnLayout():
            # Create a slider with a Float input.
            this_slider = pm.floatSliderGrp(maxValue=2,
                                            minValue=0,
                                            field=1,
                                            fieldMinValue=0,
                                            fieldMaxValue=0,
                                            value=mc.playbackOptions(playbackSpeed=1,q=1),
                                            step=0.05,
                                            sliderStep=0.05
                                            )
            # Add the Commands to run when interacted with.
            pm.floatSliderGrp(this_slider,
                                edit=True,
                                changeCommand=pm.Callback(_change_commands,
                                                            this_slider,
                                                            specific_value=False,
                                                            printout=True),
                                dragCommand=pm.Callback(_change_commands,
                                                            this_slider,
                                                            specific_value=False,
                                                            printout=False),
                                )
        ui_kwargs = {'numberOfColumns':len(AVAILABLE_SPEEDS)}
        if 1 in AVAILABLE_SPEEDS:
            index_one = AVAILABLE_SPEEDS.index(1)
            ui_kwargs['columnWidth'] = [[index_one,50],[index_one+1,74]]
        button_row = pm.rowLayout(**ui_kwargs)
        with button_row:
            # For every speed option, add a button.
            for num,speed in enumerate(AVAILABLE_SPEEDS):
                new_text = str(speed)
                if speed == 1:
                    new_text += '({} fps)'.format(get_unit())
                
                pm.button(new_text, command=pm.Callback(_change_commands,
                                                        this_slider,
                                                        specific_value = True,
                                                        value = speed,
                                                        printout = True))

speed_adjuster_ui()
