"""Removes a hook from a git repository.

Usage:
  chooks remove [--global] [-q | --quiet] <name>

Options:
  --global     Removes a global hook.
  -q, --quiet  Do not prompt for removal.
"""


from chooks import git

# TODO interactive removal (show list, etc)
# TODO remove by pattern


def run(args):
    choice = ''
    if not args.get('--quiet'):
        choice = raw_input('Are you sure? [Y/n] ')

    if choice in ('', 'Y'):
        if git.remove_hook(args['<name>']):
            return 0
    return 1
