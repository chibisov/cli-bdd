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


class ChangeDirectory(StepBase):
    """Change directory.

    Examples:

    ```gherkin
    Given I cd to "/tmp/test/"
    ```
    """
    type_ = 'given'
    sentence = 'I cd to "(?P<dir_path>[^"]*)"'

    def step(self, dir_path):
        os.chdir(dir_path)


class CreateFileWithContent(StepBase):
    """Creates a file.

    Examples:

    ```gherkin
    Given a file "/tmp/test/" with "some content"
    Given the file named "/tmp/test/" with "another content"
    ```
    """
    type_ = 'given'
    sentence = (
        '(a|the) file'
        '( named)? "(?P<file_path>[^"]*)" with "(?P<file_content>[^"]*)"'
    )

    def step(self, file_path, file_content):
        with open(file_path, 'wt') as ff:
            ff.write(file_content)


class CreateFileWithMultilineContent(StepBase):
    '''Creates a file with multiline content.

    Examples:

    ```gherkin
    Given a file "/tmp/test/" with:
        """
        line one
        line two
        line three
        """

    Given a file named "/tmp/test/" with:
        """
        line one
        line two
        line three
        """
    ```
    '''
    type_ = 'given'
    sentence = (
        '(a|the) file'
        '( named)? "(?P<file_path>[^"]*)" with'
    )

    def step(self, file_path):
        with open(file_path, 'wt') as ff:
            ff.write(self.get_text())


class CheckFileOrDirectoryExist(StepBase):
    """Checks whether file or directory exist.

    Examples:

    ```gherkin
    Then a file "/var/new.txt" should exist
    Then the file named "/var/new.txt" should not exist
    Then the directory "/var/" should not exist
    ```
    """
    type_ = 'then'
    sentence = (
        '(a|the) (?P<file_or_directory>(file|directory))'
        '( (named|from))? "(?P<path>[^"]*)" should( (?P<should_not>not))? exist'
    )

    def step(self, file_or_directory, path, should_not=None):
        assert_that(
            os.path.exists(path),
            equal_to(not should_not)
        )


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
    {
        'func_name': 'change_directory',
        'class': ChangeDirectory
    },
    {
        'func_name': 'create_file_with_content',
        'class': CreateFileWithContent
    },
    {
        'func_name': 'create_file_with_multiline_content',
        'class': CreateFileWithMultilineContent
    },
    {
        'func_name': 'check_file_or_directory_exist',
        'class': CheckFileOrDirectoryExist
    }
]
