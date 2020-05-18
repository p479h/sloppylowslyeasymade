"""
    gravity.py in 3d
    """
from matplotlib.animation import FuncAnimation
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as p3


class Physics:
    """Physics was created as a class, because I want physical laws to be mutable!
    Imagine being able to have a glimpse of what the universe would be like if
    the fundamental forces of nature behaved differently!
    Functions defined here will represent physical laws or suport for visuals.
    IN the future, there will be support for charged particles."""

    def __init__(self, origin=None, universe_dimensions=150, t_0=0, t=0, dt=0.1, num_dims=2, t_b=False,
                 stars=False):
        self.origin = origin if origin else np.array([0 for x in range(num_dims)])  # (m, m)
        self.universe_dimensions = [(-universe_dimensions, universe_dimensions)
                                    for dimension in range(num_dims)]  # m This is the lengths of -+ xyz axes
        self.num_dims = num_dims
        self.t_0 = t_0  # s
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
        self.ax.set_title('Predru\'s world', color="white", fontdict={'fontname': "monospace"})
        self.make_buttons()
        self.make_stars() if stars else None  # makes stars

    def g_force(self, object_self, object_other):
        """object_self feels the force, object_other applies force
        RETURNS THE FORCE OF OTHER ON SELF"""
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
        """WHEN COMPLETED IT WILL FIND THE MAGENTIC FORCES"""
        if object_self.charge == None or object_other.change == None:
            return self.origin * 0
        forces = self.g_force(object_self, object_other)  # uses the set up of the gravitational forces.
        forces = forces*self.C_cons/self.G_cons/object_other.mass/object_self.mass
        forces = forces*object_self.charge*object_other*charge*-1
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

    def update_2d_axes(self):
        """Updates the plot after planetary movement"""
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def make_buttons(self):
        """Creates button that starts the animation"""
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

    def replay(self, click):
        for planet in Planet.planets:
            planet.position = planet.initial_position
            planet.velocity = planet.initial_v
            # The map does not update correctly for some reason
            self.t = 0

    def update_dt(self, val):
        self.dt = val

    def evolve_system(self):
        """Lets the position of the planets change"""
        for pl in Planet.planets:  # Updates velocities of all planets
            pl.update_velocity()
        for pl in Planet.planets:  # Applies change in location after dt seconds
            pl.position = pl.position + pl.velocity*self.dt
            pl.update_ring_location()
            pl.data = np.c_[pl.position[0], pl.position[1]]
            if self.num_dims == 2:
                pl.scatt.set_offsets(pl.data)
            else:
                pl.data = ([[pl.position[i]] for i in range(3)])
                pl.scatt._offsets3d = tuple(pl.data)
        self.t += self.dt
        self.text.set_text(f"{round(self.t, 2)} seconds") if self.t_b else None

        # Here the 3d stuff will come

    def play(self, button_press):
        """Plays 2000 dt period"""
        for x in range(2000):
            self.evolve_system()
            if self.num_dims == 2:
                self.update_2d_axes()
            else:
                self.update_3d_axes()

    def update_3d_axes(self):
        self.update_2d_axes()

    def record(self, frame):
        """Function used for FuncAnimation"""
        self.evolve_system()
        print(frame)
        return [pl.scatt for pl in Planet.planets]

    def record_gif(self, name_gif='gravity_3d.gif', frames=100, fps=40, repeat=False):
        """Saves the gif without need for looking up functions"""
        ani = FuncAnimation(self.fig, self.record, repeat=repeat,
                            frames=frames, blit=True, interval=1)
        writergif = mpl.animation.PillowWriter(fps=fps)
        ani.save(name_gif, writer=writergif)
        print("Completed!")

    def make_stars(self):
        "makes stars for plot"
        data = [np.random.randint(low=self.universe_dimensions[0][0]*2, high=self.universe_dimensions[0][1]*2, size=45) for x in range(3)]
        x, y, z = [data[i] for i in range(3)]
        s = np.random.randint(1, 10, 45)
        if self.num_dims == 3:
            self.stars = self.ax.scatter3D(x, y, z, c='white', alpha=0.8, marker="*", s=s)
        else:
            self.stars = self.ax.scatter(x, y, c='white', alpha=0.8, marker="*", s=s)

    def make_n_objects(self, number, clas, rings=False):
        """makes n planet
        universe.make_n_objects(10, Planet)"""
        for x in range(number):
            f = clas.random__init__(self, rings=rings)


class Planet:
    """Class refers to planets, but a more appropriate name
    would be particle as I plan on adding support for charges."""
    planets = []  # List of Planet instances

    def __init__(self, shape="sphere", radius=1, density=10,
                 initial_position=None, initial_v=None, charge=None,
                 universe=None, ring=False):
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
        self.charge = charge  # NUMBER 0=-, 1=+
        self.dimensions = radius   # m3
        self.volume = 4/3*3.14*self.dimensions**3
        self.density = density  # kg m-3
        self.mass = self.density * self.volume  # kg
        self.charge = charge if charge else None
        if type(initial_position) == tuple:
            initial_position = np.array(initial_position)
        elif type(initial_position) == np.ndarray:
            initial_position = initial_position
        else:
            initial_position = self.universe.origin
        if type(initial_v) == tuple:
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
                                             s=self.dimensions**3, alpha=0.95)

        Planet.planets.append(self)

    def make_ring(self):
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
        """Calculates net gravitational pull from all other planets
        returns them as a numpy array (f_x, f_y, f_i,...)"""
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
        index, lis = Planet.planets.index(self), Planet.planets.copy()
        lis.pop(index)
        return lis

    def update_velocity(self):
        """Updates the velocities of a planet"""
        forces = self.find_g_forces() + self.find_charge_forces()
        v_new = self.universe.update_velocity(self, forces=forces)
        self.velocity = v_new
        self.check_boundery()

    def check_boundery(self):
        """Does not allow particles to be lost because they escaped the figure"""
        for index, value in enumerate(self.position):
            if abs(value) >= self.universe.universe_dimensions[0][1]*4:
                self.velocity[index] = -self.velocity[index]

    @staticmethod
    def random__init__(universe, rings=False):
        """Creates randomized planet"""
        generate = np.random.uniform
        max = universe.universe_dimensions[0][1]*0.7
        zi = universe.num_dims
        r, d, ip, i_v = generate(1, 5), generate(1, 1e10), \
            generate(-max, max, size=zi), generate(-15, 15, zi)
        ans = np.random.randint(0, 10) if rings else False
        if ans >= 7:
            ans = True
        else:
            ans = False
        return Planet(radius=r, density=d, initial_position=ip, universe=universe, initial_v=i_v, ring=ans)

    def set_v_orbit(self, sun):
        """sets planet's orbit around it's sun!"""
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
            if self.universe.num_dims == 3:
                if i % 2 == 0:
                    planet.velocity = planet.velocity[::-1]
                    planet.position = planet.position[::-1]

                    if i % 4 == 0 and self.universe.num_dims == 3:
                        v = planet.velocity[planet.velocity != 0][0]/np.sqrt(2)
                        planet.velocity = np.array([v, 0, v])

                elif i % 3 == 0:
                    v = planet.velocity[planet.velocity != 0][0]/np.sqrt(2)
                    planet.velocity = np.array([-1*v, 0, v])
            if np.random.randint(0, 10) % 2 == 0:
                planet.velocity = planet.velocity*-1
            planet.initial_v = planet.velocity.copy()
            planet.initial_position = planet.position.copy()
            i = i+1 if both_axes else i


def make_solar_system(num_dims=2, dt=0.1, universe_dimensions=250, t_b=True,
                      stars=True, sun_density=1e12, sun_radius=10, n_planets=10,
                      rand_orbits=True, show=True, save=False, rings=False):
    universe = Physics(num_dims=num_dims, dt=dt, universe_dimensions=universe_dimensions,
                       t_b=t_b, stars=stars)
    earth = Planet(universe=universe, density=sun_density, radius=sun_radius,
                   initial_position=(0 for x in range(num_dims)))
    universe.make_n_objects(n_planets, Planet, rings=rings)
    earth.make_all_planets_orbit(both_axes=rand_orbits)
    if show == True:
        plt.show()
    if save == True:
        universe.record_gif(name_gif='gravity_3d.gif', frames=1000, fps=25, repeat=False)


make_solar_system(num_dims=3, dt=0.05, universe_dimensions=250, t_b=True,
                  stars=True, sun_density=1e12, sun_radius=10, n_planets=10, rand_orbits=True,
                  show=True, save=False, rings=True)
