from subprocess import call


def key_down(key):
    cmd = f"osascript -e 'tell application \"System Events\" to key down \"{key}\"'"
    call(cmd, shell=True)


def key_up(key):
    cmd = f"osascript -e 'tell application \"System Events\" to key up \"{key}\"'"
    call(cmd, shell=True)


def press_key(key, modifier=None):
    cmd = f"osascript -e 'tell application \"System Events\" to keystroke \"{key}\"'"
    if modifier:
        cmd += " using {" + modifier + " down}"
    call(cmd, shell=True)


if __name__ == '__main__':
    press_key("a")
