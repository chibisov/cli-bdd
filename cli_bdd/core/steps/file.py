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
    """
    Examples:
        Given I copy a file from "/tmp/old.txt" to "/var/new.txt"
        Given I copy the file name "hello.txt" to "/var/"
        Given I copy a directory from "/tmp/hello/" to "/var/"
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


base_steps = {
    'copy_file_or_directory': CopyFileOrDirectory,
}
