from datetime import datetime

# Wed Jun 06 17:37:55 MDT 2018
# timezone is dropped! See below
TIMEFMT = '%a %b %d %H:%M:%S %Y'


class DataPoint:
    """DataPoint represents a single parsed line from odb2 csv log"""

    def __init__(self, csvrow):
        # oh LAWD, the csv file has spaces in the header, so thats whats used
        # by Dict Reader rows, ouch :-( only SOME have it, check file
        self.long = float(csvrow[' Longitude'])
        self.lat = float(csvrow[' Latitude'])
        self.speed = float(csvrow['GPS Speed (Meters/second)'])
        self.alt = float(csvrow[' Altitude'])
        # HACK: here be dragons: datetime.strptime cant handle %Z / 'MDT'
        # just drop timezone for this prototype
        self.time = datetime.strptime(csvrow['GPS Time'].replace(' MDT', ''), TIMEFMT)
