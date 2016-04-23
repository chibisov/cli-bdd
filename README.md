## BDD for command-line applications

Inspired by [aruba](https://github.com/cucumber/aruba/).

[Documentation](http://chibisov.github.io/cli-bdd/).

[![Build Status](https://travis-ci.org/chibisov/cli-bdd.svg?branch=master)](https://travis-ci.org/chibisov/cli-bdd)
[![PyPI](https://img.shields.io/pypi/v/cli-bdd.svg?maxAge=2592000)]()
[![PyPI](https://img.shields.io/pypi/dm/cli-bdd.svg?maxAge=2592000)]()

```gherkin
Feature: showing off cli-bdd

    Scenario: create and remove file
        Given I cd to "/tmp/"
        Given a file "test.txt" with "some text"
        When I run `rm -i test.txt` interactively
        And I type "Yes"
        Then the file "/tmp/test.txt" should not exist
```
