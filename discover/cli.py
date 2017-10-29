"""
discover

Usage:
  discover want to learn about <topic>...
  discover want to learn <topic>...
  
  I want to learn about <topic>
  discover ask I want to learn about <topic>
  I want <topic>
  discover -h | --help
  discover --version
  I --version
  discover hello
  discover ask I want to learn about <topic>
  discover ask <question>...


Options:
  -h --help                         Show this screen.
  --version                         Show version.

Examples:
  discover hello
  discover ask Teach me about Albert Einstien 
  I want to learn about <topic>

Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/askalburgi/discover_black
"""


from inspect import getmembers, isclass

from docopt import docopt

from . import __version__ as VERSION


def main():
    """Main CLI entrypoint."""
    import discover.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(discover.commands, k) and v:
            module = getattr(discover.commands, k)
            discover.commands = getmembers(module, isclass)
            command = [command[1] for command in discover.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()


'''
	Credit: https://github.com/rdegges/skele-cli/edit/master/skele/cli.py
'''