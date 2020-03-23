import numpy as np

np.random.seed(42)

class People(object):
    def __init__(self, pid, pos, move_limit, 
                 age=0, status=0,
                 days_rec=30, days_sick=0,
                 rate_g=0.2,
                 rate_d=0.1,
                 rate_s=0.0, 
                 sick_near_by=False):
        """
        :param pid: int, id of people
        :param pos: 2d numpy arr, x-y coord
        :param move_limit: upper limit of the x, y coordinates
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
        :param sick_near_by: bool, if there is a sick ppl on your position
        """
        self.pid = pid
        self.pos = pos
        self.limit = move_limit
        self.age = age
        self.status = status
        self.days_rec = days_rec
        self.days_sick = days_sick
        self.rate_g = rate_g
        self.rate_d = rate_d
        self.rate_s = rate_s
        self.snb = sick_near_by

    def report_status(self):
        print("Player{} position is ({})".format(self.pid,self.pos))
        if self.status == 0:
            print("Player{} is currently healthy".format(self.pid))
            if self.snb:
                print("There is some sick people nearby!")
            else:
                print("There is no sick people nearly!")
        elif self.status == 1:
            print ("Player{} is currently sick".format(self.pid))
            print("Player has been sick for {} days".format(self.days_sick))
        elif self.status == 2:
            print ("Player{} is currently recovered".format(self.pid))
        else:
            print("Player{} is dead".format(self.pid))
        print("Player {}'s age is {}".format(self.pid,self.age))

    def check_status(self):
        """
        check if the status of the subject is valid
        """
        # days_sick should always <= days_rec
        assert self.days_sick <= self.days_rec, "Invalid days being sick {} > {}".format(self.days_sick, self.days_rec)
        assert self.rate_g >= 0.0 and self.rate_g <= 1, "rate of getting sick cannot be negative or be more than 1"
        assert self.rate_s >= 0.0 and self.rate_s <= 1, "rate of  staying cannot be negative or be more than 1"
        assert self.rate_d >= 0.0 and self.rate_d <= 1, "rate of death cannot be a negative or be more than 1"
        assert self.days_sick >= 0, "days sick cannot be negative!"
        assert self.days_rec >= 0, "recovery days cannot be negative!"
        # TODO
        # assert ppl is inside the box
        if self.status == 0:
            assert self.days_sick == 0, "I'm healthy!"

    def get_sick(self):
        if self.status == 0 and self.snb:
            r = np.random.random()
            if r <= self.rate_g:
                self.status = 1

    def recover(self):
        if self.status == 1:
            if self.days_sick == self.days_rec:
                self.status = 2

    def update_days_sick(self):
        if self.status == 1:
            self.days_sick += 1

    def die(self):
        if self.status == 1:
            r = np.random.random()
            if r <= self.rate_d:
                self.status = 3

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
                if self.pos[0] < 0:
                    self.pos[0] += 2
                if self.pos[0] >= self.limit:
                    self.pos[0] -= 2
                if self.pos[1] < 0:
                    self.pos[1] += 2
                if self.pos[1] >= self.limit:
                    self.pos[1] -= 2

    def update_status(self):
        self.check_status()
        self.get_sick()
        self.recover()
        self.die()
        self.update_days_sick()
        self.walk()
        self.check_status()

#p = People(1, np.array([60,60]))
#p.report_status()
#p.check_status()
                  
