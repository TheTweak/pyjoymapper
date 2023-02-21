import os


def press_key(key, modifier=None):
    cmd = f"osascript -e 'tell application \"System Events\" to keystroke \"{key}\"'"
    if modifier:
        cmd += " using {" + modifier + " down}"
    os.system(cmd)


if __name__ == '__main__':
    press_key("a")
