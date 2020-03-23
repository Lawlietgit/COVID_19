import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from people import People

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
                               age=0, status=status, days_rec=30,
                               days_sick=0, rate_g=0.2, rate_d=0.0, rate_s=0.0) 
                        for i in range(n)]
            self.all_p.extend(cur_list)
        self.to_pos_array()

    def to_pos_array(self):
        self.x = np.array([p.pos[0] for p in self.all_p]).reshape(1,-1)
        self.y = np.array([p.pos[1] for p in self.all_p]).reshape(1,-1)
        self.s = np.array([p.status for p in self.all_p]).reshape(1,-1)

    def update(self):
        self.all_p = [p.walk() for p in self.all_p]

    def plot_current(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set(xlim=(-1, 100), ylim=(-1, 100))
        scat = ax.scatter(self.x, self.y, c=self.s)
        plt.show()

grid = Grid(100, [100,10,10,10])
#print(grid.all_p)
#grid.to_pos_array()
grid.plot_current()
