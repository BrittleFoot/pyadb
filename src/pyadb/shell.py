


_TOUCHES = "content insert --uri content://settings/system --bind name:s:show_touches --bind value:i:"

SHOW_TOUCHES = _TOUCHES + '1'
HIDE_TOUCHES = _TOUCHES + '0'


def show_touches():
    return SHOW_TOUCHES

def hide_touches():
    return HIDE_TOUCHES

def screenrecord(cast_location : str, time_limit : int):
    return f"screenrecord --bugreport --verbose --time-limit {time_limit} {cast_location}"