import readline
import shlex
import os

def setup_autocomplete(commands, get_current_dir):

    def completer(text, state):
        line = readline.get_line_buffer()
        parts = shlex.split(line)

        if len(parts) <= 1:
            options = sorted(commands.keys())

        else:
            command = parts[0]

            if command in commands:
                current_dir = get_current_dir()
                options = sorted(item.name for item in current_dir.iterdir())
            else:
                options = []

        matches = [
            option for option in options
            if option.startswith(text)
        ]

        if len(matches) > 1:
            common = os.path.commonprefix(matches)

            if state == 0 and common != text:
                return common

        if state < len(matches):
            return matches[state]

        return None

    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete") 