import readline
from pathlib import Path

history_file = Path.home() / ".r_history"

def setup_history():

    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass

    readline.set_history_length(1000)


def save_history():

    readline.write_history_file(history_file) 