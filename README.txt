Implemented basic set of positive tests for 'https://beta.1neschool.com' API testing.
Used simple test management python framework 'unittest' for running tests.

The tests set contains one positive test-case for each API method and just illustrate the test implementation ability. Of course the test set can be enlarged and there are a lot of thinks to test to cover all functionality.

In case of need I can implement professional test running management system and it will support following:

 - file system structure to separate tests into testsuites, testgroups, etc, based on business or functional requreiements
 - test flow runner
 - filter sub set of tests to be run (by options, file, labeling, etc)
 - data driven testing (load test data from external files)
 - behavior driven testing (use technique to implement behavioral tests)
 - test templating (implement template tests and generate set of tests based on template's data) 
 - logging mechanism
 - debug levels for reporting
 - good filterable reports (shell, HTML, pdf, XML, etc)
 - results mailing
 - other specific requests for testing and testing flow control

Requirements:
Python2.7
    json, requests, unittest modules

To be able to run tests just invoke following from terminal (linux, osx) or powerShell (windows):
 python test_api.py

Basic report will be printed in shell.

Note: 1st test trying to create user with specified userId. Just change the USERID variable value in top of test_api.py file with unique username for proper running.

