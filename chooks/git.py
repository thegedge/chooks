"""
Helper functions for executing git functions pertinent to chooks.
"""
import constants
import os
import sh


# Hooks
HOOKS = {
    'applypatch-msg',
    'commit-msg',
    'post-applypatch',
    'post-checkout',
    'post-commit',
    'post-merge',
    'post-receive',
    'post-rewrite',
    'post-update',
    'pre-applypatch',
    'pre-auto-gc',
    'pre-commit',
    'pre-push',
    'pre-rebase',
    'pre-receive',
    'prepare-commit-msg',
    'update',
}


def git_dir():
    """Attempts to retrieve the git directory.

    If GIT_DIR is defined, return its value. Otherwise return the value of
    `git rev-parse --git-dir`.
    """
    git_dir = os.getenv('GIT_DIR')
    if git_dir:
        return git_dir

    try:
        return str(sh.git('rev-parse', git_dir=True)).strip()
    except sh.ErrorReturnCode as exc:
        pass


def working_tree():
    """Attempts to retrieve the working tree.

    Proceeds in the following fashion:
      1. If GIT_WORK_TREE is defined then return it,
      2. if `git rev-parse --show-toplevel` succeeds then return it, else
      3. return the parent directory of git_dir().
    """
    work_tree = os.getenv('GIT_WORK_TREE')
    if work_tree:
        return work_tree

    try:
        return sh.git.rev_parse(show_toplevel=True).wait()
    except sh.ErrorReturnCode as exc:
        pass

    git_directory = git_dir()
    if git_directory:
        return os.path.abspath(os.path.join(git_directory, os.path.pardir))


def _exec(command, *args, **kwargs):
    """Executes the given git command.

    Returns a 2-tuple with whether or not the command was successfully
    executed, and the result (as returned from sh module command).
    """
    try:
        git_cmd = sh.git.bake(work_tree=working_tree(),
                              _iter=True,
                              _err=open(os.devnull, 'w'))
        git_cmd = git_cmd.bake(command, **kwargs)
        result = git_cmd(*args)
        result.wait()
        return True, result
    except sh.ErrorReturnCode as exc:
        return False, exc


def status():
    """Generator for the git-status command.

    Each item yielded contains four components:

      1. status part 1,
      2. status part 2,
      3. path part 1, and
      4. path part 2.

    These parts correspond with X, Y, PATH1, and PATH2 from the git-status
    manpage, respectively.
    """
    succeeded, result = _exec('status', porcelain=True)
    if succeeded:
        for line in result:
            status, paths = line[:2], line[3:].strip()
            path1, _, path2 = paths.partition(' -> ')
            yield status[0], status[1], path1, path2


def remove_hook(hook_name, is_global=False):
    """Executes the git-config command, removing a section.

    Returns True if the command succeeded, False otherwise.
    """
    kwargs = {'remove_section': True}
    if is_global:
        kwargs['global'] = True

    section_name = '%s.%s' % (constants.PREFIX, hook_name)
    succeeded, result = _exec('config', section_name, **kwargs)
    if succeeded:
        result.wait()
    return succeeded


def set_hook_value(hook_name, key, value, is_global=False):
    """Sets a value for the given hook.

    Returns True if the command succeeded, False otherwise.
    """
    if is_global:
        kwargs['global'] = True

    git_key = '%s.%s.%s' % (constants.PREFIX, hook_name, key)
    succeeded, result = _exec('config', git_key, value)
    if succeeded:
        result.wait()
    return succeeded


def remove_hook_value(hook_name, key, is_global=False):
    """Removes a value for the given hook.

    Returns True if the command succeeded, False otherwise.
    """
    if is_global:
        kwargs['global'] = True

    git_key = '%s.%s.%s' % (constants.PREFIX, hook_name, key)
    succeeded, result = _exec('config', git_key, unset=True)
    if succeeded:
        result.wait()
    return succeeded


def set_hook_values(hook_name, values, is_global=False):
    """Sets a dictionary of values for the given hook.

    If any value is None, it will be ignored. If any value could not be set,
    False is returned. Otherwise True.
    """
    for key, value in values.items():
        if value and not set_hook_value(hook_name, key, value, is_global):
            return False
    return True


def get_values(query):
    """Get all config values matching a given query.

    Each item yielded contains four parts: section name, subsection name,
    key name, and the value.
    """
    succeeded, result = _exec('config', query, get_regexp=True, null=True)
    if succeeded:
        lines = str.join('', result).split('\0')
        for line in lines:
            if line:
                keypath, value = line.split('\n', 1)
                section_name, _, name = keypath.partition('.')
                subsection_name, _, name = name.rpartition('.',)
                yield section_name, subsection_name, name, value


def get_values_dict(query):
    """Returns a nested dictionary version of the git-config results.

    In particular, the returned dictionary has the following structure:
      {
          'section': {
              'subsection': {
                  'key1': 'value1',
                  'key2': 'value2',
                  ...
              },
              ...
          },
          ...
      }
    """
    result = {}
    for section, subsection, key, value in get_values(query):
        section = result.setdefault(section, {})
        subsection = section.setdefault(subsection, {})
        subsection[key] = value
    return result


def environment():
    """Returns git-relevant environment variables in a dictionary.

    The following key/values are returned:
        - work_tree: absolute path to the working tree
        - author_name: full name of the person who authored the commit
        - author_email: email of the person who authored the commit
        - author_date: date the commit was authored
        - committer_name: full name of the person committing
        - committer_email: email of the person committing
        - committer_date: date of committing
    """
    envget = os.environ.get
    return {
        constants.KEY_GIT_WORK_TREE:       os.path.abspath(working_tree()),
        constants.KEY_GIT_AUTHOR_NAME:     envget('GIT_AUTHOR_NAME', ''),
        constants.KEY_GIT_AUTHOR_EMAIL:    envget('GIT_AUTHOR_EMAIL', ''),
        constants.KEY_GIT_AUTHOR_DATE:     envget('GIT_AUTHOR_DATE', ''),
        constants.KEY_GIT_COMMITTER_NAME:  envget('GIT_COMMITTER_NAME', ''),
        constants.KEY_GIT_COMMITTER_EMAIL: envget('GIT_COMMITTER_EMAIL', ''),
        constants.KEY_GIT_COMMITTER_DATE:  envget('GIT_COMMITTER_DATE', ''),
    }
