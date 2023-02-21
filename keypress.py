import os


def press_key(key):
    cmd = f"osascript -e 'tell application \"System Events\" to keystroke \"{key}\"'"
    os.system(cmd)


if __name__ == '__main__':
    press_key("a")
