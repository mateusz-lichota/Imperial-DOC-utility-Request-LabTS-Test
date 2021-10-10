#!/usr/bin/python3
"""
This is a CGI script for programatically requesting test execution on LabTS. 
To use it, make a POST request to the server it is hosted on. 
Required parameters (supply them in POST data. Example: curl -X POST <url> -d "user_id=<sth>&password=<sth>&..."):
    - user_id        your college id
    - password       your college password
    - repo_id        '.../repository/<here>?...' in the LabTS url
    - exercise       '.../exercises/<here>/...' in the LabTS url
    - milestone      '...?milestone=<here>' in the LabTS url
    - commit_id      you need to somehow get it programatically
"""
import sys
import subprocess
import cgi
import cgitb
from request_test import request_test
cgitb.enable()

# This line is required for the server to properly execute this script.
# Removing it results in server error 500.
print("Content-Type:text/html\r\n\r\n")


# Ensure that required packages are installed, as the Apache server running this file
# is using a different python version on a different machine, and possibly different system
command = [sys.executable, "-m", "pip", "install", "--user", 'requests lxml']
subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()


# Accessing values stored in cgi.FieldStorage is problematic, 
# so this wrapper makes them accessible via dot notation.
args = type('ArgsDotGetter', (cgi.FieldStorage,), {'__getattr__': lambda s, k: s.__getitem__(k).value})()

request_test(
    user_id=          args.user_id,
    password=         args.password,
    exercise_number=  args.exercise,
    repository_id=    args.repo_id,
    milestone=        args.milestone,
    commit_id=        args.commit_id,
)