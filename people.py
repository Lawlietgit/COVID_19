import numpy as np

class People(object):
    def __init__(self, pid, pos, age=0, status=0, days_rec=30, 
                 days_sick=0,
                 rate_g=0.2,
                 rate_d=0.01,
                 rate_s=0.0):
        """
        :param pid: int, id of people
        :param pos: 2d numpy arr, x-y coord
        :param status: int
            0 - healthy,
            1 - sick,
            2 - recovered
            3 - died
        :param age: int
        :param days_sick: int, days since sick
        :param days_rec: int, days to recover
        :param rate_g: float, the rate of getting sick
                       when making contact with sick ppl
        :param rate_d: float, rate of sick ppl to die
        :param rate_s: float, rate of ppl to stay
        """
        self.pid = pid
        self.pos = pos
        self.age = age
        self.status = status
        self.days_rec = days_rec
        self.days_sick = days_sick
        self.rate_g = rate_g
        self.rate_d = rate_d
        self.rate_s = rate_s

    def report_status(self):
        """
        report the status of the subject people
            [pid, status, days, ...]
        """
        # TODO

    def check_status(self):
        """
        check if the status of the subject is valid
        """
        # days_sick should always <= days_rec
        assert self.days_sick <= self.days_rec, "Invalid days being sick {} > {}".format(self.days_sick, self.days_rec)
        assert self.rate_g >= 0.0, "rate of getting sick cannot be negative!"
        if self.status == 0:
            assert self.days_sick == 0, "I'm healthy!"
        # TODO


    def walk(self):
        if self.status != 3:
            r = np.random.random()
            if r > self.rate_s:
               r_dir = np.random.random()
               if r_dir < 0.125: # up
                   step = np.array([1,0])
               elif r_dir < 0.25: # left, up
                   step = np.array([-1,1])
               elif r_dir < 0.375: # left
                   step = np.array([-1,0])
               elif r_dir < 0.5: # left, down
                   step = np.array([-1,-1])
               elif r_dir < 0.625: # down
                   step = np.array([0,-1])
               elif r_dir < 0.75: # right, down
                   step = np.array([1,-1])
               elif r_dir < 0.875: # right
                   step = np.array([1,0])
               else: # right, up
                   step = np.array([1,1])
               self.pos += step
