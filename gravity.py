"""
    gravity.py in 3d
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

    def __init__(self, origin=None, universe_dimensions=150, t=0, dt=0.1,
                 num_dims=2, t_b=False, stars=False, category="universe"):
        """
        Parameters
        ----------
            origin: np.array, optional
                Origin of the Physics instance
                (default  = 0)

            universe_dimensions: int, float
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

            t_b: bool
                Show time in plot? (default  = False)

            stars: bool
                Show stars in plot? (default  = False)

            category: str
                Changes the name of the plot
                {"universe": "x world", "subatomic": "x particles",
                other: "x creation"}. x = "Predru's """
        self.origin = origin if origin else np.array([0 for x in range(num_dims)])  # (m, m)
        self.universe_dimensions = [(-universe_dimensions, universe_dimensions)
                                    for dimension in range(num_dims)]  # m This is the lengths of -+ xyz axes
        self.num_dims = num_dims
        self.t = t  # s
        self.dt = dt  # s
        self.G_cons = 6.674*1e-11  # m3 kg-1 s-2
        self.C_cons = 8.9875517923*1e9  # kg m3 s-4 A-2
        self.t_b = t_b
        if num_dims == 2:
            self.fig, self.ax = plt.subplots()
            self.ax.set(fc='black', xlim=self.universe_dimensions[0], ylim=self.universe_dimensions[1])
            self.text = self.ax.text(.1, 0.1, "", color="white", transform=self.ax.transAxes)
        else:
            self.fig = plt.figure()
            self.ax = p3.Axes3D(self.fig)
            self.ax.set(fc='black', xlim=self.universe_dimensions[0],
                        ylim=self.universe_dimensions[1], zlim=self.universe_dimensions[2])
            self.ax.grid(False)
            self.ax.set_facecolor('black')
            self.ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.text = self.ax.text2D(.1, 0.1, "", color="white", transform=self.ax.transAxes)
            self.ax.view_init(21, 79)
        self.fig.set_facecolor("black")
        c = "black" if num_dims == 2 else "white"
        text_setter = 'Predrus\'s world' if category.lower() == "universe" else \
            'Predrus\'s particles' if category.lower() == "subatomic" else "Predrus\'s creation"
        self.ax.set_title(text_setter, color=c, fontdict={'fontname': "monospace"})
        self.make_buttons()
        self.make_stars() if stars else None  # makes stars
        Physics.instances.append(self)

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
        r = object_other.position - object_self.position
        IrI = np.sqrt(sum(r**2))
        if object_self.shape == "sphere" and object_other.shape == "sphere":
            if IrI <= object_self.dimensions+object_other.dimensions:
                return r*0
            elif IrI <= object_self.dimensions:
                return r*0
        a = self.G_cons*object_other.mass*r/IrI**3
        forces = a*object_self.mass
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
        for planet in Planet.instances:
            planet.position = planet.initial_position
            planet.velocity = planet.initial_v
            # The map does not update correctly for some reason
            self.t = 0

    def update_dt(self, val):
        self.dt = val

    def evolve_system(self):
        """Checks for all the physical changes that occur to all the Planet instances
            under self dictating physical properties and updates the plot afterwards"""
        for pl in Planet.instances:  # Updates velocities of all planets
            pl.update_velocity()
        for pl in Planet.instances:  # Applies change in location after dt seconds
            pl.position = pl.position + pl.velocity*self.dt
            pl.update_ring_location()
            pl.data = np.c_[pl.position[0], pl.position[1]]
            if self.num_dims == 2:
                pl.scatt.set_offsets(pl.data)
            else:
                pl.data = ([[pl.position[i]] for i in range(3)])
                pl.scatt._offsets3d = tuple(pl.data)
        self.t += self.dt
        if self.dt >= 0.1:
            self.text.set_text(f"{round(self.t, 2)} seconds") if self.t_b else None
        else:
            self.text.set_text(f"{round(self.t, 1)} seconds") if self.t_b else None
        # Here the 3d stuff will come

    def play(self, button_press):
        """Plays 2000 dt evolve_system() cycles"""
        for x in range(2000):
            try:
                self.evolve_system()
                if self.num_dims == 2:
                    self.update_2d_axes()
                else:
                    self.update_3d_axes()
            except:
                break

    def update_3d_axes(self):
        self.update_2d_axes()

    def record(self, frame):
        """Function goes inside FuncAnimation when making animation"""
        self.evolve_system()
        print(frame)
        return [pl.scatt for pl in Planet.instances]

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
        data = [np.random.randint(low=self.universe_dimensions[0][0]*2,
                                  high=self.universe_dimensions[0][1]*2, size=45) for x in range(3)]
        x, y, z = [data[i] for i in range(3)]
        s = np.random.randint(1, 10, 45)
        if self.num_dims == 3:
            self.stars = self.ax.scatter3D(x, y, z, c='white', alpha=0.8, marker="*", s=s)
        else:
            self.stars = self.ax.scatter(x, y, c='white', alpha=0.8, marker="*", s=s)

    def make_n_objects(self, number, clas, rings=False, charge=False):
        """Creates number instances of clas. (Designed for Planet).
        Parameters
        ----------
            number: int
            clas: class (current app supports only Planet)
            rings: Gets passed to Planet. Giving it a chance of 30% of getting a ring.
            Charge: Gets passed to Planet. Giving it a chance of 30% of getting a charge.
        """
        for x in range(number):
            f = clas.random__init__(self, rings=rings, charge=charge)


class Planet:
    """ Creates a particle

    Atributes
    ---------
        universe: Physics object -> Determines physical properties(default = Physics())

        shape: str -> Does not do much yet.(default = "sphere")

        charge: int == +-1 -> Gives + or - charge type to object.(default = None)

        charge_density: int, float -> Units: C m-3 (default = 1)

        total_charge: charge_density*volume -> Units: C

        dimensions: int, float -> Radius -> Units: m (default = 1)

        volume = 4/3 * 3.14 * radius**3 -> Units = m3

        density: int, float -> Mass density -> Units: kg/m3 (default = 1)

        mass = volume*density -> Units: kg

        initial_v: np.ndarray -> Initial velocity of the object as a vector
            [x, y] or [x, y, z] for 2, 3 dimensions respectively.
            (default = np.array([0, 0]) or np.array([0, 0, 0]))

        velocity: current velocity of the object as ndarray

        initial_position: np.ndarray -> Initial position of object given as vector
            [x, y] or [x, y, z] for 2, 3 dimensions.
            (default = np.array([0, 0]) or np.array([0, 0, 0]))

        position: current position of object as ndarray

        ring: bool -> If the planet has a ring.(default = False)

        category: str -> What king of object it is(e.g. Planet, Star...) (default = "planet")

        scatt: mpl.canvas instance (The actuall points on graph)

        data: Nx2 or Nx3 list used when updating the visuals between dt cycles.

    Output
    ------
        Instance of Planet
        """
    instances = []  # List of Planet instances

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
        self.mass = self.density * self.volume  # kg
        if charge:
            self.charge = charge
            self.total_charge = charge*charge_density*4/3*3.14*radius**3
        else:
            self.total_charge = None

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
        plot = self.universe.fig, self.universe.ax
        if self.universe.num_dims == 2:
            self.make_ring() if ring else None
            self.scatt = plot[1].scatter(self.position[0], self.position[1],
                                         s=self.dimensions**3)
        else:
            self.make_ring() if ring else None
            datas = self.position[0], self.position[1], self.position[2]
            if self.density <= 1e11:
                self.scatt = plot[1].scatter(datas[0], datas[1], datas[2],
                                             s=self.dimensions**3 * 4, alpha=0.95)
            else:
                self.scatt = plot[1].scatter(datas[0], datas[1], datas[2],
                                             s=self.dimensions**3, alpha=0.95, c="yellow")

        Planet.instances.append(self)

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
            self.ring = self.universe.ax.scatter(x, y, s=r/4)
        else:
            self.z_ring = z = np.zeros(len(x))
            z = z + self.position[2]
            self.ring = self.universe.ax.scatter(x, y, z, s=r/4)
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
        else:
            pass

    def find_g_forces(self):
        """Uses function of physics instance to obtain net force on self
        outputs this net force as a ndarray."""
        planetsF = self.get_other_planets()  # Forces of other planets on itself.
        forces = np.array([0 for x in range(self.universe.num_dims)])
        for planet in planetsF:  # Finds the overal forces when all planets are considered.
            relative_coord = planet.position - self.position
            forces = forces + self.universe.g_force(self, planet)
        return forces

    def find_charge_forces(self):
        """finds all the gravitational forces of other planets on itself
        these will get returned as a numpy array """
        other_planets = self.get_other_planets()
        forces = np.array([0 for x in range(self.universe.num_dims)])
        for planet in other_planets:
            dist = planet.position - self.position
            forces = forces + self.universe.m_force(self, planet)
        return forces

    def get_other_planets(self):
        """Returns list with all planets that might
        be applying forces on the planet being observed"""
        index, lis = Planet.instances.index(self), Planet.instances.copy()
        lis.pop(index)
        return lis

    def update_velocity(self):
        """Updates the velocities of a planet"""
        forces = self.find_g_forces() + self.find_charge_forces()
        v_new = self.universe.update_velocity(self, forces=forces)
        self.velocity = v_new
        self.check_boundery()

    def check_boundery(self):
        """Reflects particle's getting out of universe's "volume" """
        for index, value in enumerate(self.position):
            if abs(value) >= self.universe.universe_dimensions[0][1]*4:
                self.velocity[index] = -self.velocity[index]

    @staticmethod
    def random__init__(universe, rings=False, charge=None):
        """Creates randomized planet on using universe as template for physics
        Outputs a Planet instance"""
        generate = np.random.uniform
        max = universe.universe_dimensions[0][1]*0.7
        zi = universe.num_dims
        r, d, ip, i_v = generate(1, 5), generate(1, 1e10), \
            generate(-max, max, size=zi), generate(-15, 15, zi)
        ans = np.random.randint(0, 10) if rings else False
        charge = np.random.choice([-1, 1]) if charge else None
        if ans >= 7:
            ans = True
        else:
            ans = False
        return Planet(radius=r, density=d, initial_position=ip, universe=universe, initial_v=i_v,
                      ring=ans, charge=charge)

    def set_v_orbit(self, sun):
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

    def make_all_planets_orbit(self, both_axes=False):
        """Makes "self" the sun
        both axes refers to a more adventurous orbital style"""
        i = 1
        for planet in self.get_other_planets():
            planet.set_v_orbit(self)
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
            i = i+1 if both_axes else i


def make_solar_system(num_dims=2, dt=0.1, universe_dimensions=250, t_b=True,
                      stars=True, sun_density=1e12, sun_radius=10, n_planets=10,
                      rand_orbits=True, show=True, save=False, rings=False, charge=False):
    """Just makes it easier to create a working simulation for testing."""
    universe = Physics(num_dims=num_dims, dt=dt, universe_dimensions=universe_dimensions,
                       t_b=t_b, stars=stars)
    earth = Planet(universe=universe, density=sun_density, radius=sun_radius,
                   initial_position=(0 for x in range(num_dims)))
    universe.make_n_objects(n_planets, Planet, rings=rings)
    earth.make_all_planets_orbit(both_axes=rand_orbits)
    if show == True:
        plt.show()
    if save == True:
        universe.record_gif(name_gif='gravity_3d_new.gif', frames=1000, fps=35, repeat=False)
    print([x for x in earth.__dict__])


def make_protons_and_electrons():
    """Just makes it easier to create a working simulation for testing."""
    universe = Physics(num_dims=3, universe_dimensions=100, t=0, dt=0.5, t_b=True,
                       category='subatomic')
    for x in range(10):
        position = np.random.uniform(-70, 70, 3)
        choice = np.random.choice([-1, 1])
        planet = Planet(radius=1, density=200, initial_position=position, charge=choice,
                        charge_density=0.001, universe=universe)
    plt.show()


# make_protons_and_electrons()
if __name__ == "__main__":
    print("hello")
    make_solar_system(num_dims=3, dt=0.07, universe_dimensions=250, t_b=True,
                      stars=True, sun_density=1e12, sun_radius=10, n_planets=10, rand_orbits=True,
                      show=True, save=False, rings=True, charge=False)
