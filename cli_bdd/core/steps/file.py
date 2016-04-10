import os
import shutil

from hamcrest import (
    assert_that,
    contains_string,
    equal_to,
    is_not,
    is_,
)

from cli_bdd.core.steps.base import StepBase


class CopyFileOrDirectory(StepBase):
    """Copies a file or directory.

    Examples:

    ```gherkin
    Given I copy a file from "/tmp/old.txt" to "/var/new.txt"
    Given I copy the file named "hello.txt" to "/var/"
    Given I copy a directory from "/tmp/hello/" to "/var/"
    ```
    """
    type_ = 'given'
    sentence = (
        'I copy (a|the) (?P<file_or_directory>(file|directory))'
        '( (named|from))? "(?P<source>[^"]*)" to "(?P<destination>[^"]*)"'
    )

    def step(self, file_or_directory, source, destination):
        if file_or_directory == 'file':
            shutil.copyfile(source, destination)
        else:
            shutil.copytree(source, destination)


class MoveFileOrDirectory(StepBase):
    """Moves a file or directory.

    Examples:

    ```gherkin
    Given I move a file from "/tmp/old.txt" to "/var/new.txt"
    Given I move the file named "hello.txt" to "/var/"
    Given I move a directory from "/tmp/hello/" to "/var/"
    ```
    """
    type_ = 'given'
    sentence = (
        'I move (a|the) (?P<file_or_directory>(file|directory))'
        '( (named|from))? "(?P<source>[^"]*)" to "(?P<destination>[^"]*)"'
    )

    def step(self, file_or_directory, source, destination):
        shutil.move(source, destination)


class CreateDirectory(StepBase):
    """Creates directory.

    Examples:

    ```gherkin
    Given a directory "/tmp/test/"
    Given the directory named "/tmp/test/"
    ```
    """
    type_ = 'given'
    sentence = (
        '(a|the) directory'
        '( named)? "(?P<dir_path>[^"]*)"'
    )

    def step(self, dir_path):
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


base_steps = [
    {
        'func_name': 'copy_file_or_directory',
        'class': CopyFileOrDirectory
    },
    {
        'func_name': 'move_file_or_directory',
        'class': MoveFileOrDirectory
    },
    {
        'func_name': 'create_directory',
        'class': CreateDirectory
    },
]
