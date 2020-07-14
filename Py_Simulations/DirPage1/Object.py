from mpl_toolkits.mplot3d import art3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

class Object:
    instances = []

    def __init__(self, universe=None, rel_size=10, mass =100,
                 init_v=None, init_p=None, name=None, total_charge = 0,
                 density=1e10, ring=False, color=None, cmap="viridis", marker=None,
                 category="all", markersize = 30, orbit = None):
        # characteristics
        self.universe = universe
        self.num_dims = self.universe.num_dims  # Used for plotting as well
        self.velocity = init_v
        self.position = init_p
        self.init_v = init_v  # Initial velocity
        self.init_p = init_p  # Initial position
        self.mass = mass
        self.ring = True if ring else None  # Make ring?
        self.velocity = init_v
        self.position = init_p
        self.name = name  # Could be used to identify object later
        self.total_charge = total_charge
        self.charge = True if total_charge>1 else False
        self.radius = markersize*5
        self.orbit = orbit

        # Plot related information
        self.color = color
        self.cmap = cmap
        self.marker = marker
        self.markersize = markersize
        self.ax = self.universe.ax  # Facilitates writting
        self.make_ring() if ring else None  # Makes rings
        self.make_plot()
        self.make_scatt()
        #self.ring should be created here as a patch.

        # Attributes used in functions
        self.net_acc = np.zeros(self.num_dims) #Starts at 0 acc
        self.other_objects = []  # Used to facilitate computations
        self.path_data = None  # Used for recordings
        self.v_data = None  # Used for recordings

        # Creates easy access to own instances
        try:
            self.__class__.__bases__.instances = []
            self.__class__.instances.append(self)
            self.universe.objects.append(self)
        except:
            self.__class__.instances.append(self)
            self.universe.objects.append(self)

    def get_facecolor_array_from_v_data(self, key):
        """Returns the list of rgba's needed to give colors to object scatter"""
        if key == "None":
            return self._facecolor
        elif key == 'vx':
            array = self.v_data[:, 0]
        elif key == 'vy':
            array = self.v_data[:, 1]
        elif key == 'vz':
            speed = np.sqrt(np.sum(self.v_data**2, axis=1))
            array = speed if self.num_dims == 2 else self.v_data[:, 2]
        elif key == "speed":
            array = np.sqrt(np.sum(self.v_data**2, axis=1))
        cc_min = np.amin(array)
        cc_max = np.amax(array)
        cc = mpl.colors.Normalize(cc_min, cc_max)
        map = mpl.cm.ScalarMappable(cc, self.cmap)
        return map.to_rgba(array)

    def update_show(self, flag):
        if not hasattr(self.universe, "page"): return
        if not hasattr(self.universe.page, "cmaps"): return
        page = self.universe.page
        self.cmap = page.cmaps[page.cmap_index]
        if hasattr(self, "scatt"):
            self.scatt.set_visible(True)
            self.plot.set_visible(False)
            self.ring.set_visible(False) if self.ring else None
            self.scatt._offsets3d = [self.path_data[:, i] for i in range(self.num_dims)]
            self.scatt._offsets = np.c_[self.path_data[:, 0], self.path_data[:, 1]]
            self.scatt._facecolor3d = self.get_facecolor_array_from_v_data(key = flag)
            self.scatt._edgecolor3d = self.scatt._facecolor3d
            self.scatt._facecolors = self.scatt._facecolor3d
            self.scatt._edgecolors  = self.scatt._facecolor3d


    def make_scatt(self):
        """
        Creates a PatchCollection object that will, later,
        carry the points with the specified velocity"""
        self.scatt = self.universe.ax.scatter(
            *self.position[:self.num_dims], s = self.markersize*20,
            c = self.color,
            cmap = "viridis",
            )
        if self.num_dims == 3:
            self.scatt._offsets3d = [[],[],[]]
        else :
            self.scatt._offsets = [[None, None]]
        self._facecolor = self.scatt._facecolor3d \
        if self.num_dims == 3 else self.scatt._facecolors



    def reset_own_scatt(self):
        """Get's plot to initial state!!!
        If you plan on modifying this code. Note how 3d has scat._facecolor3d
        scatt._edgecolor3d without the 's' in the end as in scat._facecolors"""
        if self.num_dims == 2:
            self.scatt._offsets = [self.init_p[i] for i in range(self.num_dims)]
            self.scatt.set_facecolor(self.color)
        else:
            self.scatt._offsets3d = [self.init_p[i] for i in range(self.num_dims)]
            self.scatt._edgecolor3d = self._facecolors
            self.scatt._facecolor3d = self._facecolors
        if self.ring:
            self.ring.set_visible(False)

    def update_scatt_to_current_position(self):
        """Updates scatter data points. Not to be used unless you are Pedro."""
        if self.universe.num_dims == 2:
            self.scatt._offsets = [[self.position[0], self.position[1]]]
        else:
            data = [[self.position[i]] for i in range(3)]
            self.scatt._offsets3d = data

    def update_plot_to_current_position(self):
        self.plot.set_data(*self.position[:2].reshape(2, 1))
        if self.num_dims == 3:
            self.plot.set_3d_properties([self.position[2]])
        self.update_ring_position() if self.ring else None



    def temporarily_hide_scatt(self):
        """Temporarily makes the scatter disappear"""
        if self.num_dims == 2:
            self.scatt._offsets = ([[None, None]])  # REmoves extra points
            self.scatt.set_facecolor(self.color)
        else:
            self.scatt._offsets3d = [[], [], []]
            self._facecolors = [(0,0,0,1)]


    def temporarily_hide_plot(self):
        self.plot.set_data([],[])
        self.plot.set_color(self.color)
        if self.num_dims == 3:
            self.plot.set_3d_properties([])
        if self.ring:
            self.ring.set_visible(False)


    def show_path(self):
        self.plot.set_visible(False)
        if self.ring:
            self.ring.set_visible(False)
        self.scatt.set_visible(True)
        if self.num_dims == 3:
            self.scatt._offsets3d = [self.path_data[:, i] for i in range(self.num_dims)]
        else:
            self.scatt._offsets = np.c_[[self.path_data[:, i] for i in range(self.num_dims)]]


    def get_other_objects(self):
        """Returns list with all planets that might
        be applying forces on the planet being observed"""
        index = self.universe.objects.index(self)
        lis = self.universe.objects.copy()
        lis.pop(index)
        self.other_objects = lis


    def update_velocity(self):
        self.velocity = self.velocity + self.net_acc*self.universe.dt

    def update_position(self):
        self.position = self.position+self.velocity*self.universe.dt


    def make_plot(self):
        """
        Make plot instance!!!
        """
        self.ax = self.universe.ax
        self.fig = self.universe.fig
        self.canvas = self.universe.fig.canvas
        self.plot, = self.ax.plot(
            *[[self.position[i]] for i in range(self.num_dims)],
            color = self.color,
            markersize = self.markersize,
            marker = self.marker, alpha=0.95,lw = 0,
            )
        self.canvas.draw()
        self.canvas.flush_events()


class Large_object(Object):
    """This class has better support for planetary motion"""
    instances = []

    def __init__(self, orbit_rand=False, *args, **kwargs):
        Object.__init__(self,  *args, **kwargs)
        # Orbit rand stands for random orbit
        # self.find_orbit()
        # self.check_orbit(orbit_rand)  # Ensure orbit is stabilished

    def make_ring(self):
        "Makes a ring around self of using multiple points and pyploy.scatter"
        ratio2 = self.universe.u_size/25
        self.ring = mpl.patches.Wedge(
            [0, 0], self.markersize*ratio2/4, 0, 360,
            width = self.markersize*ratio2/16, )
        self.ax.add_patch(self.ring)
        if self.num_dims == 2:
            self.ring.my_verts = self.ring.get_path()._vertices
            self.ring.get_path()._vertices*=0.6
            self.ring.get_path()._vertices+= self.position
        else:
            art3d.pathpatch_2d_to_3d(self.ring, z=0, zdir="z")
            self.ring._segment3d = np.array([np.array(x) for x in self.ring._segment3d])
            self.ring.my_verts = self.ring._segment3d
            #This is all set manually because mpl 3d is broken.
            self.update_ring_position()
        self.ring.set_color("blue")
        self.ring.set_edgecolor("white")
        self.ring.set_alpha(0.7)

    def update_ring_position(self):
        """
        mpl has not made it possible to update the position of
        a Wedge patch. Therefore, I HAVE MODIFIED IT so
        that this function would work. Doing the same in other
        computers will NOT work!"""
        if self.num_dims == 2:
            self.ring.get_path()._vertices = self.ring.my_verts+self.position
        else:
            self.ring._segment3d = self.ring.my_verts+self.position


    def calculate_net_acc(self):
        self.get_other_objects() if len(self.other_objects)==0 else None
        self.net_acc = np.zeros(self.num_dims)  # Reset forces every cycle
        if len(self.other_objects) >= 1:
            self.calc_net_charge_acc()  # Gets charge acceleration
            self.calc_new_g_acc()  # Gets g acceleration
        else:
            print("The planet is alone!")


    def calc_net_charge_acc(self):
        """Calculates the net acceleration due to coulumb interactions"""
        k = self.universe.constants["K_e"]
        if self.charge != 0 and self.charge != None:
            for object in self.other_objects:
                if object.charge != 0 and object.charge != None:
                    r = object.position - self.position
                    r_ = np.sqrt(sum(r**2))
                    unit_v = r/r_
                    if r_ > self.radius + object.radius:  # CHecks for proximity
                        charge = self.total_charge*object.total_charge*-1
                        acc = k*charge*unit_v/(sum(r**2)*self.mass)
                        self.net_acc = self.net_acc + acc

    def calc_new_g_acc(self):
        """Calculates the net acceleration due to gravitational interactions"""
        k = self.universe.constants["K_e"]
        g = self.universe.constants["G"]
        for object in self.other_objects:
            r = object.position - self.position
            r_ = np.sqrt(sum(r**2))
            unit_v = r/r_
            if r_ > self.radius + object.radius:  # CHecks for proximity
                acc = g*object.mass*unit_v/sum(r**2)
                self.net_acc = self.net_acc + acc

    def find_orbit(self):
        if not self.orbit: return
        for object in self.universe.objects:
            if object.name == self.orbit:
                self.orbit = object
                print("ORBIT WAS DETECTED")
                break

    def check_orbit(self, orbit_rand):
        # flexibility with inputs
        if type(self.orbit) == str: return
        flex = {}
        possible_yes = "random different yes true".split()
        possible_no = "same equal no not false".split()
        for yes in possible_yes:  # Will allow for multiple rand_orbit responses
            flex[yes] = True
        for no in possible_no:
            flex[no] = False
        limit = self.universe.u_size*2 if self.num_dims == 3 else self.universe.u_size  # Universe limits
        g = self.universe.constants["G"]  # Gets constant
        zeroes = np.zeros(self.num_dims)  # Used to control number of dimensions
        if self.orbit:
            r = self.orbit.init_p - self.init_p  # distance vector
            r_ = np.sqrt(sum(r**2))
            if r_ < (self.radius+self.orbit.radius)/2 or r_ == 0 or r_ == 0.:  # Checks for Large objects on same point
                self.init_p = np.zeros(self.num_dims)  # Sets position that eases calculations
                min = limit/5
                r_ = np.random.randint(min, limit)  # New distance
            v_ideal = np.sqrt(g*self.orbit.mass/r_)
            self.init_v = np.zeros(self.num_dims)
            self.init_p = np.zeros(self.num_dims)
            self.init_v[0] = v_ideal
            self.init_p[0] = r_  # Assigns random distance to close objects along x axis
            orbit_rand = "true" if orbit_rand == True else "False" if orbit_rand == False else orbit_rand
            if not flex[orbit_rand.lower()]:  # The input may be weird
                if self.num_dims == 2:
                    self.init_p = self.init_p[::-1]  # Ensures perp velocity
                elif self.num_dims == 3:
                    self.init_p[0] = 0
                    self.init_p[1] = r_
            else:
                if self.num_dims == 3:
                    v = self.init_v[self.init_v != 0][0]/np.sqrt(2)  # More components
                    self.init_v[0] = v
                    self.init_v[1] = v
                    while np.where(self.init_p != 0)[0][0] not in np.where(self.init_v == 0)[0]:
                        for x in range(self.num_dims):
                            self.init_v[x] = self.init_v[x]*np.random.choice([-1, 1])  # Changes direction
                            self.init_p[x] = self.init_p[x]*np.random.choice([-1, 1])  # Changes direction
                        np.random.shuffle(self.init_p)
                        np.random.shuffle(self.init_v)
                else:
                    self.init_v[0] = v_ideal
                    self.init_p = self.init_p[::-1]  # Ensures perp velocity
            self.init_v = self.init_v + self.orbit.init_v
            self.init_p = self.init_p + self.orbit.init_p
            self.velocity = self.init_v.copy()
            self.position = self.init_p.copy()
        self.update_plot_to_current_position()
        print(self.position, self.velocity, f"are the init_v and p of {self.name}")
        self.universe.fig.canvas.draw()
        self.universe.fig.canvas.flush_events()
