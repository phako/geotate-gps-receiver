from flask import Flask, request

import datetime

app = Flask(__name__)

# @app.route('/gws/2008.03.04/time.ashx')
@app.route('/', methods=['GET', 'POST'])
def time():
    print(request.headers)
    if request.method == "POST":
        print(request.data)
    t = datetime.datetime.now(datetime.timezone.utc)
    return f"0019:38:00.000 18-10-23"

if __name__ == '__main__':
    app.run(debug=True, port=8899)