### Imperial DOC utility: Request LabTS Test

This repository contains python scripts for programatically requesting execution of test on the DOC LabTS platform using your credentials.

To learn how to use the standalone script run `python3 request_test.py --help`

To set up the CGI script on your college-provided hosting first copy `request_test.cgi` and `request_test.py` into your `public_html` directory on a lab machine (you can do it via ssh), and then consult the [Computing Suport Group guide to hosting CGI scripts](https://www.imperial.ac.uk/computing/people/csg/guides/web-hosting/cgi/) to set the permissions correctly.

To learn how to use the CGI script refer to its included documentation at the top of the file.

Example usage:
```
curl -X POST "https://www.doc.ic.ac.uk/~<user_id>/request_test.cgi" -d "commit_id=<sth>&exercise=<sth>&milestone=<sth>&repo_id=<sth>&user_id=<user_id>&password=<password>"
```