"""Constants used by various parts of the chooks library."""


# Prefix used for keys in chook configuration
PREFIX = 'chooks'

#-----------------------------------------------------------------------
# Keys used for parameters grabbed from the git environment
#-----------------------------------------------------------------------

KEY_GIT_WORK_TREE = 'work_tree'
KEY_GIT_AUTHOR_NAME = 'author_name'
KEY_GIT_AUTHOR_EMAIL = 'author_email'
KEY_GIT_AUTHOR_DATE = 'author_date'
KEY_GIT_COMMITTER_NAME = 'committer_name'
KEY_GIT_COMMITTER_EMAIL = 'committer_email'
KEY_GIT_COMMITTER_DATE = 'committer_date'

#-----------------------------------------------------------------------
# Keys used for hook parameters that are stored
#-----------------------------------------------------------------------

# The command being executed.
KEY_COMMAND = 'command'

# "True" if this chook is disabled, anything else it is enabled.
KEY_DISABLED = 'disabled'

# "True" if this chook is fatal, anything else it isn't fatal.
KEY_FATAL = 'fatal'

# Comma-separated list of filename filters this chook applies to.
KEY_FILTERS = 'filters'

# Comma-separated list of git hooks this chook applies to. If no value given,
# this chook applies to all .
KEY_HOOKS = 'hooks'

# "True" if file data should be given to the command through stdin.
KEY_STDIN = 'stdin'

# "True" if his chook is applied once. If not "True", this chook is applied to
# all files in the staging area.
KEY_ONCE = 'once'

#-----------------------------------------------------------------------
# Keys used for dynamic options that can be used as placeholders for commands
#-----------------------------------------------------------------------

# The name of the hook currently being executed.
KEY_HOOK_NAME = 'hook_name'

# The file currently being processed by the chook command.
KEY_FILE = 'file'

# The X part of the git status (documented in man status).
KEY_STATUS_X = 'status_x'

# The Y part of the git status (documented in man status).
KEY_STATUS_Y = 'status_y'

# THe git hook currently being executed.
KEY_GIT_HOOK = 'git_hook'
