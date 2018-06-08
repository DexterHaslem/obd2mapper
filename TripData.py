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
            # TODO: the files are logged in order, but it may be better
            # to parse date and handle in chrono. huge perf hit tho
            for row in reader:
                self.data.append(DataPoint(row))

    def _haversine_dist(self):
        # a = sin²(Δφ/2) + cos φ1 ⋅ cos φ2 ⋅ sin²(Δλ/2)
        pass

    def _equirect_approx_dist_m(self, fromp, to):
        # we dont need full haversine distance
        # approximate the meters diff
        # EARTHRADIUS_KM = 6372.8
        EARTHRADIUS_M = 6372800
        x = radians(to.long - fromp.long) * cos(radians(fromp.lat + to.lat) / 2)
        y = radians(fromp.lat - to.lat)
        dist_m = sqrt(x * x + y * y) * EARTHRADIUS_M
        return dist_m

    def interp(self, min_meters=10):
        """showing 2000 points on a google map in a small area kills it,
        interpolate between effective points.

        This is done by setting a min number of distance between points,
        grouping points that are all within the
        threshold and keeping track how many 'loitering' points there are
        """

        # TODO: this could be optimized
        # bit of a hack, relies on data being in chronological order
        # so this doesnt work for nearby points from LAPS

        filtered = []
        maxlen = len(self.data)

        last_good_idx = 0
        # cant use a for loop, we are monkey jumping with peeking
        for idx in range(maxlen):
            cur_pt = self.data[idx]

            if idx < maxlen - 1:
                # if we are far enough away from next one, add to list
                # (forward peeking)
                next_idx = idx + 1
                next_pt = self.data[next_idx]
                md = self._equirect_approx_dist_m(cur_pt, next_pt)
                if md >= min_meters:
                    # see how many points we skipped
                    loiter_count = next_idx - last_good_idx
                    filtered.append(cur_pt)
                    cur_pt.loiter = loiter_count
                    last_good_idx = idx

        # while idx < maxlen:
        #     cur_pt = self.data[idx]
        #     filtered.append(cur_pt)
        #
        #     # keep peeking at next until we get far enough away
        #     idx += 1
        #
        #     while idx < maxlen:
        #         next_pt = self.data[idx]
        #         md = self._equirect_approx_dist_m(cur_pt, next_pt)
        #         if md >= min_meters:
        #             # this is a ghetto monkey jump. we are far enough away
        #             # to be the next point
        #             idx = next
        #             break
        #         next += 1
        print('interp: returned {} out of {} points'.format(len(filtered), maxlen))
        return filtered

    def as_google_features(self):
        pass
