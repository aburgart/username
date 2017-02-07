#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi #this will validate user imput
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
<    </style>
</head>
<body>
    <h1>
        <a href="/">Signup</a>
    </h1>
"""


page_footer = """
</body>
</html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile("^.{3,20}$")
def valid_password(password):
    if not PASS_RE.match(password):
        return False
    else:
        return True
def valid_verifiedpassword(password,verifypassword):
    return password == verifypassword

EMAIL_RE = re.compile("^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    if email =="":
        return True
    else:
        return EMAIL_RE.match(email)

form = """
        <form action="/" method="post">
        <label>
            Username
            <input type="text" name="username"/>
            <span>%(usernameerror)s</span>
        </label>
        <br>
        <label>
            Password
        </label>
            <input type="password" name="password"/>
            <span>%(passworderror)s</span>

        <br>
        <label>
            Verify Password
            <input type="password" name="verifypassword"/>
            <span>%(verifypassworderror)s</span>
        </label>
        <br>
        <label>
            Email (optional)
            <input type="text" name="the-email"/>
            <span>%(emailerror)s</span>
        </label>
        <br>
        <input type="submit" value="submit"/>
    </form>
    """


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.signup.com/
    """

    def get(self):
        usernameerror=passworderror=emailerror=verifypassworderror=""
        content = page_header + form %{"usernameerror":usernameerror,
                                        "passworderror":passworderror,
                                        "verifypassworderror":verifypassworderror,
                                        "emailerror":emailerror} + page_footer
        self.response.write(content)
        # username_options=""
        # if valid_username(username) :
        #     username_options+= '<option value="{0}">{0}</option>'.format(username)


    def post(self):

        user_name = self.request.get("username")
        user_password = self.request.get("password")
        user_verifiedpassword=self.request.get("verifypassword")
        user_email = self.request.get("email")

        error=0

        usernameerror=passworderror=emailerror=verifypassworderror=""
        if not valid_username(user_name):
            usernameerror = "Not a valid username"
            error+=1
        if not valid_password(user_password):
            passworderror = "Not a valid password"
            error+=1
        if not valid_verifiedpassword(user_password,user_verifiedpassword):
            verifypassworderror ="Your password does not match"
            error+=1
        if not valid_email(user_email):
            emailerror="Not a valid email"
            error+=1

        if error > 0:
            content = page_header + form %{"usernameerror":usernameerror,
                                        "passworderror":passworderror,
                                        "verifypassworderror":verifypassworderror,
                                        "emailerror":emailerror} + page_footer
            self.response.write(content)

        else:
            self.response.write("welcome , " + user_name)



class User(webapp2.RequestHandler):


    def get(self):
        new_user = self.request.get("username")
        real_password = self.request.get("password")
        correct_email = self.request.get("the-email")

        self.response.write("<h1>welcome " + new_user + "</h1>")


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', User)


], debug=True)
