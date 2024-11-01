from maya import cmds as mc
from maya import mel

attr_dict = {}

def set_key_then_frame(frame_forward=True,*args,**kwargs):
    
    set_key_on_modified_attributes(objects=None)
    
    if frame_forward:
        mel.eval('currentTime -edit (`playbackOptions -q -slp` ? `findKeyframe -timeSlider -which next` : `findKeyframe -which next`)')
    else:
        mel.eval('currentTime -edit (`playbackOptions -q -slp` ? `findKeyframe -timeSlider -which previous` : `findKeyframe -which previous`)')
    

def set_key_on_modified_attributes(objects=None):
    """Sets keys on only the attributes that have been modified."""
    global attr_dict

    if not objects:
        objects = cmds.ls(sl=True)

    if not objects:
        return
    
    for item in objects:
        for attr in mc.listAttr(item,keyable=True) or []:
            item_attr = item+'.'+attr
            new_value = mc.getAttr(item_attr)
            if item_attr in attr_dict and attr_dict[item_attr] != new_value:
                mc.setKeyframe(item_attr)
            attr_dict.setdefault(item_attr,new_value)
            attr_dict[item_attr] = new_value

mc.nameCommand('nextFrame_andKey',command='python("set_key_then_frame(frame_forward=True)")',annotation='Set Key while changing current Frame Forward.',)
mc.nameCommand('previousFrame_andKey',command='python("set_key_then_frame(frame_forward=False)")',annotation='Set Key while changing current Frame Backward.',)

mc.hotkey(keyShortcut='.', name='nextFrame_andKey', dragPress=True)
mc.hotkey(keyShortcut=',', name='previousFrame_andKey', dragPress=True)

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
