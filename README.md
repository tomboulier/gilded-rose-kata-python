# Gilded Rose starting position in Python

This is the starting position for the Gilded Rose refactoring kata in Python,
taken from the [Gilded Rose Kata](https://github.com/emilybache/GildedRose-Refactoring-Kata) by Emily Bache.

For exercise instructions see [Gilded Rose requirements (in french)](gilded_rose_requirements.md).

Suggestion: create a python virtual environment for this project. See the [documentation](https://docs.python.org/3/library/venv.html)

## Run the unit tests from the Command-Line

```
python -m unittest
```

## Run the TextTest fixture from the Command-Line

For e.g. 10 days:

```
python texttest_fixture.py 10
```

You should make sure the command shown above works when you execute it in a terminal before trying to use TextTest (see below).


## Run the TextTest approval test that comes with this project

There are instructions in the [TextTest Readme](../texttests/README.md) for setting up TextTest. You will need to specify the Python executable and interpreter in [config.gr](../texttests/config.gr). Uncomment these lines:

    executable:${TEXTTEST_HOME}/python/texttest_fixture.py
    interpreter:python

## Run the ApprovalTests.Python test

This test uses the framework [ApprovalTests.Python](https://github.com/approvals/ApprovalTests.Python). You will need to install  Run it like this:

```
python tests/test_gilded_rose_approvals.py
```

You will need to approve the output file which appears under "approved_files" by renaming it from xxx.received.txt to xxx.approved.txt.
