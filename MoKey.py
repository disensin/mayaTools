from maya import cmds as mc
from maya import mel

attr_dict = {}

import maya.cmds as cmds

def create_hotkey_commands():
    """
    Creates hotkey commands and assigns them using Maya's hotkey editor.

    This function defines a set of custom hotkey commands for controlling frame and keyframe navigation in Maya. It creates or updates nameCommands, runTimeCommands, and assigns hotkeys based on user-defined configurations.
    """
    hotkey_data = {
        'Key_Prev6Frames': {
            'annotation': 'Autokey, go to previous 6 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)-6)',
            'keyShortcut': '^',
            'commandLanguage': 'python',
            'altModifier': True
        },
        'Key_Next6Frames': {
            'annotation': 'Autokey, go to next 6 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)+6)',
            'keyShortcut': '^',
            'commandLanguage': 'python',
            'altModifier': False
        },
        # ---
        'Key_Prev5Frames': {
            'annotation': 'Autokey, go to previous 5 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)-5)',
            'keyShortcut': '%',
            'commandLanguage': 'python',
            'altModifier': True
        },
        'Key_Next5Frames': {
            'annotation': 'Autokey, go to next 5 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)+5)',
            'keyShortcut': '%',
            'commandLanguage': 'python',
            'altModifier': False
        },
        # ---
        'Key_Prev4Frames': {
            'annotation': 'Autokey, go to previous 4 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)-4)',
            'keyShortcut': '$',
            'commandLanguage': 'python',
            'altModifier': True
        },
        'Key_Next4Frames': {
            'annotation': 'Autokey, go to next 4 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)+4)',
            'keyShortcut': '$',
            'commandLanguage': 'python',
            'altModifier': False
        },
        # ---
        'Key_Prev3Frames': {
            'annotation': 'Autokey, go to previous 3 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)-3)',
            'keyShortcut': '#',
            'commandLanguage': 'python',
            'altModifier': True
        },
        'Key_Next3Frames': {
            'annotation': 'Autokey, go to next 3 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)+3)',
            'keyShortcut': '#',
            'commandLanguage': 'python',
            'altModifier': False
        },
        # ---
        'Key_Prev2Frames': {
            'annotation': 'Autokey, go to previous 2 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)-2)',
            'keyShortcut': '@',
            'commandLanguage': 'python',
            'altModifier': True
        },
        'Key_Next2Frames': {
            'annotation': 'Autokey, go to next 2 Frames',
            'command': 'cmds.autoKeyframe(); cmds.currentTime(cmds.currentTime(q=1)+2)',
            'keyShortcut': '@',
            'commandLanguage': 'python',
            'altModifier': False
        },
        'Key_PrevFrame': {
            'annotation': 'Autokey, go to previous Frame',
            'command': 'autoKeyframe; nextOrPreviousFrame "previous"',
            'keyShortcut': ',',
            'commandLanguage': 'mel',
            'altModifier': True
        },
        'Key_NextFrame': {
            'annotation': 'Autokey, go to next Frame',
            'command': 'autoKeyframe; nextOrPreviousFrame "next"',
            'keyShortcut': '.',
            'altModifier': True,
            'commandLanguage': 'mel'
        },
        'Key_PrevKey': {
            'annotation': 'Autokey, go to previous Keyframe',
            'command': 'autoKeyframe; currentTime -edit (`playbackOptions -q -slp` ? `findKeyframe -timeSlider -which previous` : `findKeyframe -which previous`)',
            'keyShortcut': ',',
            'altModifier': False,
            'commandLanguage': 'mel'
        },
        'Key_NextKey': {
            'annotation': 'Autokey, go to next Keyframe',
            'command': 'autoKeyframe; currentTime -edit (`playbackOptions -q -slp` ? `findKeyframe -timeSlider -which next` : `findKeyframe -which next`)',
            'keyShortcut': '.',
            'altModifier': False,
            'commandLanguage': 'mel'
        }
    }
    
    """
    Dictionary Structure:
    hotkey_data: dict
        - Key (str): Unique identifier for the hotkey configuration.
        - Values (dict): Contains configuration for each hotkey.
            - annotation (str): Description of the hotkey command.
            - command (str): The command to be executed by the hotkey.
            - keyShortcut (str): The key to which the command will be assigned.
            - commandLanguage (str): Language of the command ('mel' or 'python').
            - altModifier (bool, optional): Indicates if the Alt key should be used as a modifier.
            - ctrlModifier (bool, optional): Indicates if the Ctrl key should be used as a modifier.
            - shiftModifier (bool, optional): Indicates if the Shift key should be used as a modifier.
            - dragPress (bool, optional): Indicates if the hotkey should activate on drag press. Defaults to True.
    """

    for key, data in hotkey_data.items():
        # Create a nameCommand for the hotkey
        name_command = cmds.nameCommand(
            key + 'NameCommand',
            annotation=data['annotation'],
            command=key,
            sourceType='mel' if data['commandLanguage'] == 'mel' else 'python'
        )

        # Delete the existing runTimeCommand if it exists
        if cmds.runTimeCommand(key, q=1, exists=1):
            cmds.runTimeCommand(key, e=1, delete=1)

        # Create a new runTimeCommand
        cmds.runTimeCommand(
            key,
            annotation=data['annotation'],
            category='Custom Scripts.ito-cuts',
            command=data['command'],
            commandLanguage=data['commandLanguage']
        )

        # Define the hotkey arguments
        hotkey_kwargs = {
            'altModifier': data.get('altModifier', False),
            'ctrlModifier': data.get('ctrlModifier', False),
            'shiftModifier': data.get('shiftModifier', False),
            'dragPress': data.get('dragPress', True)
        }

        # Remove any existing hotkey assignment
        if cmds.hotkey(data['keyShortcut'], q=1, **hotkey_kwargs):
            cmds.hotkey(keyShortcut=data['keyShortcut'], name="")

        # Assign the hotkey to the nameCommand
        cmds.hotkey(
            keyShortcut=data['keyShortcut'],
            name=name_command,
            **hotkey_kwargs
        )

create_hotkey_commands()

aimer_group = ''
aimed_item = ''
def make_aim_and_move():
    global aimer_group,aimed_item
    if aimer_group and mc.objExists(aimer_group):
        delete_aim_and_move()
    items = mc.ls(sl=1)
    aimed_item = items[0]
    
    # create aimer setup
    forward_locator = mc.spaceLocator(name='forward_locator')
    up_locator = mc.spaceLocator(name='up_locator')
    aimer_group = mc.group(forward_locator,up_locator)
    
    mc.matchTransform(aimer_group,aimed_item)
    mc.setAttr(forward_locator[0]+'.tx',5)
    mc.setAttr(up_locator[0]+'.ty',5)
    mc.pointConstraint(aimed_item,aimer_group)
    this_parent = mc.parentConstraint(aimed_item,forward_locator[0],maintainOffset=1)
    this_parent += mc.parentConstraint(aimed_item,up_locator[0],maintainOffset=1)
    # Bake the aimer tools to the aimed_item's rotations
    mc.ogs(pause=True)
    start_frame = mc.playbackOptions(q=1,minTime=1)
    end_frame = mc.playbackOptions(q=1,maxTime=1)
    mc.bakeResults(forward_locator+up_locator,smart=1,time=(start_frame,end_frame))
    mc.ogs(pause=True)
    mc.delete(this_parent)
    
    # Aim constrain the aimed_item to the aimer tool
    new_aim_constraint = mc.aimConstraint(forward_locator[0],aimed_item,worldUpObject=up_locator[0],worldUpType='object',maintainOffset=1)
    mc.select(forward_locator+up_locator)
    
    # Animate and set keys on the aimer objects

def delete_aim_and_move():
    global aimer_group,aimed_item
    if aimer_group and mc.objExists(aimer_group):
        # Bake aimed_item and delete aimer tool
        mc.ogs(pause=True)
        start_frame = mc.playbackOptions(q=1,minTime=1)
        end_frame = mc.playbackOptions(q=1,maxTime=1)
        mc.bakeResults(aimed_item,smart=1,time=(start_frame,end_frame))
        mc.ogs(pause=True)
        mc.delete(aimer_group)
        mc.select(aimed_item)
        aimer_group = ''
