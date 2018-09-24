#!/usr/local/bin/python3.7

import os
import cgi
import cgitb
import sys

cgitb.enable()


def on_GET(request, form):

    sys.stderr.write(str(form))

    print("Content-type: text/html")
    print()
    print("<html>")
    print("<center>Hello</center>")
    print("<p>this is some text</p>")
    print("<p>%s</p>" % request)
    print("</html>")


def on_PUT(request):
    pass


def on_POST(request, form):

    #sys.stderr.write(str(request))
    #sys.stderr.write(str(form))

    # Get data from fields
    artist = form.getvalue('artist_name')
    song = form.getvalue('song_name')


def on_DELETE(request):
    pass


def main():
    request = os.environ['REQUEST_METHOD']

    fp = open('database.csv', 'a')
    form = cgi.FieldStorage()

    if request == 'GET':
        on_GET(request, form)

    elif request == 'PUT':
        pass

    elif request == 'POST':
        on_POST(request, form)

    elif request == 'DELETE':
        pass


if __name__ == '__main__':
    main()
