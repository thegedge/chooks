"""Adds a chook to a git repository.

Usage:
  chooks add [--stdin | --argument] [--once | --filter=FILTER...] [--global]
             [--fatal] [--hook=NAME...] [--name=NAME] [--disabled]
             [--] <command> [<args>...]

Options:
  --stdin            Supply input files to this chook via stdin.
  --filter=<filter>  Only execute this chook for files who names match the
                     given filter.
  --global           Execute this chook for all repositories.
  --hook=<name>      Name of the git hooks this chook will be executed for
                     (if not specified, default to all git hooks).
  --fatal            Return a nonzero status to the git hook if this chook
                     returns a nonzero status.
  --once             If specified, this chook is only applied once for the git
                     hook. If not specified, this chook is applied against all
                     files echoed by 'git status' (excluding ignored/untracked)
  --name=<name>      Custom hook name (defaults to the command name).
  --disabled         Default the hook to a disabled state.
"""


from chooks import constants
from chooks import git

# TODO interactive mode?


def run(args):
    full_cmd = '%s %s' % (args['<command>'], ' '.join(args['<args>']))
    filters = args.get('--filter') and ','.join(args['--filter'])
    # TODO validate hook names, making sure they're actually git hooks
    hooks = args.get('--hook') and ','.join(args['--hook'])

    values = {
        constants.KEY_COMMAND: full_cmd,
        constants.KEY_STDIN: args.get('--stdin'),
        constants.KEY_FILTERS: filters,
        constants.KEY_HOOKS: hooks,
        constants.KEY_FATAL: args.get('--fatal'),
        constants.KEY_DISABLED: args.get('--disabled'),
    }

    hook_name = args.get('--name') or args['<command>']
    is_global = args.get('--global', False)
    if git.set_hook_values(hook_name, values, is_global=is_global):
        return 0
    return 1
