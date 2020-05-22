"""
    Physics class + other imports
    """
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3


class Physics:
    """Class that controls physical laws and visualization

    Atributes
    ---------
        create an instance called "instance"
        run: print(instance.__dict__)

    Output
    ------
        A physics instance. Analogous to a "universe".
        Planet objects take "universes" as arguments.
        The properties of this "universe" determine how
        Planet instances will interact.
        """
    instances = []

    def __init__(self, origin=None, u_size=150, t=0, dt=0.1,
                 num_dims=2, show_time=False, stars=False, category="universe"):
        """
        Parameters
        ----------
            origin: np.array, optional
                Origin of the Physics instance
                (default  = 0)

            u_size: int, float
                Side length of Physics instance if imagined as a cube
                (default  = 150)

            t: int, float
                Current time
                (default  = 0)

            dt: int, float
                Time step taken when evaluating changes in instances
                (default  = 0.1)

            num_dims: int
                Number of physical dimensions in the system (2 or 3)
                (default  = 2)

            show_time: bool
                Show time in plot? (default  = False)

            stars: bool
                Show stars in plot? (default  = False)

            category: str
                Changes the name of the plot
                {"universe": "x world", "subatomic": "x particles",
                other: "x creation"}. x = "Predru's """
        self.origin = origin if origin else np.array([0 for x in range(num_dims)])  # (m, m)
        self.u_size = [(-u_size, u_size) for dimension in range(num_dims)]  # m This is the lengths of -+ xyz axes
        self.num_dims = num_dims
        self.t = t  # s
        self.dt = dt  # s
        self.G_cons = 6.674*1e-11  # m3 kg-1 s-2
        self.C_cons = 8.9875517923*1e9  # kg m3 s-4 A-2
        self.show_time = show_time
        self.category = category  # {universe: world, subatomic: particles}
        self.make_plot()  # This takes care of the visuals
        self.make_stars() if stars else None  # makes stars
        self.objects = []  # used for optimization
        self.__class__.instances.append(self)

    def make_plot(self):
        """Makes the visuals"""
        self.fig = plt.figure()
        if self.num_dims == 2:
            self.ax = self.fig.add_subplot(111)
            self.ax.set(fc='black', xlim=self.u_size[0], ylim=self.u_size[1])
            self.text = self.ax.text(.1, 0.1, "", color="white", transform=self.ax.transAxes)
        elif self.num_dims == 3:
            self.ax = p3.Axes3D(self.fig)
            self.ax.set(fc='black', xlim=self.u_size[0],
                        ylim=self.u_size[1], zlim=self.u_size[2])
            self.ax.grid(False)
            self.ax.set_facecolor('black')
            self.ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.text = self.ax.text2D(.1, 0.1, "", color="white", transform=self.ax.transAxes)
            self.ax.view_init(21, 79)
        else:
            print('Number of dimensions not supported for visualization')
        self.fig.set_facecolor("black")
        c = "black" if self.num_dims == 2 else "white"
        text_setter = 'Predrus\'s world' if self.category.lower() == "universe" else \
            'Predrus\'s particles' if self.category.lower() == "subatomic" else "Predrus\'s creation"
        self.ax.set_title(text_setter, color=c, fontdict={'fontname': "monospace"})
        self.make_buttons()

    def g_force(self, object_self, object_other):
        """
        Parameters
        ----------
            object_self = object with mass and position.
            object_other = object with mass and position.
        Output
        ------
            The net gravitational pull of object_other on object_self
            as a vecor/np.ndarray.
        """
        os, oo = object_self, object_other
        r = oo.position - os.position
        IrI = np.sqrt(sum(r**2))
        if os.shape == "sphere" and oo.shape == "sphere":
            if IrI <= os.dimensions+oo.dimensions:
                return r*0
            elif IrI <= os.dimensions:
                return r*0
        a = self.G_cons*oo.mass*r/IrI**3
        forces = a*os.mass
        return forces

    def m_force(self, object_self, object_other):
        """
        Parameters
        ----------
            object_self = object with charge and position.
            object_other = object with charge and position.
        Output
        ------
            The net electric pull of object_other on object_self
            as a vecor/np.ndarray."""
        if object_self.charge == None or object_other.charge == None:
            return self.origin * 0

        elif (object_other.charge == 1 or object_other.charge == -1) and \
                (object_self.charge == 1 or object_self.charge == -1):

            r = object_other.position - object_self.position
            IrI = np.sqrt(sum(r**2))

            prdct_of_charges = object_other.total_charge*object_self.total_charge
            forces = self.C_cons*prdct_of_charges*r/IrI**3
            forces = forces*-1  # nEnsures the direction of the force comes out right
            return forces
        else:
            print("You made a mistake somewhere")
            return self.origin * 0

    def update_velocity(self, object, forces):
        """
        Parameters
        ----------
            object = object with mass and position.
            forces = vector/ndarray with net forces on object.
        Sets
        ----
            object.velocity = forces/object.mass*dt + object.velocity

        Output
        ------
            New object's velocity as a vector/ndarray.
            """
        dt = self.dt
        dps = forces*dt  # Changes in momentum
        dvs = dps/object.mass  # Changes in speed
        vs = object.velocity + dvs  # Final velocity
        return vs

    def update_2d_axes(self):
        """Updates the plot after planetary movement"""
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def make_buttons(self):
        """Creates buttons that help with the interaction"""
        self.button_axes = []
        self.fig2 = plt.figure(figsize=(3, 2))
        ax1 = self.fig2.add_axes([0.1, 0.6, 0.4, 0.3], label="ax1")
        ax2 = self.fig2.add_axes([0.5, 0.6, 0.4, 0.3], label="ax2")
        ax3 = self.fig2.add_axes([0.5, 0.3, 0.4, 0.3], label="ax3")
        ax4 = self.fig2.add_axes([0.1, 0.3, 0.4, 0.3], label="ax4")
        ax5 = self.fig2.add_axes([0.15, 0.1, 0.7, 0.1], label="ax5")
        for ax in (ax1, ax2, ax3, ax4, ax5):
            ax.get_yaxis().set_visible(False)
            ax.get_xaxis().set_visible(False)
            self.button_axes.append(ax)
        button = mpl.widgets.Button(self.button_axes[0], label='Play')
        button.on_clicked(self.play)
        self.play_button = button  # To keep the button existing!

        button = mpl.widgets.Button(self.button_axes[1], label='Re-Play')
        button.on_clicked(self.replay)
        self.replay_button = button

        slider = mpl.widgets.Slider(self.button_axes[4], label='dt',
                                    valmin=0.01, valmax=2.0, valstep=0.01,
                                    valinit=self.dt)
        slider.on_changed(self.update_dt)
        self.slider = slider

        button = mpl.widgets.Button(ax3, "Exit")
        button.on_clicked(self.close)
        self.close_button = button

    def close(self, press):
        "Closes the plots"
        plt.close("all")

    def replay(self, click):
        """Returns all Planet instances in the plot to their starting position and velocity"""
        for object in self.objects:
            object.position = object.initial_position
            object.velocity = object.initial_v
            # The map does not update correctly for some reason
            self.t = 0

    def update_dt(self, val):
        self.dt = val

    def evolve_system(self):
        """Checks for all the physical changes that occur to all the Planet instances
            under self dictating physical properties and updates the plot afterwards"""
        for object in self.objects:  # Updates velocities of all planets
            object.update_velocity()
        for object in self.objects:  # Applies change in location after dt seconds
            object.position = object.position + object.velocity*self.dt
            object.update_ring_location() if 'update_ring_location' in dir(object) else None
            object.data = np.c_[object.position[0], object.position[1]]
            if self.num_dims == 2:
                object.scatt.set_offsets(object.data)
            else:
                object.data = ([[object.position[i]] for i in range(3)])
                object.scatt._offsets3d = tuple(object.data)
        self.t += self.dt
        if self.dt >= 0.1:
            self.text.set_text(f"{round(self.t, 2)} seconds") if self.show_time else None
        else:
            self.text.set_text(f"{round(self.t, 1)} seconds") if self.show_time else None
        # Here the 3d stuff will come

    def play(self, button_press):
        """Plays 2000 dt evolve_system() cycles"""
        while True:
            try:
                self.evolve_system()
                if self.num_dims == 2:
                    self.update_2d_axes()
                else:
                    self.update_3d_axes()
            except:
                break
        print("Simulation is over")

    def update_3d_axes(self):
        self.update_2d_axes()

    def record(self, frame):
        """Function goes inside FuncAnimation when making animation"""
        self.evolve_system()
        print(frame)
        return [pl.scatt for pl in self.objects]

    def record_gif(self, name_gif='gravity_3d.gif', frames=100, fps=40, repeat=False):
        """
        Parameters
        ----------
            name_gif: str -> Name of the gif you wish to save
                (default = "gravity_3d.gif")
            frames: int -> length of gif in frames
                (default = 100)
            fps: int -> Frames per second
                (default = 40)
            repeat: bool
                No idea what it does. (default = False)
        Output
        ------
            gif named "name_gif" is created in current directory
            """
        ani = FuncAnimation(self.fig, self.record, repeat=repeat,
                            frames=frames, blit=True, interval=1)
        writergif = mpl.animation.PillowWriter(fps=fps)
        ani.save(name_gif, writer=writergif)
        print("Completed!")

    def make_stars(self):
        "Adds stars to Physics instance.ax"
        data = [np.random.randint(low=self.u_size[0][0]*2,
                                  high=self.u_size[0][1]*2, size=45) for x in range(3)]
        x, y, z = [data[i] for i in range(3)]
        s = np.random.randint(1, 10, 45)
        if self.num_dims == 3:
            self.stars = self.ax.scatter3D(x, y, z, c='white', alpha=0.8, marker="*", s=s)
        else:
            self.stars = self.ax.scatter(x, y, c='white', alpha=0.8, marker="*", s=s)

    def make_n_planets(self, number, clas, rings=False, charge=False):
        """Creates number instances of clas. (Designed for Planet).
        Parameters
        ----------
            number: int
            clas: class (current app supports only Planet)
            rings: Gets
            passed to Planet. Giving it a chance of 30% of getting a ring.
            Charge: Gets passed to Planet. Giving it a chance of 30% of getting a charge.
        """
        for x in range(number):
            f = clas.random__init__(self, rings=rings, charge=charge)

    def make_n_moons(self, number, clas, planet_list):  # Still have to work on it.
        pass


class Large_things:
    instances = []
    """ Creates a particle
    instances = []  # List of instances
    """

    def __init__(self, shape="sphere", radius=1, density=10,
                 initial_position=None, initial_v=None, charge=None,
                 universe=None, ring=False, charge_density=1, category="planet"):
        """
        Parameters
        ----------
            universe: Physics object -> Determines physical properties
                (default = Physics())

            shape: str -> Does not do much yet.
                (default = "sphere")

            charge: int == +-1 -> Gives + or - charge type to object.
                (default = None)

            charge_density: int, float -> Units: C m-3
                (default = 1)

            dimensions: int, float -> Radius -> Units: m
                (default = 1)

            density: int, float -> Mass density -> Units: kg/m3
                (default = 1)

            initial_v: np.ndarray, list, tupple -> Initial velocity of the object as a vector
                [x, y] or [x, y, z] for 2, 3 dimensions respectively.
                (default = np.array([0, 0]) or np.array([0, 0, 0]))

            initial_position: np.ndarray, list, tupple -> Initial position of object given as vector
                [x, y] or [x, y, z] for 2, 3 dimensions.
                (default = np.array([0, 0]) or np.array([0, 0, 0]))

            ring: bool -> If the planet has a ring.
                (default = False)

            category: str -> What king of object it is(e.g. Planet, Star...)
                (default = "planet")
            """
        self.universe = universe
        self.shape = shape
        self.charge = charge  # NUMBER 0=-, 1=+
        self.dimensions = radius   # m3
        self.volume = 4/3*3.14*self.dimensions**3
        self.density = density  # kg m-3
        self.category = category
        self.mass = density * self.volume  # kg
        self.charge_density = charge_density  # Cm-3
        self.attribute_charge(charge)
        self.set_position_velocity(initial_position, initial_v)
        self.make_ring() if ring else None
        self.create_plot()  # ads self to plot
        self.__class__.instances.append(self)  # adds self to list of Large_things instances
        universe.objects.append(self)  # ads self to universe objects
        try:
            self.__class__.__bases__.instances.append(self)
        except:
            None

    def change_self_size(self, ratio_new_to_old):
        """Change the size of a single instnce on the plot"""
        size = self.scatt.get_sizes()*ratio_new_to_old
        self.scatt.set_sizes(size)

    def create_plot(self):
        plot = self.universe.fig, self.universe.ax
        c = "yellow" if self.category == "sun" else "white" if self.category == "moon"\
            else None
        marker = None  # "$♥$"
        area = self.dimensions
        if self.universe.num_dims == 2:
            self.scatt = plot[1].scatter(self.position[0], self.position[1],
                                         s=area, c=c, marker=marker)
        else:
            datas = self.position[0], self.position[1], self.position[2]
            self.scatt = plot[1].scatter(datas[0], datas[1], datas[2],
                                         s=area, alpha=0.95, c=c, marker=marker)

    def set_position_velocity(self, initial_position, initial_v):
        if type(initial_position) == tuple or type(initial_position) == list:
            initial_position = np.array(initial_position)
        elif type(initial_position) == np.ndarray:
            initial_position = initial_position
        else:
            initial_position = self.universe.origin
        if type(initial_v) == tuple or type(initial_v) == list:
            initial_v = np.array(initial_v)
        elif type(initial_v) == np.ndarray:
            initial_v = initial_v
        else:
            initial_v = self.universe.origin
        self.velocity = initial_v
        self.initial_v = initial_v
        self.initial_position = initial_position
        self.position = initial_position

    def attribute_charge(self, charge):  # to make init shorter
        if charge:
            self.charge = charge
            self.total_charge = charge*self.charge_density\
                * 4/3*3.14*self.dimensions**3
        else:
            self.total_charge = None

    def make_ring(self):
        "Makes a ring around self of using multiple points and pyploy.scatter"
        r = self.dimensions*6
        r = r/1.6 if self.universe.num_dims == 2 else r
        self.t_ring = t = np.arange(0, np.pi * 2.0, 0.01)
        self.x_ring = r * np.cos(t)
        self.y_ring = r * np.sin(t)
        y = r * np.sin(t)
        x = r * np.cos(t)
        x = x + self.position[0]
        y = y + self.position[1]
        if self.universe.num_dims == 2:
            self.ring_location = np.array([self.x_ring, self.y_ring])
            self.ring = self.universe.ax.scatter(x, y, s=r/40)
        else:
            self.z_ring = z = np.zeros(len(x))
            z = z + self.position[2]
            self.ring = self.universe.ax.scatter(x, y, z, s=r/40)
            self.ring_location = np.array([self.x_ring, self.y_ring, self.z_ring])

    def update_ring_location(self):
        if hasattr(self, 'x_ring'):
            if self.universe.num_dims == 2:
                data = data = self.x_ring + self.position[0], self.y_ring + self.position[1]
                data = np.c_[data[0], data[1]]
                self.ring.set_offsets(data)
            else:
                data = self.x_ring + self.position[0], self.y_ring + self.position[1], \
                    self.z_ring + self.position[2]
                data = [data[i] for i in range(3)]
                self.ring._offsets3d = tuple(data)

    def find_g_forces(self):
        """Uses function of physics instance to obtain net force on self
        outputs this net force as a ndarray."""
        planetsF = self.get_other_objects()  # Forces of other planets on itself.
        forces = np.array([0 for x in range(self.universe.num_dims)])
        for planet in planetsF:  # Finds the overal forces when all planets are considered.
            relative_coord = planet.position - self.position
            forces = forces + self.universe.g_force(self, planet)
        return forces

    def find_charge_forces(self):
        """finds all the gravitational forces of other planets on itself
        these will get returned as a numpy array """
        other_things = self.get_other_objects()
        forces = np.array([0 for x in range(self.universe.num_dims)])
        for thing in other_things:
            dist = thing.position - self.position
            forces = forces + self.universe.m_force(self, thing)
        return forces

    def get_other_objects(self):
        """Returns list with all planets that might
        be applying forces on the planet being observed"""
        index = self.universe.objects.index(self)
        lis = self.universe.objects.copy()
        lis.pop(index)
        return lis

    def update_velocity(self):
        """Updates the velocities of a planet"""
        p = print
        forces = self.find_g_forces() + self.find_charge_forces()
        v_new = self.universe.update_velocity(self, forces=forces)
        self.velocity = v_new
        self.check_boundery()

    def check_boundery(self):
        """Reflects particle's getting out of universe's "volume" """
        for index, value in enumerate(self.position):
            if abs(value) >= self.universe.u_size[0][1]*4:
                self.velocity[index] = -self.velocity[index]

    @staticmethod  # This function shall be revised
    def random__init__(universe, rings=False, charge=None, cls=None):
        """Creates randomized planet on using universe as template for physics
        Outputs a Planet instance"""
        generate = np.random.uniform
        max = universe.u_size[0][1]*0.7
        zi = universe.num_dims
        r, d, ip, i_v = generate(1, 5), generate(1, 1e10), \
            generate(-max, max, size=zi), generate(-15, 15, zi)
        ans = np.random.randint(0, 10) if rings else False
        charge = np.random.choice([-1, 1]) if charge else None
        if ans and ans >= 7:
            ans = True
        else:
            ans = False
        return cls(radius=r, density=d, initial_position=ip, universe=universe, initial_v=i_v,
                   ring=ans, charge=charge)

    def set_orbit(self, sun):
        """sets planet's orbit around it's sun!
        This is done by changing their initial position and velocity"""
        d = self.position - sun.position
        d = np.sqrt(sum(d**2))
        g = self.universe.G_cons
        v_ideal = np.sqrt(g*sun.mass / d)
        if self.universe.num_dims == 3:
            self.position = np.array([0, d, 0])
            self.velocity = np.array([v_ideal, 0, 0])
        else:
            self.position = np.array([0, d])
            self.velocity = np.array([v_ideal, 0])
        self.initial_position = self.position.copy()
        self.initial_v = self.velocity.copy()
        self.universe.update_2d_axes() if self.universe.num_dims == 2 else \
            self.universe.update_3d_axes()

    def make_all_planets_orbit(self, both_axes=False):
        """Makes "self" the sun
        both axes refers to a more adventurous orbital style"""
        i = 1
        for planet in self.get_other_objects():
            planet.set_orbit(self)
            if self.universe.num_dims == 3 and both_axes:
                if i % 2 == 0:
                    planet.velocity = planet.velocity[::-1]
                    planet.position = planet.position[::-1]

                    if i % 4 == 0 and self.universe.num_dims == 3:
                        v = planet.velocity[planet.velocity != 0][0]/np.sqrt(2)
                        planet.velocity = np.array([v, 0, v])

                elif i % 3 == 0:
                    v = planet.velocity[planet.velocity != 0][0]/np.sqrt(2)
                    planet.velocity = np.array([-1*v, 0, v])
            if np.random.randint(0, 10) % 2 == 0 and both_axes:
                planet.velocity = planet.velocity*-1
            planet.initial_v = planet.velocity.copy()
            planet.initial_position = planet.position.copy()
            i = i+1 if both_axes else both_axes

    def update_plot(self):
        """Used to update plot upon creation of instance"""
        self.data = np.c_[self.position[0], self.position[1]]
        if self.universe.num_dims == 2:
            self.scatt.set_offsets(self.data)
        else:
            self.data = ([[self.position[i]] for i in range(3)])
            self.scatt._offsets3d = tuple(self.data)
        self.universe.update_2d_axes()


class Planet(Large_things):  # adapt class to work with Physics
    instances = []

    def __init__(self, category="planet", *args, **kwargs):
        super().__init__(category=category, *args, **kwargs)


class Sun(Large_things):
    instances = []

    def __init__(self, category="sun", *args, **kwargs):
        super().__init__(category=category, *args, **kwargs)


class Moon(Large_things):
    """Creates an object orbiting another object"""
    instances = []

    def __init__(self, orbit=None, rad_orb=10, resize=False, category="moon",
                 **kwargs):
        if orbit:
            kwargs["universe"] = orbit.universe
            super().__init__(category=category, **kwargs)
            self.rad_orb = rad_orb
            self.set_orbit(orbit)  # orbits orbit
            self.orbit = orbit
            self.adjust_sizes(orbit, resize)
            self.update_plot()
            print("moon was created")
        else:
            print("This object will not behave as a moon.")

    def print_v(self):
        v = np.sqrt(sum(self.velocity**2))
        print(v)

    def adjust_sizes(self, orbit, resize):
        if resize:
            self.universe.already_resized = True if \
                hasattr(self.universe, "already_resized") else False
            if not self.universe.already_resized:
                for planet in orbit.__class__.__bases__[0].instances:
                    size = planet.scatt.get_sizes()
                    size = size/orbit.dimensions**2 if planet.__class__ == \
                        orbit.__class__ or planet.__class__.__bases__[0] == \
                        planet.__class__.__bases__[0] else size/2
                    planet.scatt.set_sizes(size)

    def set_orbit(self, orbit):
        """sets planet's orbit around it's planet!
        This is done by changing their initial position and velocity.
        But it keelps the distance from the planet."""
        d = self.rad_orb
        g = self.universe.G_cons
        v_ideal = np.sqrt(g*orbit.mass/d)
        if self.universe.num_dims == 3:
            self.position = np.array([0, d, 0]) + orbit.position
            self.velocity = np.array([v_ideal, 0, 0]) + orbit.velocity
        else:
            self.position = np.array([0, d]) + orbit.position
            self.velocity = -1*np.array([v_ideal, 0]) + orbit.velocity
        self.initial_position = self.position.copy()
        self.initial_v = self.velocity.copy()

#Running the simulation to get a feel for it
if __name__ == "__main__":
    universe = Physics(show_time=True, dt=0.01, num_dims=2, u_size=2000, stars=True)
    sun = Sun(universe=universe, density=1e15, radius=40, initial_position=(0, 0))
    sun.change_self_size(5)
    for x in range(10):
        x = Planet.random__init__(universe=universe, cls=Planet)
    sun.make_all_planets_orbit(both_axes=False)
    for planet in Planet.instances:
        moon = Moon(orbit=planet, radius=2, density=1e10, rad_orb=30)
    earth = Planet(radius=10, universe=universe, density=1e12, initial_position=(0, 1500))
    earth.set_orbit(sun)
    moon = Moon(orbit=earth, radius=1, density=1e10, rad_orb=20)
    plt.show()
