from csv import DictReader
from math import cos, sqrt, radians

from datapoint import DataPoint


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

    # def _haversine_dist(self):
    #     # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
    #     pass

    def _equirect_approx_dist_m(self, fromp, to):
        # we dont need full haversine distance
        # approximate the meters diff
        # EARTHRADIUS_KM = 6372.8
        EARTHRADIUS_M = 6372800
        x = radians(to.long - fromp.long) * cos(radians(fromp.lat + to.lat) / 2)
        y = radians(fromp.lat - to.lat)
        dist_m = sqrt(x * x + y * y) * EARTHRADIUS_M
        return abs(dist_m)

    def filtered_by_dist(self, min_meters=2):
        """Return a copy of the data points with data points less than `min_meters` away filtered
        out. All filtered out points are tallied as 'loiter' points
        """
        # TODO: make this interp and average all loiter'd points
        # bit of a hack, relies on data being in chronological order
        # so this doesnt work for nearby points from LAPS

        filtered = []
        maxlen = len(self.data)

        last_pt = None
        skip_tally = 0

        for idx in range(maxlen):
            cur_pt = self.data[idx]
            #cur_pt.loiter = skip_tally

            if not last_pt:
                cur_pt.loiter = 0
                filtered.append(cur_pt)
                last_pt = cur_pt
                continue

            # if we are far enough away from last saved point, add us and make us most recent point
            md = self._equirect_approx_dist_m(last_pt, cur_pt)
            if md >= min_meters:
                cur_pt.loiter = skip_tally
                filtered.append(cur_pt)
                last_pt = cur_pt
                skip_tally = 0
            else:
                skip_tally += 1

        return filtered
