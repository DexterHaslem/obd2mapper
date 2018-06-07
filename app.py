from csv import DictReader

from flask import Flask, render_template

from datapoint import DataPoint

app = Flask(__name__)

# TODO: let client upload a log
TESTFILE = 'obd2log_20180606.csv'


def parse_file():
    with open(TESTFILE) as f:
        reader = DictReader(f)
        # TODO: the files are logged in order, but it may be better
        # to parse date and handle in chrono. huge perf hit tho
        for row in reader:
            yield DataPoint(row)


def get_interped(pts):
    """showing 2000 points on a google map in a small area kills it,
    so interpolate between effective points
    """

    # TODO: make this more interesting lol
    return pts[::8]


ALL_POINTS = None
INTERP_POINTS = None


@app.route('/')
def hello():
    global ALL_POINTS
    global INTERP_POINTS
    if not ALL_POINTS:
        ALL_POINTS = list(parse_file())
        INTERP_POINTS = get_interped(ALL_POINTS)

    return render_template('map.html', datapoints=INTERP_POINTS)


if __name__ == '__main__':
    app.run()
