"""Disables a hook from executing.

Usage:
  chooks disable [--global] <name>

Options:
  --global     Disables a global hook.
"""


from chooks import constants
from chooks import git


def run(args):
    if git.set_hook_value(args['<name>'], constants.KEY_DISABLED, True):
        return 0
    return 1
