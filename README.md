## BDD for command-line applications

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
