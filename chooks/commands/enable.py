"""Enables a hook so it can execute.

Usage:
  chooks enable [--global] <name>

Options:
  --global     Enables a global hook.
"""


from chooks import constants
from chooks import git


def run(args):
    if git.remove_hook_value(args['<name>'], constants.KEY_DISABLED):
        return 0
    return 1
