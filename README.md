chooks is a utility to simplify management of your custom git hooks.

Note that this is a work-in-progress project, so be sure to send me feature
requests, or alternate designs that are advantageous over any approaches I've
taken.

# Installation

Use pip or easy_install:

    pip install 'git+git://github.com/thegedge/chooks.git#egg=chooks'

If some interest grows then I will add this project to PyPI. Alternatively, you
can install chooks manually. Make sure bin/chooks is in your `PATH` environment
variable and that chooks/ is in your python import path.

# Usage

Chooks can be executed on the command-line:

    chooks <command> [<command arguments>...]

Where the command can be one of `add`, `disable`, `enable`, `execute`, `help`,
`install`, `list`, or `remove`. For more information on any of these commands
use `chooks help cmd`.

## Install

This command installs shell scripts into the hooks directory of working
directory's repository. Note that it does not overwrite existing hooks by
default, but you can override this behaviour with `--overwrite`.

## Add

Adds a new chook to the current repository. The command to invoke for this
chook can contain the following placeholders:

  - **hook**: the name of the git hook being executed.
  - **file**: the file to use as input
  - **author_name**: name of the person who authored the commit.
  - **author_email**: email of the person who authored the commit.
  - **author_date**: date the commit was authored.
  - **status_(x|y)**: the X/Y components of a file's status. See the _Output >
    Short Format_ section of `git help status` for what various combinations of
    X and Y mean.

These can be used as arguments for your commands by wrapping them in `%()s`
(e.g., `%(author_name)s`). For example, suppose you want to make sure all your
\*.cpp and \*.hpp files have a copyright line in them. If not, you want to
prevent a commit from going through. The following command will add this hook:

    chooks add --filter='*.?pp' --stdin --name='copyright check' --fatal
        --hook='pre-commit' -- grep Copyright

## Remove

Removes a chook from a repository. By default, a prompt will ask you if you
want to remove the given chook (if it exists), but you can suppress this by
specifying the `-q` or `--quiet` option.

## List

Lists all chooks you have for the working directory's repository. By default it
lists chooks in a short format: `name -> command`. If you specify `--verbose`
you will get a long format listing showing all the different options specified
for a given chook.

## Execute

This command is not intended for manual use, but it is possible to use it. It
executes all chooks for a given git hook in the working directory's repository.

# Comparison To Similar Tools

I'd just like to say that I wrote this tool in boredom, paying no attention to
whether or not there were existing tools. There are, so I thought it might be
nice to find some differences:

   - [git-hooks](https://github.com/icefox/git-hooks)
      - Because of its name, integrates nicely with git (i.e., you use the
        command `git hooks' to work with your hooks).
      - Allows for user, global, and per-repository hooks.
      - Requires you to write a shell script for every hook, even if all you
        want to do is run a simple command.
      - Disabling a hook means shuffling files around.
      - No easy way to run a hook based on file filters.
   - [hooked](https://github.com/newky/hooked)
      - Requires you to write all of your hooks as Python scripts, which
        overall is nice, but sometimes you just want to run a simple command.
      - Requires you to manually edit a JSON config to add/remove/update hooks.
      - Currently limited to pre-commit, prepare-commit-msg, and commit-msg
        hooks, but wouldn't be too difficult to extend it beyond these.
      - You have to take care of filtering in your hooks.

Note that if any of these points are incorrect, let me know and I'll be sure to
remove/update them. Also, if there are any advantages to these scripts over
chooks, let me know and I'll add those points to the list. Also feel free to
send a pull request my way with the changes.
