#!/usr/bin/python3
"""
This is a script for programatically requesting test execution on LabTS (https://teaching.doc.ic.ac.uk/labts).
"""
import sys
import warnings
import argparse
import requests
import lxml.html

def request_test(*, user_id, password, exercise_number, repository_id, milestone, commit_id):
    login_page_url = f'https://teaching.doc.ic.ac.uk/labts/users/sign_in'
    repo_page_url  = f'https://teaching.doc.ic.ac.uk/labts/lab_exercises/2122/exercises/{exercise_number}/repository/{repository_id}'
    request_url    = f'https://teaching.doc.ic.ac.uk/labts/lab_exercises/2122/exercises/{exercise_number}/repository/{repository_id}/request?commit_id={commit_id}&milestone={milestone}'

    session = requests.Session()

    login_page_content = session.get(login_page_url).content
    login_page_tree = lxml.html.fromstring(login_page_content)
    auth_token = login_page_tree.xpath('/html/body/div[1]/form/input[2]/@value')[0]


    session.post(login_page_url, data=[
        ('utf8', '✓'),
        ('authenticity_token', auth_token),
        ('user[uid]', user_id),
        ('user[password]', password),
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

if __name__ == '__main__':
    def make_wide(formatter, w=90, h=36):
        """Return a wider HelpFormatter, if possible."""
        try:
            # https://stackoverflow.com/a/5464440
            # beware: "Only the name of this class is considered a public API."
            kwargs = {'width': w, 'max_help_position': h}
            formatter(None, **kwargs)
            return lambda prog: formatter(prog, **kwargs)
        except TypeError:
            warnings.warn("argparse help formatter failed, falling back.")
            return formatter


    p = argparse.ArgumentParser(description=__doc__, formatter_class=make_wide(argparse.HelpFormatter))
    
    requiredNamed = p.add_argument_group('required named arguments')
    requiredNamed.add_argument("--user_id",   required=True, type=str, help="your college id")
    requiredNamed.add_argument("--password",  required=True, type=str, help="your college password")
    requiredNamed.add_argument("--repo_id",   required=True, type=int, help="'.../repository/<here>?...' in the LabTS url")
    requiredNamed.add_argument("--exercise",  required=True, type=int, help="'.../exercises/<here>/...' in the LabTS url")
    requiredNamed.add_argument("--milestone", required=True, type=int, help="'...?milestone=<here>' in the LabTS url")
    requiredNamed.add_argument("--commit_id", required=True, type=int, help="you need to somehow get it programatically")
    p.add_argument("-v", "--verbose",   action='store_true', help="verbose output")

    if len(sys.argv) == 1:
        p.print_help()
        exit()

    args = p.parse_args()
    
    request_test(
        user_id=          args.user_id,
        password=         args.password,
        exercise_number=  args.exercise,
        repository_id=    args.repo_id,
        milestone=        args.milestone,
        commit_id=        args.commit_id,
    )