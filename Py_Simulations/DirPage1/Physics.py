"""
    This is the first class to be created. It will contain the main figure and axes.
    It should also contain a function to make all the buttons necessary. It should
    contain a list with all the important objects inside it."""

import mpl_toolkits.mplot3d.axes3d as p3
from mpl_toolkits.mplot3d import art3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import itertools

class Physics:
    """Back-bone of the simulation. Contains the main figure and axes"""
    instances = []  # You never know when you will neeed to acces Physics instances

    def __init__(self, u_size=1000, num_dims=2, stars=True, dt=0.01,
                 show_time=False, name="Predru\'s world", recording=False, t=0,
                 blit = False, page = None, *args, **kwargs):

        #First we deal with the GUI
        #This is the  tkinter frame where it's canvas will be
        self.page = page

        # Follow Universe characteristics
        self.u_size = u_size  # If universe is a cube, u_size = side length
        self.num_dims = num_dims  # Number of dimensions (2-3)
        self.stars = stars  # If the plot has stars
        self.t = t  # s
        self.dt = dt  # s
        self.constants = {"G": 6.67408*1e-11, "K_e": 8.9875517923*1e9}  # Constants in STI
        self.show_time = show_time #Flag for plot
        self.name = name  # Title of the figure
        self.objects = []  # List of objects in Physics instance

        # Follow elements about recording
        self.recording = recording  # True for recorded Simulation

        # Follow elements that concerns plotting and stars
        self.make_plot()  # makes the plot
        self.make_stars(stars)  # Makes stars for a prettier background
        # self.canvas, self.ax and self.fig are defined in self.make_plot()
        # self.stars1, self.stars2, self.stars3 are defined in self.make_stars()
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.blit = blit #Used for 3d draws. But it has a cost.

        # More stuff on organization
        self.__class__.instances.append(self)  # Adds self to instances

        # Things that functions depend on
        self.running = False  # will be set to true while simulation runs

        # Things for testing later
        self.object_pairs = []  # Will help with efficiency

    def find_pairs(self):
        "So that planets won't have to search for each other all the time"
        stuff = self.objects
        self.object_pairs = []
        for subset in itertools.combinations(stuff, 2):
            self.object_pairs.append(subset)


    def make_stars(self, stars):
        "Adds stars to Physics instance.ax"
        size = self.u_size, -1*self.u_size  # These values were randomly chosen
        data = [np.random.randint(low=size[1]*2,
                                  high=size[0]*2, size=35) for x in range(3)]
        x, y, z = [data[i] for i in range(3)]
        data2 = [np.random.randint(low=size[1]*2,
                                  high=size[0]*2, size=10) for i in range(3)]
        x2, y2, z2 = [data2[i] for i in range(3)]
        data3 = [np.random.randint(low=size[1]*2,
                                  high=size[0]*2, size=10) for i in range(3)]
        x3, y3, z3 = [data3[i] for i in range(3)]
        if self.num_dims == 3:
            self.stars1, = self.ax.plot(x, y, z, lw = 0, color = "white",
                                markersize = 2, alpha=0.8, marker= "*")
            self.stars2, = self.ax.plot(x2, y2, z2, lw = 0, color = "green",
                                markersize = 1, alpha=0.8, marker= "*")
            self.stars3, = self.ax.plot(x3, y3, z3, lw = 0, color = "blue",
                                markersize = 1, alpha=0.8, marker= "*")

        else:
            self.stars1, = self.ax.plot(x, y, lw = 0, color = "white",
                                markersize = 2, alpha=0.8, marker= "*")
            self.stars2, = self.ax.plot(x2, y2, lw = 0, color = "green",
                                markersize = 1, alpha=0.8, marker= "*")
            self.stars3, = self.ax.plot(x3, y3, lw = 0, color = "blue",
                                markersize = 0.5, alpha=0.8, marker= "*")
        if not stars:
            self.stars1.set_visible(False)
            self.stars2.set_visible(False)
            self.stars3.set_visible(False)
        self.canvas.draw()
        self.canvas.flush_events()

    def make_plot(self):
        """Makes the visuals"""
        mpl.style.use("fast")#For faster rendering
        self.fig = plt.figure(figsize = (5, 4))
        if self.page!=None:
            self.canvas = mpl.backends.backend_tkagg.FigureCanvasTkAgg(
                self.fig, self.page.canvas_area)
            self.canvas.get_tk_widget().pack()
        else:
            self.canvas = self.fig.canvas
        lims = lims = -1*self.u_size, self.u_size  # Dimensions of axes
        # Checks number of dimensions of axes
        if self.num_dims == 2:  # 2dimensions
            self.ax = self.fig.add_subplot(111)
            self.fig.set_facecolor("black")
            self.ax.set(fc='black', xlim=lims, ylim=lims)
            self.text = self.ax.text(.1, 0.1, "", color="white",
                                     transform=self.ax.transAxes)  # Place where time will show
            #What follows is because 2D titles need special treatment
            self.ax.text(.5,.9, self.name, horizontalalignment='center',
                transform=self.ax.transAxes, fontdict={'fontname': "monospace",
                                                        "color": "white"})
        elif self.num_dims == 3:  # 3 dimensions
            self.ax = p3.Axes3D(self.fig)
            self.ax.set(xlim=lims, ylim=lims, zlim=lims, fc = "black")
            self.text = self.ax.text2D(.1, 0.1, "", color="white",
                                       transform=self.ax.transAxes)
            self.ax.view_init(21, 79)  # Nice angle for visuals
        else:
            # In case too many dimensions are used.
            print('Number of dimensions not supported for visualization')

        self.ax.axis("off")#To make all ticks and lines disappear
        self.ax.set_position([0, 0, 1, 1])
        # Color c of text depends on whether you are recording or not
        # This is because recording changes fig color
        c = "black" if self.num_dims == 2 and self.recording else "white"
        title = self.name if self.name else "Predru\'s world"
        self.ax.set_title(title, color=c, fontdict={'fontname': "monospace"})


    def new_collect_data(self):
        """Collects n cycles of planetary movement. n is taken from a slider.
        This information is stored as object.path_data and object.v_data
        for positions and velocities respectively"""
        if not hasattr(self, "data_collected"):
            self.data_collected = False
        self.running = False
        if self.data_collected: return
        shape = (1, self.num_dims)  # Shape of the multidimentional array
        if self.page!=None:
            self.page.update_cycles(self.page.nc_slider.get())
            number_cycles = self.page.cycles
        else:
            if hasattr(self, "number_cycles"):
                number_cycles = self.number_cycles
            else:
                number_cycles = 100
        print(number_cycles, "Cycles collected")  # Info about number of cycles
        self.replay()  # Restats recording
        for object in self.objects:
            setattr(object, "path_data", np.array([[object.position[x] for
                                                    x in range(self.num_dims)]]))  # Restarts calculations
            setattr(object, "v_data", np.array([[object.velocity[x] for x
                                                 in range(self.num_dims)]]))  # speed data

        for x in range(number_cycles):  # number of cycles that are considered in the calculations
            for object in self.objects:  # Updates velocities of all planets
                object.calculate_net_acc()
                object.update_velocity()

            for object in self.objects:  # Applies change in location after dt seconds
                object.update_position()
                object.path_data = np.concatenate((object.path_data,
                                                   object.position.reshape(shape)))
                object.v_data = np.concatenate((object.v_data,
                                                object.velocity.reshape(shape)))
        self.data_collected = True

    def replay(self):
        """Gets objects to initial state"""
        for object in self.objects:
            object.velocity = object.init_v
            object.position = object.init_p
        self.t = 0
        self.play() if self.running else None

    def play(self):
        self.running = True  # Set running status
        for object in self.objects:
            object.temporarily_hide_scatt()
            object.plot.set_visible(True)
            object.ring.set_visible(True) if object.ring else None
        rings = False
        for object in self.objects:
            rings = True if object.ring else rings
        try:
            while self.running:  # Pressing a button will disrupt the play. But not throw errors.
                for i in np.arange(3):
                    for object in self.objects:  # update all the velocities
                        object.calculate_net_acc()
                        object.update_velocity()
                    for object in self.objects:  # updates all the positions
                        object.update_position()
                    self.t = self.t + self.dt
                for object in self.objects:  # update all the velocities
                    object.calculate_net_acc()
                    object.update_velocity()
                for object in self.objects:  # updates all the positions
                    object.update_position()
                    object.update_plot_to_current_position()
                self.t = self.t + self.dt
                self.text.set_text(f"{round(self.t, 1)} seconds") if\
                    self.show_time else None
                self.canvas.draw()
                self.canvas.flush_events()
        except :
            print("PROBLEM WITH RUN!")

    def show_comp(self):
        if hasattr(self, "page"):
            if not self.running:
                for object in self.objects:
                    if hasattr(object, "scatt"):
                        object.update_show(
                            self.page.show_comp.get()
                        )

    @classmethod
    def twod(cls):
        print("still has to work on it.")

    @classmethod
    def threed(cls, page):

        print("still has to work on it.")
        page.delete_canvas()
        objs = [
            ['Sun_1', 'yellow', 15, 'False', '0.0', '[0, 0, 0]', '[0, 0, 0]', '1e+16', 'o', 'None...Yet'],
            ['Planet_7', 'pink', 9, 'True', '0.0', '[0, 0, 0]', '[0.0, 1200.0, 0.0]', '1000000000000.0', 'o', 'Sun_1'],
            ['Planet_9', 'purple', 10, 'True', '0.0', '[0, 0, 0]', '[0.0, 1500.0, 0.0]', '1000000000000.0', 'o', 'Sun_1'],
            ['Planet_12', 'green', 7, 'True', '0.0', '[0, 0, 0]', '[0.0, 2400.0, 0.0]', '1000000000000.0', 'o', 'Sun_1'],
            ['Planet_13', 'red', 7, 'True', '0.0', '[0, 0, 0]', '[0.0, 2100.0, 0.0]', '1000000000000.0', 'o', 'Sun_1'],
            ['Planet_14', 'cyan', 8, 'False', '0.0', '[0, 0, 0]', '[0.0, 850.0, 0.0]', '1000000000000.0', 'o', 'Sun_1'],
            ['Moon_15', 'white', 4, 'False', '0.0', '[0, 0, 0]', '[0.0, 550.0, 0.0]', '10000000000.0', 'o', 'Sun_1'],
            ['Moon_16', 'white', 4, 'False', '0.0', '[0, 0, 0]', '[0.0, 1050.0, 0.0]', '10000000000.0', 'o', 'Sun_1'],
            ['Moon_17', 'white', 4, 'False', '0.0', '[0, 0, 0]', '[0.0, 1350.0, 0.0]', '10000000000.0', 'o', 'Sun_1'],
            ['Moon_18', 'white', 4, 'False', '0.0', '[0, 0, 0]', '[0.0, 1800.0, 0.0]', '10000000000.0', 'o', 'Sun_1'],
            ]
        page_ = page.__class__.instances['page1_1']
        page_.box_interactive.set(False),
        page_.change_page("page1_2")(),#Note the ()!!! Change page is a wraper!
        page_.master.geometry("600x500"),

        for obj in objs:
            page_.tree.insert("", "end", text = f"{obj[-1]}".strip(), values = obj)
        page.draw_simulation()
        page_.tree.delete(*page_.tree.get_children())
