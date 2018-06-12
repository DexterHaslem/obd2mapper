from csv import DictReader
from math import cos, sqrt, radians

from datapoint import DataPoint


# def _haversine_dist(self):
#     # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
#     pass

def _equirect_approx_dist_m(fromp, to):
    # we dont need full haversine distance approximate the meters diff
    EARTHRADIUS_M = 6372800
    x = radians(to.long - fromp.long) * cos(radians(fromp.lat + to.lat) / 2)
    y = radians(fromp.lat - to.lat)
    dist_m = sqrt(x * x + y * y) * EARTHRADIUS_M
    return abs(dist_m)


class TripData:
    def __init__(self, filename):
        self.data = []
        self.fn = filename
        self._parse_file()

    def _parse_file(self):
        with open(self.fn) as f:
            reader = DictReader(f)

            for row in reader:
                self.data.append(DataPoint(row))

    def _for_prev(self, fn):
        """Calls a function for each data point in data that has a
        previous point (first skipped).

        fn gets parameters of previous point, current point (which
        are DataPoint)"""
        prev = None
        for p in self.data:
            if not prev:
                prev = p
                continue

            fn(prev, p)

    def filtered_by_dist(self, min_meters=2):
        """Return a copy of the data points with data points less than
        `min_meters` away filtered out. All filtered out points are
        tallied as 'loiter' points
        """

        # TODO: make this interp and average all loiter'd points
        # bit of a hack, relies on data being in chronological order.
        # note this doesnt work for nearby points from laps

        filtered = []
        loiter_count = 0
        prev = None

        for p in self.data:
            if not prev:
                prev = p
                continue

            dist = _equirect_approx_dist_m(prev, p)
            if dist >= min_meters:
                p.loiter = loiter_count
                loiter_count = 0
                filtered.append(p)
                prev = p
            else:
                loiter_count += 1

        num_filtered = len(self.data) - len(filtered)
        print('filtered {} data points'.format(num_filtered))
        return filtered

    def total_length_meters(self):
        """Returns total length of trip in meters. Rounded to two decimals
        for pretty printing"""
        prev = None
        total = 0
        for p in self.data:
            if not prev:
                prev = p
                continue

            total += _equirect_approx_dist_m(prev, p)
            prev = p

        return round(total, 2)

    def total_altitude_traversed(self):
        """Returns total meters effectively traversed up/down.
        Rounded to two decimals for pretty printing"""
        prev = None
        total = 0
        for p in self.data:
            if not prev:
                prev = p
                continue

            total += abs(prev.alt - p.alt)
            prev = p

        return round(total, 2)

    def avg_mps(self):
        """Returns average meters per second for all the data points in the trip.
        Rounded to two decimals for pretty printing"""
        total_mps = sum([p.speed for p in self.data])
        avg = total_mps / len(self.data)
        return round(avg, 2)
