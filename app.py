import json

from flask import Flask, render_template

from TripData import TripData

app = Flask(__name__)

# TODO: let client upload a log
TESTFILE = 'trips/obd2log_20180606.csv'
TESTFILE2 = 'trips/obd2log_20180607.csv'

trip = TripData(TESTFILE2)


@app.route('/mindist/<int:mindist>')
def get_points(mindist):
    filtered = trip.filtered_by_dist(min_meters=mindist)

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
def index():
    return render_template('map.html')


@app.route('/stats')
def stats():
    length = trip.total_length_meters()
    alt = trip.total_altitude_traversed()
    avg_mps = trip.avg_mps()

    return json.dumps({
        'total_length_meters': length,
        'total_alt_meters': alt,
        'avg_mps': avg_mps
    })


if __name__ == '__main__':
    app.run()
