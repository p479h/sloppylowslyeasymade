"""
    This script will attempt to simulate gravity on a particle.
    The follow up will be simulating gravity between a few particles.
    Finally, the solar system!
    """
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class Physics:
    """Physics was created as a class, because I want physical laws to be mutable!
    Imagine being able to have a glimpse of what the universe would be like if
    the fundamental forces of nature behaved differently!
    Functions defined here will represent physical laws or suport for visuals.
    IN the future, there will be support for charged particles."""

    def __init__(self, origin=None, universe_dimensions=150, t_0=0, t=0, dt=0.1, num_dims=2):
        self.origin = origin if origin else [0 for x in range(num_dims)]  # (m, m)
        self.universe_dimensions = [(-universe_dimensions, universe_dimensions)
                                    for dimension in range(num_dims)]  # m This is the lengths of -+ xyz axes
        self.num_dims = num_dims
        self.t_0 = t_0  # s
        self.t = t  # s
        self.dt = dt  # s
        self.G_cons = 6.674*1e-11  # m3 kg-1 s-2
        self.fig, self.ax = plt.subplots()
        self.ax.set(fc='black', xlim=self.universe_dimensions[0], ylim=self.universe_dimensions[1])

    def g_force(self, object_self, object_other):
        """object_self feels the force, object_other applies force"""
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

    def update_velocity(self, object, forces):
        """receives np.array([f_x, f_y, f_z])
            uses it to calculate change in velocity
            after dt seconds.
            """
        dt = self.dt
        dps = forces*dt  # Changes in momentum
        dvs = dps/object.mass  # Changes in speed
        vs = object.velocity + dvs  # Final velocity
        return vs

    def update_axes(self):
        """Updates the plot after planetary movement"""
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def evolve_system(self):
        """Lets the position of the planets change"""
        for pl in Planet.planets:  # Updates velocities of all planets
            pl.update_velocity()
        for pl in Planet.planets:  # Applies change in location after dt seconds
            pl.position = pl.temporary_position + pl.velocity*self.dt
            pl.temporary_position = pl.position
            pl.data = np.c_[pl.position[0], pl.position[1]]
            pl.scatt.set_offsets(pl.data)

    def play(self, button_press):
        """Plays 2000 dt period"""
        for x in range(2000):
            self.evolve_system()
            self.update_axes()

    def record(self, frame):
        """Function used for FuncAnimation"""
        self.evolve_system()
        print(frame)
        return [pl.scatt for pl in Planet.planets]


class Planet:
    """Class refers to planets, but a more appropriate name
    would be particle as I plan on adding support for charges."""
    planets = []  # List of Planet instances

    def __init__(self, shape="sphere", radius=1, density=10,
                 initial_position=None, initial_v=None, charge=None,
                 universe=None):
        """
            Planet characteristics. Universe is a Physics instance
            shape is a string
            dimensions is the radius, but only for spheres(future_update for qudrlaterals)
            density is a float or integer
            initial position is a set of coordnates such as (x, y, z)
            charge has no function yet
            initial_v is initial velocity
            WATCH OUT FOR THE NUMBER OF DIMESIONS. Should match with universe!
            """
        self.universe = universe
        self.shape = shape
        self.dimensions = radius   # m3
        self.volume = 4/3*3.14*self.dimensions**3
        self.density = density  # kg m-3
        self.mass = self.density * self.volume  # kg
        self.charge = charge if charge else None
        if type(initial_position) == tuple:
            initial_position = np.array(initial_position)
        if type(initial_v) == tuple:
            initial_v = np.array(initial_v)
        self.velocity = initial_v
        self.position = initial_position
        self.temporary_position = self.position.copy()
        plot = self.universe.fig, self.universe.ax
        self.scatt = plot[1].scatter(self.position[0], self.position[1], s=self.dimensions**3)
        Planet.planets.append(self)

    def find_g_forces(self):
        """Calculates net gravitational pull from all other planets
        returns them as a numpy array (f_x, f_y, f_i,...)"""
        planetsF = Planet.planets.copy()
        index = Planet.planets.index(self)
        planetsF.pop(index)  # Forces of other planets on itself.
        forces = np.array([0 for x in range(self.universe.num_dims)])
        for planet in planetsF:  # Finds the overal forces when all planets are considered.
            relative_coord = planet.temporary_position - self.temporary_position
            forces = forces + self.universe.g_force(self, planet)
        return forces

    def update_velocity(self):
        """Updates the velocities of a planet"""
        v_new = self.universe.update_velocity(self, forces=self.find_g_forces())
        self.velocity = v_new
        self.check_boundery()

    def check_boundery(self):
        """Does not allow particles to be lost because they escaped the figure"""
        for index, value in enumerate(self.position):
            if abs(value) >= self.universe.universe_dimensions[0][1]*0.8:
                self.velocity[index] = -self.velocity[index]

    @staticmethod
    def random__init__(universe):
        """Creates randomized planet"""
        generate = np.random.uniform
        r, d, ip, i_v = generate(1, 5), generate(1, 1e10), \
            generate(-100, 100, size=2), generate(-10, 10, 2)
        return Planet(radius=r, density=d, initial_position=ip, universe=universe, initial_v=i_v)


universe = Physics(dt=0.03)
fig2, ax2 = plt.subplots()  # Creates button to play animation. I wish this was in one of the classes. But the button wouldnt work.
button = mpl.widgets.Button(ax2, label='Play')
button.on_clicked(universe.play)
for x in range(10):  # Just makes 10 planets.
    h = Planet.random__init__(universe)
sun = Planet(initial_position=(50, -10), initial_v=(0, 0), radius=8, density=1e11, universe=universe)  # Now a few specific planets
sun2 = Planet(initial_position=(-50, 10), initial_v=(0, 0), radius=8, density=1e11, universe=universe)
venus = Planet(initial_position=(0, -100), initial_v=(0, 0), shape="sphere", radius=3, density=1e9, universe=universe)
mars = Planet(initial_position=(0, 100), initial_v=(0, 0), shape="sphere", radius=3, density=1e9, universe=universe)

plt.show()
# ani = FuncAnimation(universe.fig, universe.record, repeat=False, frames=900, blit=True, interval=1,)
# writergif = mpl.animation.PillowWriter(fps=30)
# ani.save('gravity_long.gif', writer=writergif)
