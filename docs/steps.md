
# Command

Module: `cli_bdd.core.steps.command`


### run_command

Runs a command.

Examples:

```gherkin
When I run `echo hello`
```

Matcher:
```
I run `(?P<command>[^`]*)`
```


### successfully_run_command

Runs a command and checks it for successfull status.


Examples:

```gherkin
When I successfully run `echo hello`
```

Matcher:
```
I successfully run `(?P<command>.*)`
```


### run_command_interactively

Runs a command in interactive mode.

Examples:

```gherkin
When I run `rm -i hello.txt` interactively
```

Matcher:
```
I run `(?P<command>[^`]*)` interactively
```


### type_into_command

Types an input into the previously ran in interactive mode command.

Examples:

```gherkin
When I type "Yes"
```

Matcher:
```
I type "(?P<input_>[^"]*)"
```


### got_interactive_dialog

Waits for a dialog.

By default waits for 1 second. Timeout could be changed by providing
`in N seconds` information.

Examples:

```gherkin
When I got "Password:" for interactive dialog
When I got "Password:" for interactive dialog in 1 second
When I got "Name .*: " for interactive dialog in 0.01 seconds
```

Matcher:
```
I got "(?P<dialog_matcher>[^"]*)" for interactive dialog( in (?P<timeout>(\d*[.])?\d+) seconds?)?
```


### output_should_contain_text

Checks the command output (stdout, stderr).

Examples:

```gherkin
Then the output should contain:
    """
    hello
    """

Then the output should contain exactly:
    """
    hello
    """

Then the stderr should not contain exactly:
    """
    hello
    """
```

Matcher:
```
the (?P<output>(output|stderr|stdout)) should( (?P<should_not>not))? contain( (?P<exactly>exactly))?
```


### exit_status_should_be

Checks the command status code.

Examples:

```gherkin
Then the exit status should be 1
Then the exit status should not be 1
```

Matcher:
```
the exit status should( (?P<should_not>not))? be (?P<exit_status>\d+)
```




# Environment

Module: `cli_bdd.core.steps.environment`


### set_the_environment_variable

Sets the environment variable.

Examples:

```gherkin
Given I set the environment variable "hello" to "world"
```

Matcher:
```
I set the environment variable "(?P<variable>.*)" to "(?P<value>.*)"
```


### append_to_the_environment_variable

Appends a value to the environment variable.

Examples:

```gherkin
Given I append "world" to the environment variable "hello"
```

Matcher:
```
I append "(?P<value>.*)" to the environment variable "(?P<variable>.*)"
```


### prepend_to_the_environment_variable

Prepends a value to the environment variable.

Examples:

```gherkin
Given I prepend "world" to the environment variable "hello"
```

Matcher:
```
I prepend "(?P<value>.*)" to the environment variable "(?P<variable>.*)"
```


### set_the_environment_variables

Populates the set of the environment variables.

Examples:

```gherkin
Given I set the environment variables to:
    | variable | value |
    | age      | 25    |
    | name     | gena  |
```

Matcher:
```
I set the environment variables to
```


### append_the_values_to_the_environment_variables

Appends the values to the set of the environment variables.

Examples:
```gherkin
I append the values to the environment variables:
    | variable | value |
    | age      | 1     |
    | name     | a     |
```

Matcher:
```
I append the values to the environment variables
```


### prepend_the_values_to_the_environment_variables

Prepends the values to the set of the environment variables.

Examples:

```gherkin
I prepend the values to the environment variables:
    | variable | value |
    | age      | 1     |
    | name     | a     |
```

Matcher:
```
I prepend the values to the environment variables
```




# File

Module: `cli_bdd.core.steps.file`


### copy_file_or_directory

Copies a file or directory.

Examples:

```gherkin
Given I copy a file from "/tmp/old.txt" to "/var/new.txt"
Given I copy the file named "hello.txt" to "/var/"
Given I copy a directory from "/tmp/hello/" to "/var/"
```

Matcher:
```
I copy (a|the) (?P<file_or_directory>(file|directory))( (named|from))? "(?P<source>[^"]*)" to "(?P<destination>[^"]*)"
```


### move_file_or_directory

Moves a file or directory.

Examples:

```gherkin
Given I move a file from "/tmp/old.txt" to "/var/new.txt"
Given I move the file named "hello.txt" to "/var/"
Given I move a directory from "/tmp/hello/" to "/var/"
```

Matcher:
```
I move (a|the) (?P<file_or_directory>(file|directory))( (named|from))? "(?P<source>[^"]*)" to "(?P<destination>[^"]*)"
```


### create_directory

Creates directory.

Examples:

```gherkin
Given a directory "/tmp/test/"
Given the directory named "/tmp/test/"
```

Matcher:
```
(a|the) directory( named)? "(?P<dir_path>[^"]*)"
```


### change_directory

Change directory.

Examples:

```gherkin
Given I cd to "/tmp/test/"
```

Matcher:
```
I cd to "(?P<dir_path>[^"]*)"
```


### create_file_with_content

Creates a file.

Examples:

```gherkin
Given a file "/tmp/test/" with "some content"
Given the file named "/tmp/test/" with "another content"
```

Matcher:
```
(a|the) file( named)? "(?P<file_path>[^"]*)" with "(?P<file_content>[^"]*)"
```


### create_file_with_multiline_content

Creates a file with multiline content.

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

Matcher:
```
(a|the) file( named)? "(?P<file_path>[^"]*)" with
```


### check_file_or_directory_exist

Checks whether file or directory exist.

Examples:

```gherkin
Then a file "/var/new.txt" should exist
Then the file named "/var/new.txt" should not exist
Then the directory "/var/" should not exist
```

Matcher:
```
(a|the) (?P<file_or_directory>(file|directory))( (named|from))? "(?P<path>[^"]*)" should( (?P<should_not>not))? exist
```



