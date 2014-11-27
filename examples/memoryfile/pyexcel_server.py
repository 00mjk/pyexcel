"""
pyexcel_server.py
:copyright: (c) 2014 by C. W.
:license: GPL v3

This shows how to use pyexcel to handle excel file upload. In order
to evaluate it, please install Flask::

    pip install Flask
    python flaskserver.py

Then visit http://localhost:5000/upload

Flask is a micro framework for web development. For more infomation,
please visit: http://flask.pocoo.org
"""
import sys
from flask import Flask, request, render_template, jsonify, make_response
import pyexcel as pe
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'excel' in request.files:
        # handle file upload
        filename = request.files['excel'].filename
        extension = filename.split(".")[1]
        # Obtain the file extension and content
        # pass a tuple instead of a file name
        sheet = pe.load_from_memory(extension, request.files['excel'].read())
        # then use it as usual
        data = sheet.to_dict()
        # respond with a json
        return jsonify({"result":data})
    return render_template('upload.html')
    
data = [
    ["REVIEW_DATE","AUTHOR","ISBN","DISCOUNTED_PRICE"],
    ["1985/01/21","Douglas Adams",'0345391802',5.95],
    ["1990/01/12","Douglas Hofstadter",'0465026567',9.95],
    ["1998/07/15","Timothy \"The Parser\" Campbell",'0968411304',18.99],
    ["1999/12/03","Richard Friedman",'0060630353',5.95],
    ["2004/10/04","Randel Helms",'0879755725',4.50]
]

@app.route('/download')
def download():
    sheet = pe.Sheet(data)
    io = StringIO()
    sheet.save_to_memory("csv", io)
    output = make_response(io.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    # start web server
    app.run()
