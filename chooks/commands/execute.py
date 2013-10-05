"""Execute all chooks for a given git hook.

Usage:
  chooks execute <hook> [<args>...]
"""


import fnmatch
import os
import subprocess

from chooks import constants
from chooks import git


def _exec_command(command, params):
    """Execute a command.

    Args:
        command: the command to execute
        parameters: a dictionary mapping of parameter names to values

    Returns:
        True if the command executed successfully (or it failed and this hook
        is not fatal), False otherwise.
    """
    successful = True
    try:
        # TODO how to deal with output from stdout/stderr. Most likely a chook
        #      option to say whether or not they should be printed on failure.
        fname = params.get(constants.KEY_FILE)
        use_stdin = params.get(constants.KEY_STDIN)
        stdin = open(fname if use_stdin else os.devnull, 'r')
        output = subprocess.check_call(command % params,
                                       stdin=stdin,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.STDOUT,
                                       shell=True)
    except subprocess.CalledProcessError as exc:
        msg = None
        if params.get(constants.KEY_ONCE):
            msg = '"%(hook_name)s" failed' % params
        else:
            msg = '"%(hook_name)s" failed on file "%(file)s"' % params

        if params.get(constants.KEY_FATAL):
            print 'FATAL:', msg
            successful = False
        else:
            print 'WARNING:', msg
    return successful


def run(args):
    format_dict = git.environment()
    format_dict[constants.KEY_GIT_HOOK] = args['<hook>']

    # Filter based on whether or not a chook operates on this git hook
    sections = git.get_values_dict(constants.PREFIX)
    filtered_hooks = []
    hooks = sections.get(constants.PREFIX, {})
    for name, hook in hooks.items():
        right_hook = args['<hook>'] in hook.get(constants.KEY_HOOKS, git.HOOKS)
        not_disabled = hook.get(constants.KEY_DISABLED) != 'True'
        if right_hook and not_disabled:
            filtered_hooks.append((name, hook))

    # Apply chooks
    return_code = 0
    for hook_name, hook in filtered_hooks:
        command = hook.get(constants.KEY_COMMAND)
        fatal = hook.get(constants.KEY_FATAL) == 'True'
        filters = hook.get(constants.KEY_FILTERS, '*').split(',')
        use_stdin = hook.get(constants.KEY_STDIN) == 'True'
        once = hook.get(constants.KEY_ONCE) == 'True'

        # TODO Have get_values_dict return booleans and such so we can just do
        #      format_dict.update(hook)
        #
        format_dict[constants.KEY_COMMAND] = command
        format_dict[constants.KEY_FATAL] = fatal
        format_dict[constants.KEY_FILTERS] = ','.join(filters)
        format_dict[constants.KEY_STDIN] = use_stdin
        format_dict[constants.KEY_HOOK_NAME] = hook_name
        format_dict[constants.KEY_ONCE] = once

        if once:
            if not _exec_command(command, format_dict):
                return_code = 1
        else:
            for x, y, old_path, new_path in git.status():
                # Skip over ignored and untracked files
                if x in '?!' or y in '?!':
                    continue

                fname = os.path.abspath(new_path or old_path)
                if any(fnmatch.fnmatch(fname, f) for f in filters):
                    format_dict[constants.KEY_FILE] = fname
                    format_dict[constants.KEY_STATUS_X] = x
                    format_dict[constants.KEY_STATUS_Y] = y
                    if not _exec_command(command, format_dict):
                        return_code = 1

    return return_code
