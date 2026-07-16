from pathlib import Path
import importlib.util

def load_plugins(commands):

    plugin_dir = Path.home() / ".config/r/plugins"

    if not plugin_dir.exists():
        plugin_dir.mkdir(parents=True,exist_ok=True)
        return 

    for file in plugin_dir.glob("*.py"):

        spec = importlib.util.spec_from_file_location(
            file.stem,
            file
        )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "register"):
            try:
             module.register(commands) 
            except Exception as e:
                print (f"Failed loading{file.name} : {e}") 