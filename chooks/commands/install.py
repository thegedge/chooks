"""Installs git hooks to execute chooks.

Usage:
  chooks install [--overwrite]

Options:
  --overwrite  Overwrite existing git hooks with the chook bootstrap scripts.
"""


import os.path
import stat

from chooks import git

# TODO remove PYTHONPATH= below when releasing
_HOOK_TEMPLATE = (
    '#!/bin/sh\n'
    'PYTHONPATH=~/projects/python/chooks.py/ chooks execute %s "$@"'
)

_EXECUTABLE = (stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP
                            | stat.S_IROTH | stat.S_IXOTH)


def run(args):
    git_dir = git.git_dir()
    if git_dir:
        overwrite = args.get('--overwrite', False)
        hooks_dir = os.path.join(git_dir, 'hooks')
        for hook, uses_stdin in git.HOOKS.items():
            hook_fname = os.path.join(hooks_dir, hook)
            if not os.path.exists(hook_fname) or overwrite:
                with open(hook_fname, 'wt') as hook_file:
                    hook_file.write(_HOOK_TEMPLATE % hook)
                os.chmod(hook_fname, _EXECUTABLE)
            else:
                print 'Hook already exists for %s' % hook
    else:
        print 'Unable to get git dir'
        return 1
    return 0
