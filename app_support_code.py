from config import conf_debug
from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime


class AppSupport:

    @staticmethod
    def myprint(print_str):
        if conf_debug:   # change in file config.py
            print(print_str)

    @classmethod
    def datalines(cls, filey, data, special=0):
        first = "<br>BAD LINK-->  "
        sec = "<br><span id='errline'>&nbsp;*** ERROR-->  "
        third = "&emsp;&emsp;---> Found on: "
        fourth = "Here are your broken links:"
        if special == 1:
            first = "No broken links."
            sec = "No errors found."
            third = ""
            fourth = "Thanks for using LinkCheck."

        f = open(filey, 'w')
        f.write("<p></p><h3>" + fourth + "</h3><p></p>")

        for line in data:
            f.write(first)
            f.write("<a href='" + str(line[0]) + "'>")
            f.write(str(line[0])+ "</a>&ensp;")
            f.write(sec + str(line[1])+ "</span>&ensp;")  ## the error  # span needed!!
            f.write("<br><span  style=padding-bottom=4px>&ensp;&ensp;" + third + "<a href='")
            f.write(str(line[2]) + "'>")
            f.write(str(line[2])+ "</a></span>")
        f.close()


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)