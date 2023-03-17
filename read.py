import readline
import atexit
import os

cache_dir = os.getenv("XDG_CACHE_DIRECTORY")
if not cache_dir:
    cache_dir = os.path.join(os.path.expanduser("~"), ".cache")

histfile = os.path.join(cache_dir, '.gptcli_history')

try:
    readline.read_history_file(histfile)
    readline.set_history_length(2048)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)