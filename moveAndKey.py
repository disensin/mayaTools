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

