<h1>BDD for command-line applications</h1>

Inspired by [aruba](https://github.com/cucumber/aruba/).

```gherkin
Feature: showing off cli-bdd

    Scenario: create and remove file
        Given I cd to "/tmp/"
        Given a file "test.txt" with "some text"
        When I run `rm -i test.txt` interactively
        And I type "Yes"
        Then the file "/tmp/test.txt" should not exist
```


[Source repository on Github](https://github.com/chibisov/cli-bdd).

Installation:

```
$ pip install cli-bdd
```

Read the docs how to use `cli-bdd` with [behave](/behave/) and [lettuce](/lettuce/).
