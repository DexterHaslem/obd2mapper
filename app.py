from flask import Flask, render_template

from TripData import TripData

app = Flask(__name__)

# TODO: let client upload a log
TESTFILE = 'trips/obd2log_20180606.csv'
TESTFILE2 = 'trips/obd2log_20180607.csv'

@app.route('/')
def hello():
    data = TripData(TESTFILE2)
    return render_template('map.html', datapoints=data.interp())


if __name__ == '__main__':
    app.run()
