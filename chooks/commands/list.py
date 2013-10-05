"""Lists chooks in a git repository.

Usage:
  chooks list [-v | --verbose]

Options:
  -v, --verbose  Show more verbose information for each hook.
"""


from chooks import constants
from chooks import git

# TODO automatic paging?


def run(args):
    sections = git.get_values_dict(r'%s' % constants.PREFIX)
    if constants.PREFIX not in sections:
        print 'This repository has no chooks'
        return 1

    yes_no = lambda x: 'Yes' if x == 'True' else 'No'
    hooks = sections[constants.PREFIX]
    for name, hook in hooks.items():
        command = hook[constants.KEY_COMMAND]
        disabled = hook.get(constants.KEY_DISABLED) == 'True'
        if args.get('--verbose'):
            uses_stdin = hook.get(constants.KEY_STDIN)
            filters = hook.get(constants.KEY_FILTERS)
            git_hooks = hook.get(constants.KEY_HOOKS, 'All')
            fatal = hook.get(constants.KEY_FATAL)

            if disabled:
                print name, '[disabled]'
            else:
                print name

            print '    Command    :', command
            print '    Uses stdin :', yes_no(uses_stdin)
            print '    Fatal      :', yes_no(fatal)
            print '    Filters    :', filters
            print '    Git Hooks  :', git_hooks
        elif disabled:
            print '%s -> %s [disabled]' % (name, command)
        else:
            print name, '->', command

    return 0
