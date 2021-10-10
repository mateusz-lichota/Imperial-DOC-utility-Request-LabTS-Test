#!/usr/bin/python3
"""
This is a CGI script for programatically requesting test execution on LabTS. 
To use it, make a POST request to the server it is hosted on. 
Required parameters (supply them in POST data. Example: curl -X POST <url> -d "user_id=<sth>&password=<sth>&..."):
    - user_id           your college id
    - password          your college password
    - exercise_number   you can find it in the LabTS url (.../exercises/<here>/repository/...)
    - repository_id     you can find it in the LabTS url (.../repository/<here>?milestone...)
    - milestone         you can find it in the LabTS url (.../repository/<somenumber>?milestone=<here>)
    - commit_id         for this script to make sense you need to somehow get it programatically
"""
import sys
import subprocess
import cgi
import cgitb
cgitb.enable()

# This line is required for the server to properly execute this script.
# Removing it results in server error 500.
print("Content-Type:text/html\r\n\r\n")


# Ensure that required packages are installed, as the Apache server running this file
# is using a different python version on a different machine, and possibly different system
command = [sys.executable, "-m", "pip", "install", "--user", 'requests lxml']
subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

import requests
import lxml.html


# Accessing values stored in cgi.FieldStorage is problematic, 
# so this wrapper makes them accessible via dot notation.
args = type('ArgsDotGetter', (cgi.FieldStorage,), {'__getattr__': lambda s, k: s.__getitem__(k).value})()


labts_page_url = f'https://teaching.doc.ic.ac.uk/labts'
login_page_url = f'{labts_page_url}/users/sign_in'
repo_page_url  = f'{labts_page_url}/lab_exercises/2122/exercises/{args.exercise_number}/repository/{args.repository_id}'
request_url    = f'{repo_page_url}/request?commit_id={args.commit_id}&milestone={args.milestone}'

session = requests.Session()

login_page_content = session.get(login_page_url).content
login_page_tree = lxml.html.fromstring(login_page_content)
auth_token = login_page_tree.xpath('/html/body/div[1]/form/input[2]/@value')[0]


session.post(login_page_url, data=[
    ('utf8', '✓'),
    ('authenticity_token', auth_token),
    ('user[uid]', args.user_id),
    ('user[password]', args.password),
    ('user[remeber_me]', '0'),
    ('commit', 'Sign in'),
])

repo_page_content = session.get(repo_page_url).content
repo_page_tree = lxml.html.fromstring(repo_page_content)
auth_token = repo_page_tree.xpath('/html/head/meta[2]/@content')[0]

session.post(request_url, data=[
    ('_method', 'post'),
    ('authenticity_token', auth_token),
])
