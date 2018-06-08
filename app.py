import json

from flask import Flask, render_template

from TripData import TripData

app = Flask(__name__)

# TODO: let client upload a log
TESTFILE = 'trips/obd2log_20180606.csv'
TESTFILE2 = 'trips/obd2log_20180607.csv'

data = TripData(TESTFILE2)


@app.route('/mindist/<int:mindist>')
def get_points(mindist):
    filtered = data.filtered_by_dist(min_meters=mindist)

    dicts = []
    for p in filtered:
        d = {
            'lat': p.lat,
            'long': p.long,
            'speed': p.speed,
            'loiter': p.loiter
        }
        dicts.append(d)

    ret = {
        'points': dicts,
    }

    return json.dumps(ret)


@app.route('/')
def map():
    return render_template('map.html')


if __name__ == '__main__':
    app.run()
