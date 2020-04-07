import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anime
from people import People
import sys

np.random.seed(42)

class Grid(object):
    def __init__(self, size, n_p, steps=100):
        """
        :param size: int, size of the grid
        :param n_p: (4,) numpy array, [# of ppl of each status]
        """
        self.size = size
        self.all_p = []
        self.total_p = sum(n_p) # sum of the n_p list, indicating total number of ppl
        self.steps = steps # this is the total number of steps you simulate
        for status, n in enumerate(n_p):
            gc = 0 if status == 0 else n_p[status-1]
            cur_list = [People(i+gc, np.random.randint(self.size, size=2),
                               size, age=0, status=status) 
                        for i in range(n)]
            self.all_p.extend(cur_list)
        self.to_pos_array()
        # Setup the figure and axes...
        self.ims = []
        self.fig, (self.ax, self.ax2) = plt.subplots(1,2)
        self.sick_count = []
        self.dead_count = []
        # Then setup FuncAnimation.
#        self.ani = anime.FuncAnimation(self.fig, self.update, interval=200,
                                       # interval it is the time between your snapshots in ms
#                                       init_func=self.setup_plot, blit=True)
        self.stop = False

    def get_anime(self):
        """Initial drawing of the scatter plot."""
        for step in range(self.steps):
            self.update_allp(step)
            self.scat = self.ax.scatter(self.x, self.y, c=self.s, s=3.0, animated=True, cmap='gist_rainbow')
            classes = ['healthy', 'sick', 'recovered', 'died']
            self.ax.axis([0, self.size, 0, self.size])
            self.ax.legend(handles=self.scat.legend_elements()[0], labels=classes,
                        bbox_to_anchor=(-0.08, 0.85, 1.0, 0.2),
                        fancybox = True, ncol=2,
                        labelspacing=0.1,
                        borderpad=0.1,
                        shadow=True)
            self.ax.set_title("COVID-19 MC", pad=15)
            self.plot1, = self.ax2.plot(self.sick_count, 'b')
            self.plot2, = self.ax2.plot(self.dead_count, 'k')
            self.ax2.axis([0, self.steps, 0, self.total_p])

            # For FuncAnimation's sake, we need to return the artist we'll be using
            # Note that it expects a sequence of artists, thus the trailing comma.
            self.ims.append([self.scat, self.plot1, self.plot2])
            if self.stop:
                break
        self.ani = anime.ArtistAnimation(self.fig, self.ims, interval=200, blit=True)

    def show(self):
        self.get_anime()
        plt.show()

    def to_pos_array(self):
        self.x = np.array([p.pos[0] for p in self.all_p]).reshape(1,-1)
        self.y = np.array([p.pos[1] for p in self.all_p]).reshape(1,-1)
        self.s = np.array([p.status for p in self.all_p]).reshape(1,-1)

    def get_sick_coord(self):
        sick_coord_set = set()
        for p in self.all_p:
            if p.status == 1:
                sick_coord_set.add(tuple(p.pos))
        return sick_coord_set

    def random_check(self, check_size=2, random=False):
        if random:
            check_list = np.random.choice(self.all_p, check_size, replace=False)
        else:
            check_list = self.all_p[:check_size]
        for p in check_list:
            p.report_status()

    def update_allp(self, step):
        current_sick_coord = self.get_sick_coord()
        for p in self.all_p:
            if tuple(p.pos) in current_sick_coord:
                p.snb = True
            else:
                p.snb = False
            p.update_status()
        # self.random_check()
        self.to_pos_array()
        self.report_status(step)

    def run(self, steps=100):
        for p in range(steps):
            print("="*60)
            print("Now on step {}/{} ...".format(step+1, steps))
            print("="*60)
            self.update_allp()
            # self.report_status

    def plot_current(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set(xlim=(0, 100), ylim=(0, 100))
        scat = ax.scatter(self.x, self.y, c=self.s)
        plt.show()

    def report_status(self, step):
        counts = np.zeros(4)
        for p in self.all_p:
            if p.status == 0:
                counts[0] += 1
            elif p.status == 1:
                counts[1] += 1
            elif p.status == 2:
                counts[2] += 1
            else:
                counts[3] += 1
        # 11 sick , ... recovered
        print("="*60)
        print("Now on step {}/{} ...".format(step+1, self.steps))
        print("there are {} healthy people".format(counts[0]))
        print("there are {} sick people".format(counts[1]))
        self.sick_count.append(counts[1])
        if counts[1] == 0:
            self.stop = True
            print("No sick people left, program should exit now ...")
        print("there are {} recovered people".format(counts[2]))
        print("there are {} died people".format(counts[3]))
        self.dead_count.append(counts[3])
        print("="*60)

grid = Grid(100, [1800, 5, 1, 1])
# grid.run(100)
grid.show()

# grid.plot_current()
