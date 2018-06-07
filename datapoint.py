class DataPoint:
    """DataPoint represents a single parsed line from odb2 csv log"""

    def __init__(self, csvrow):
        # oh LAWD, the csv file has spaces in the header, so thats whats used
        # by Dict Reader rows, ouch :-( only SOME have it, check file
        self.long = float(csvrow[' Longitude'])
        self.lat = float(csvrow[' Latitude'])
        self.speed = float(csvrow['GPS Speed (Meters/second)'])
        self.alt = float(csvrow[' Altitude'])
