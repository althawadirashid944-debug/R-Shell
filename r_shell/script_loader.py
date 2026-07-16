from pathlib import Path


def find_script(command):
    script_dir = Path.home() / ".config" / "r" / "scripts"

    # Create scripts folder if it doesn't exist
    script_dir.mkdir(parents=True, exist_ok=True)

    possible_scripts = [
        script_dir / command,
        script_dir / f"{command}.sh",
        script_dir / f"{command}.py",
    ]

    for script in possible_scripts:
        if script.is_file():
            return script

    return None 