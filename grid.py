import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from people import People
import sys

np.random.seed(42)

class Grid(object):
    def __init__(self, size, n_p):
        """
        :param size: int, size of the grid
        :param n_p: (4,) numpy array, [# of ppl of each status]
        """
        self.size = size
        self.all_p = []
        # [4, 5, 2, 3]
        # [0, 1, 2, 3]
        # [0, 1, 2, 3, 4] + 4
        for status, n in enumerate(n_p):
            gc = 0 if status == 0 else n_p[status-1]
            cur_list = [People(i+gc, np.random.randint(self.size, size=2),
                               size, age=0, status=status) 
                        for i in range(n)]
            self.all_p.extend(cur_list)
        self.to_pos_array()

    def to_pos_array(self):
        self.x = np.array([p.pos[0] for p in self.all_p]).reshape(1,-1)
        self.y = np.array([p.pos[1] for p in self.all_p]).reshape(1,-1)
        self.s = np.array([p.status for p in self.all_p]).reshape(1,-1)

    def get_sick_coord(self):
        sick_coord_set = set()
        for p in self.all_p:
            if p.status == 1:
                sick_coord_set.add(tuple(p.pos))
        print(sick_coord_set)
        return sick_coord_set

    def random_check(self, check_size=2, random=False):
        if random:
            check_list = np.random.choice(self.all_p, check_size, replace=False)
        else:
            check_list = self.all_p[:check_size]
        for p in check_list:
            p.report_status()

    def update(self):
        self.random_check()
        current_sick_coord = self.get_sick_coord()
        for p in self.all_p:
            if tuple(p.pos) in current_sick_coord:
                p.snb = True
            else:
                p.snb = False
            p.update_status()
        self.random_check()
        self.to_pos_array()

    def run(self, steps=100):
        for p in range(steps):
            print("="*60)
            print("Now on step {}/{} ...".format(step+1, steps))
            print("="*60)
            self.update()
        # self.report_status

    def plot_current(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set(xlim=(0, 100), ylim=(0, 100))
        scat = ax.scatter(self.x, self.y, c=self.s)
        plt.show()

    def report_status(self):
        a=0
        for p in range(p.all):
            if p.status==1:
                a+=1
        # 11 sick , ... recovered
        print("there are {} sick people".format(a))
        print("="*60)
        print("Now on step {}/{} ...".format(step+1, steps))
        print("="*60)

grid = Grid(10, [10, 10, 0, 0])
grid.run(100)
# grid.plot_current()
