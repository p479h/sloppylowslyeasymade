"""
    This is the first class to be created. It will contain the main figure and axes.
    It should also contain a function to make all the buttons necessary. It should
    contain a list with all the important objects inside it."""

from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
from matplotlib.patches import FancyBboxPatch


class Physics:
    """Back-bone of the simulation. Contains the main figure and axes"""
    instances = []  # You never know when you will neeed to acces Physics instances

    def __init__(self, u_size=1000, num_dims=2, stars=True, dt=0.01,
                 show_time=False, name="Predru\'s world", recording=False, *args, **kwargs):
        # Follow Universe characteristics
        self.u_size = u_size  # If universe is a cube, u_size = side length
        self.num_dims = num_dims  # Number of dimensions (2-3)
        self.stars = stars  # If the plot has stars
        self.zeroes = np.array([0 for n in range(num_dims)])  # Easy starting point
        self.t = 0  # s
        self.dt = dt  # s
        self.constants = {"G": 6.67408*1e-11, "K_e": 8.9875517923*1e9}  # Constants in STI
        self.show_time = show_time
        self.name = name  # Title of the figure
        self.objects = []  # List of objects in Physics instance

        # Follow elements about recording
        self.recording = recording  # True for recorded Simulation

        # Follow elements that concerns plotting and stars
        self.make_plot()  # makes the plot
        self.buttons = {}  # Easy access to buttons and their axes
        self.sliders = {}  # E.g {"Button1":{"ax":<object>, "button":<Button>}}
        self.radiobuttons = {}  # {"cycles":{"ax":<object>, "slider":<Slider>}}
        self.widgets_fig = plt.figure(figsize=(4, 3))  # Separate figure for widgets
        self.make_test_radiobuttons()
        self.new_make_buttons()  # makes buttons
        self.new_make_sliders()
        self.make_stars() if stars else None  # Makes stars for a prettier background
        self.cmap = {}  # Information about cmap

        # Stuff on the colormaps
        self.cmap["cmaps"] = plt.colormaps()
        self.cmap["cmap"] = "inferno"
        self.cmap["ax"] = None  # Will be used for an actual axes with text
        self.cmap["buttons"] = {}  # Here we will have the buttons and their axes
        self.cmap["current_txt"] = None
        """{'cmaps':all cmaps, 'ax':text axes, 'current_txt': text instance,
            'buttons':{'button_i: {'ax_i':ax, 'button': instance, 'id'=reference_on_clicked}'}}"""
        self.colorbar = None  # Placeholder for colorbar
        self.make_text_display()

        # More stuff on organization
        self.__class__.instances.append(self)  # Adds self to instances

        # Things that functions depend on
        self.running = False  # will be set to true while simulation runs
        # Should be set to false if simulation is to begin.
        self.show = "all"  # Used to choose which paths are shown.
        self.full_paths_showing = False  # Bug prevention
        self.select_show = "all"  # Chooses which objects Display
        self.data_status = "needs_cycles"  # For when we just need to append new data
        self.data_status = "updated"  # For when we don't need more calculations
        self.data_status = "empty"  # For when all calculations must be remade
        self.color_status = "empty"  # For when color_arrays have to be resetted
        self.color_status = "updated"  # For when color_arrays can be left out

        # Things for testing later
        self.object_pairs = []  # Will help with efficiency

    def find_pairs(self):
        if len(self.object_pairs) == 0:
            for index, object in enumerate(self.objects):
                for object2 in self.objects[index+1:len(self.objects)]:
                    if index+1 != len(self.objects)-1:
                        self.object_pairs.append([object, object2])

#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
# widgets

    def make_text_display(self):
        """Makes the very pretty colormap selector!!!"""
        # making actual text
        # Making colorbar
        self.cmap["ax"] = self.widgets_fig.add_axes([0.5, 0.3, 0.4, 0.25])
        ax = self.cmap["ax"]  # Shorter writting
        grid = np.meshgrid(np.linspace(0, 1, 220), np.ones(100))[0]  # We need this for colors
        self.colorbar = self.cmap["ax"].imshow(grid, cmap=self.cmap['cmap'])
        ax.format_coord = lambda x, y: ""  # This ensures the main GUI. Doesnt fuck up.
        ax.patch.set_edgecolor("black")  # Just for appearences
        ax.patch.set_linewidth('1')  # Just for appearences
        ax.tick_params("both", length=0, labelsize=0, labelcolor="white")  # Also prettiness
        fontdict = {'fontname': "monospace", "size": 8}
        text = f"{self.cmap['cmap']}"
        p_bbox = FancyBboxPatch((0.33, 0.75), abs(0.345), abs(0.1),
                                boxstyle="round,pad=0.1", ec="k", fc="none",
                                zorder=10., transform=ax.transAxes)  # Nice round shape
        self.cmap["current_txt"] = ax.text(0.25, 0.78, text, fontdict, transform=ax.transAxes)
        ax.add_patch(p_bbox)  # Adds pretty box!

        def change_text(self, commd):  # Command for the buttons
            try:
                current_cmap = self.objects[0].cmap
                index = self.cmap['cmaps'].index(current_cmap)
                text = self.cmap["current_txt"]
                if commd == "advance":
                    index += 1
                elif commd == "None":
                    index = index
                else:
                    index -= 1
                new_cmap = self.cmap['cmaps'][index]
                text.set_text(self.cmap['cmaps'][index])
                for object in self.objects:
                    object.cmap = self.cmap['cmaps'][index]
                self.colorbar.set_cmap(new_cmap)
                self.widgets_fig.canvas.draw()
                self.widgets_fig.canvas.flush_events()
                self.top_radio_button()
            except:
                print("Press paths first. Then use this command.")

        # Wraps is a decorator because no sane person would write func twice.
        def wraps(func, self, commd): return lambda click: func(self, commd)
        back_func = wraps(change_text, self, "back")
        advance_func = wraps(change_text, self, "advance")  # Each button gets own func
        spec1, spec2 = [0.5, 0.46, 0.09, 0.09], [0.809, 0.46, 0.09, 0.09]  # Axes of buttons
        self.cmap['buttons']['back'] = {}  # organization
        self.cmap['buttons']['advance'] = {}
        self.cmap['buttons']['back']['ax'] = axb = \
            self.widgets_fig.add_axes(spec1)
        self.cmap['buttons']['advance']['ax'] = axa = \
            self.widgets_fig.add_axes(spec2)
        self.cmap['buttons']['back']['button'] = \
            mpl.widgets.Button(axb, "<-", color='green')
        self.cmap['buttons']['advance']['button'] =\
            mpl.widgets.Button(axa, "->", color='green')
        id = self.cmap['buttons']['advance']['button'].on_clicked(advance_func)
        self.cmap['buttons']['advance']['id'] = id  # sets identification
        id = self.cmap['buttons']['back']['button'].on_clicked(back_func)
        self.cmap['buttons']['back']['id'] = id  # Sets identification
        self.cmap['buttons']['advance']['button'].ax._visible = False
        self.cmap['buttons']['back']['button'].ax._visible = False
        self.colorbar._axes._visible = False
        self.widgets_fig.canvas.draw()  # Makes the function responsive.
        self.widgets_fig.canvas.flush_events()

    def new_make_buttons(self):
        # First define some functions:
        def close(click): return plt.close("all")

        def replay(click):
            self.cmap['buttons']['advance']['button'].ax._visible = False
            self.cmap['buttons']['back']['button'].ax._visible = False
            self.colorbar._axes._visible = False
            self.running = True  # Sets the planes running again.
            self.replay()

        def make_stop_button(self):
            ax = self.widgets_fig.add_axes([0.5, 0.8, 0.2001, 0.2])
            self.buttons["Stop"] = {}
            self.buttons["Stop"]["ax"] = ax
            button = mpl.widgets.Button(ax, "Stop", color="red")
            ax._visible = False

            def func(click):
                self.running = False
                self.buttons['Play']['ax'].set_visible(True)
                self.buttons["Stop"]['ax'].set_visible(False)

            def wraper(self, func): return lambda click: func(self)
            self.buttons["Stop"]["id"] = button.on_clicked(wraper(self, func))
            self.buttons["Stop"]["button"] = button

        def play(click):
            self.buttons['Stop']['ax'].set_visible(True)
            self.buttons["Play"]['ax'].set_visible(False)
            self.cmap['buttons']['advance']['button'].ax._visible = False
            self.cmap['buttons']['back']['button'].ax._visible = False
            self.colorbar._axes._visible = False
            self.widgets_fig.canvas.draw()
            self.widgets_fig.canvas.flush_events()
            self.play()

        def new_button_func(self):
            """Used in one of the buttons"""
            for key in self.radiobuttons:
                self.radiobuttons[key]['ax'].set_visible(True)
            self.buttons["Stop"]["button"].ax._visible = False
            self.buttons["Play"]["button"].ax._visible = True
            self.cmap['buttons']['advance']['button'].ax._visible = True
            self.cmap['buttons']['back']['button'].ax._visible = True
            self.colorbar._axes._visible = True
            self.widgets_fig.canvas.draw()  # Redraws graph!
            self.widgets_fig.canvas.flush_events()
            self.running = False
        make_stop_button(self)

        def path_maker(click): return [new_button_func(self),
                                       self.new_collect_data(),
                                       self.top_radio_button()]
        commands = [play, replay, path_maker, close]  # button commands in order
        # Play-Runs_simulation; #replay-Restarts simulation;
        # path_maker-shows full paths; #close-Closes all figures.
        names = 'Play,Replay,Path,Exit'.split(",")  # Button labels
        colors = ["green", "blue", "cornflowerblue", "red"]
        for x in range(4):  # Because there are 4 buttons
            if x % 2 == 0:
                new_axes = self.widgets_fig.add_axes([0.5, 0.8-x/10, 0.2, 0.2])
            else:
                new_axes = self.widgets_fig.add_axes([0.7, 0.8-(x-1)/10, 0.2, 0.2])
            new_button = mpl.widgets.Button(new_axes, names[x], color=colors[x])
            id = new_button.on_clicked(commands[x])
            self.buttons[names[x]] = {"ax": new_axes, "button": new_button, "id": id}  # Organizing

    def make_test_radiobuttons(self):
        """Makes radio buttons and creates function to set them visible or invisible"""
        new_axes = self.widgets_fig.add_axes([0.1, 0.6, 0.3, 0.3])
        commands = 'all,sun,planet,moon'.split(',')  # Will later include subatomic stuff.
        button = mpl.widgets.RadioButtons(new_axes, commands, activecolor='purple')
        def funcs(label): return [self.top_radio_button()]
        button.on_clicked(funcs)  # Show selected category
        self.radiobuttons["Object_categories_shown"] = {"ax": new_axes, "button": button}
        new_axes = self.widgets_fig.add_axes([0.1, 0.3, 0.3, 0.3])
        commands = 'None,colorvx,colorvy,colorvz,speed'.split(',')
        button = mpl.widgets.RadioButtons(new_axes, commands, activecolor='purple')

        def funcs2(Label):
            self.color_status = "empty"  # Helps with efficiency
            self.top_radio_button()
        button.on_clicked(funcs2)  # Attribute velocity as color
        self.radiobuttons["v_comps"] = {"ax": new_axes, "button": button}
        self.color_status = "updated"  # Only needs to change if someone changes botton buttons
        for key in self.radiobuttons:  # Makes axes invisible as they can't be used initially
            self.radiobuttons[key]["ax"].set_visible(False)
        self.widgets_fig.canvas.draw()  # Redraws RadioButtons!
        self.widgets_fig.canvas.flush_events()

    def new_make_sliders(self):
        """Makes 2 sliders"""
        axes = []  # Temporary storage for axes
        for x in range(2):
            specifications = [0.2, 0.1+x/15, 0.6, 0.05]
            new_axes = self.widgets_fig.add_axes(specifications)
            axes.append(new_axes)
        slider = mpl.widgets.Slider(axes[1], label='cycles',
                                    valmin=10, valmax=4000,
                                    valstep=4, valinit=500)
        id = slider.on_changed(lambda val: self.update_data_status())
        self.sliders["cycles"] = {"ax": axes[1], "slider": slider, "id": id}
        slider = mpl.widgets.Slider(axes[0], label='dt', valmin=0.001,
                                    valmax=0.2, valstep=0.001, valinit=self.dt)

        def decorator(self, func):  # Save's space for other more important functions
            def wraps(val): return func(self, val)
            return wraps  # different ways of doing the same thing.

        def update_dt(self, val):
            self.dt = val  # New dt
            self.data_status = "empty"  # New data must be calculated

        id = slider.on_changed(decorator(self, update_dt))  # Updates dt
        self.sliders["dt"] = {"ax": axes[0], "slider": slider, "id": id}

    def new_collect_data(self):
        """Collects n cycles of planetary movement. n is taken from a slider.
        This information is stored as object.path_data and object.v_data
        for positions and velocities respectively"""
        self.running = False
        shape = (1, self.num_dims)  # Shape of the multidimentional array
        number_cycles = int(self.sliders["cycles"]["slider"].val)  # Gets cycles from slider
        print(number_cycles, "Cycles collected")  # Info about number of cycles
        if self.data_status == "empty" or len(self.objects[0].path_data[1:, 0]) - number_cycles >= 0\
                or self.color_status == "empty":  # Ensures new data is only gathered when needed
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
        self.data_status = "updated"  # Prevents repetitive calculations

    def update_data_status(self):
        """activates upon clicking cycles sliders
        helps efficiency"""
        if self.data_status == "updated":
            self.data_status = "needs_cycles"
        else:
            self.data_status = "empty"

    def top_radio_button(self):
        """This function will be used by the top radio_button to determine which
        objects will be shown"""
        if self.data_status != "updated":
            self.new_collect_data()  # Collects data on color... Sets running to false
        else:
            self.running = False
        to_show = self.radiobuttons["Object_categories_shown"]['button'].value_selected  # Category to show
        comp_v = self.radiobuttons["v_comps"]['button'].value_selected
        if to_show == "all" and self.color_status == "empty":
            for object in self.objects:
                if self.num_dims == 2:
                    object.scatt._offsets = object.path_data
                    object.scatt._facecolors = object.get_facecolor_array_from_v_data(comp_v)
                else:
                    ccc = object.get_facecolor_array_from_v_data(comp_v)
                    object.scatt._facecolor3d = ccc  # Because matplotlib 3d is Broken!!!
                    object.scatt._edgecolor3d = ccc
                    object.scatt._offsets3d = [object.path_data[:, i] for i in range(3)]
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
        elif to_show == "all" and self.color_status == "updated":
            # This is fow when only the positions change
            for object in self.objects:
                if self.num_dims == 2:
                    object.scatt._offsets = object.path_data[:]
                    object.scatt._facecolors = \
                        object.get_facecolor_array_from_v_data(comp_v)
                else:
                    object.scatt._offsets3d = [object.path_data[:, i] for i in range(3)]
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
        else:
            if self.color_status == "empty":
                for object in self.objects:
                    if object.category == to_show:  # These are being defined after the if statement for memory
                        if self.num_dims == 2:
                            object.scatt._offsets = object.path_data
                            object.scatt._facecolors = \
                                object.get_facecolor_array_from_v_data(comp_v)
                        else:
                            ccc = object.get_facecolor_array_from_v_data(comp_v)
                            object.scatt._facecolor3d = ccc  # Because matplotlib 3d is Broken!!!
                            object.scatt._edgecolor3d = ccc
                            object.scatt._offsets3d = [object.path_data[:, i] for i in range(3)]
                    else:
                        object.temporarily_hide()
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
            elif self.color_status == "updated":
                for object in self.objects:
                    if object.category == to_show:
                        if self.num_dims == 2:
                            object.scatt._offsets = object.path_data
                        else:
                            object.scatt._offsets3d = [object.path_data[:, i] for i in range(3)]
                    else:
                        object.temporarily_hide()
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()
            else:
                print("PRoblem in line 400something")
# End of widgets
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################

    def replay(self):
        self.buttons["Play"]["button"].ax._visible = False
        self.buttons["Stop"]["button"].ax._visible = True
        """Gets objects to initial state"""
        for object in self.objects:
            object.velocity = object.init_v
            object.position = object.init_p
        self.t = 0
        self.play() if self.running == True else None

    def play(self):
        self.running = True  # Set running status
        for key in self.radiobuttons:
            self.radiobuttons[key]['ax'].set_visible(False)
        self.widgets_fig.canvas.draw()
        self.widgets_fig.canvas.flush_events()
        for object in self.objects:
            object.reset_own_scatt()
        while self.running:  # Pressing a button will disrupt the play. But not throw errors.
            for object in self.objects:  # update all the velocities
                object.calculate_net_acc()
                object.update_velocity()
            for object in self.objects:  # updates all the positions
                if not self.running:
                    break
                object.update_position()
                object.update_ring_location() if object.ring else None
                object.update_scatt_to_current_position()
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
            self.t = self.t + self.dt
            self.text.set_text(f"{round(self.t, 1)} seconds") if\
                self.show_time else None
        else:
            print("Play was just disrupted")

    def make_stars(self):
        "Adds stars to Physics instance.ax"
        size = self.u_size, -1*self.u_size  # These values were randomly chosen
        data = [np.random.randint(low=size[1]*2,
                                  high=size[0]*2, size=45) for x in range(3)]
        x, y, z = [data[i] for i in range(3)]
        s = np.random.randint(1, 10, 45)  # Random distribution of star sizes
        if self.num_dims == 3:
            self.stars = self.ax.scatter3D(x, y, z, c='white',
                                           alpha=0.8, marker="*", s=s)
        else:
            self.stars = self.ax.scatter(x, y, c='white',
                                         alpha=0.8, marker="*", s=s)

    def make_plot(self):
        """Makes the visuals"""
        self.fig = plt.figure()
        lims = lims = -1*self.u_size, self.u_size  # Dimensions of axes
        # Checks number of dimensions of axes
        if self.num_dims == 2:  # 2dimensions
            self.ax = self.fig.add_subplot(111)
            self.fig.set_facecolor("black")
            self.ax.set(fc='black', xlim=lims, ylim=lims)
            self.text = self.ax.text(.1, 0.1, "", color="white",
                                     transform=self.ax.transAxes)  # Place where time will show
        elif self.num_dims == 3:  # 3 dimensions
            self.ax = p3.Axes3D(self.fig)
            self.ax.set(fc='black', xlim=lims, ylim=lims, zlim=lims)
            self.ax.grid(False)  # Makes it prettier
            self.ax.w_xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))  # Erases grids
            self.ax.w_yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.ax.w_zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
            self.text = self.ax.text2D(.1, 0.1, "", color="white",
                                       transform=self.ax.transAxes)
            self.ax.view_init(21, 79)  # Nice angle for visuals
        else:
            # In case too many dimensions are used.
            print('Number of dimensions not supported for visualization')
        # Color c of text depends on whether you are recording or not
        c = "black" if self.num_dims == 2 and self.recording else "white"
        text_setter = self.name if self.name else "Predru\'s world"
        self.ax.set_title(text_setter, color=c, fontdict={'fontname': "monospace"})

        
class Object:
    instances = []

    def __init__(self, universe=None, radius=10, rel_size=10,
                 init_v=None, init_p=None, name=None, charge=None, charge_density=0,
                 density=1e10, ring=False, color=None, cmap="inferno", marker=None,
                 category="all"):
        # characteristics
        self.universe = universe
        self.num_dims = self.universe.num_dims  # Used for plotting as well
        self.radius = radius  # Radius m
        self.volume = 4/3*3.14*radius**3
        self.velocity = init_v
        self.position = init_p
        self.init_v = init_v  # Initial velocity
        self.init_p = init_p  # Initial position
        self.density = density  # Mass per unit volume
        self.mass = density*self.volume
        self.ring = True if ring else None  # Make ring?
        self.check_p_and_v()  # Checks inputs for velocity and position
        self.name = name  # Could be used to identify object later
        self.charge = charge  # Charge +-1
        self.charge_density = charge_density  # density of charge per unit volume
        self.total_charge = charge*charge_density*self.volume if charge else None
        self.category = category  # Used for stuff

        # Plot related information
        self.color = color
        self.rel_size = int(rel_size)  # Used as a multiplier of size in plot
        self.cmap = cmap
        self.universe.cmap["cmap"] = cmap
        self.marker = marker
        self._sizes = None  # Will be used for plotting
        self._facecolors = None
        self._edgecolors = None
        self._offsets3d = None  # Stores first position for 3d ploting
        self._offsets = None  # Usef for 2d plotting
        self.ax = self.universe.ax  # Facilitates writting
        self.make_ring() if ring else None  # Makes rings

        # Attributes used in functions
        self.net_acc = self.universe.zeroes
        self.other_objects = []  # Used to facilitate computations
        self.path_data = None  # Used for recordings
        self.v_data = None  # Used for recordings
        self.x_ring = None if not hasattr(self, 'x_ring') else self.x_ring
        self.y_ring = None if not hasattr(self, 'y_ring') else self.y_ring
        self.z_ring = None if not hasattr(self, 'z_ring') else self.z_ring  # Used for reference with rings
        self.ring_location = None if not hasattr(self, 'ring_location') else self.ring_location  # Full coordinates of ring
        self.ring_scatt = None if not hasattr(self, 'ring_scatt') else self.ring_scatt  # Scatt of ring
        self.ring_offsets3d = None if not hasattr(self, 'ring_offsets3d') else self.ring_offsets3d  # _offsets 3d of rings

        # Creates easy access to own instances
        try:
            self.__class__.__bases__.instances = []
            self.__class__.instances.append(self)
            self.universe.objects.append(self)
        except:
            self.__class__.instances.append(self)
            self.universe.objects.append(self)

    def reset_own_scatt(self):
        """Get's plot to initial state!!!
        If you plan on modifying this code. Note how 3d has scat._facecolor3d
        scatt._edgecolor3d without the 's' in the end as in scat._facecolors"""
        if self.num_dims == 2:
            self.scatt._offsets = self._offsets
            self.scatt._facecolors = self._facecolors
        else:
            self.scatt._offsets3d = self._offsets3d
            self.scatt._edgecolor3d = self._facecolors
            self.scatt._facecolor3d = self._facecolors
        self.scatt._sizes = self._sizes  # Still experimental

    def update_scatt_to_current_position(self):
        """Updates scatter data points. Not to be used unless you are Pedro."""
        if self.universe.num_dims == 2:
            self.scatt._offsets = [[self.position[0], self.position[1]]]
        else:
            data = [[self.position[i]] for i in range(3)]
            self.scatt._offsets3d = data

    def check_p_and_v(self):
        """In case there is any issue with inputs. The Parameters become 0"""
        types = type(self.init_v), type(self.init_p)
        if types[0] != np.ndarray:
            if types[0] == type(None):
                self.init_v = self.velocity = self.universe.zeroes
            try:
                self.init_v = self.velocity = np.array(self.init_v)
            except:
                self.init_v = self.velocity = self.universe.zeroes.copy()
        if types[1] != np.ndarray:
            if types[1] == type(None):
                self.init_p = self.position = self.universe.zeroes
            try:
                self.init_p = self.position = np.array(self.init_p)
            except:
                self.init_p = self.position = self.universe.zeroes.copy()
        if len(self.init_p) != self.num_dims:
            self.init_p = self.position = self.universe.zeroes
        if len(self.init_v) != self.num_dims:
            self.init_v = self.velocity = self.universe.zeroes

    def get_facecolor_array_from_v_data(self, key):
        """Returns the list of rgba's needed to give colors to object scatter"""
        if key == "None":
            return self._facecolors
        elif key == 'colorvx':
            array = self.v_data[:, 0]
        elif key == 'colorvy':
            array = self.v_data[:, 1]
        elif key == 'colorvz':
            speed = np.sqrt(np.sum(self.v_data**2, axis=1))
            array = speed if self.num_dims == 2 else self.v_data[:, 2]
        elif key == "speed":
            array = np.sqrt(np.sum(self.v_data**2, axis=1))
        cc_min = np.amin(array)
        cc_max = np.amax(array)
        cc = Normalize(cc_min, cc_max)
        map = ScalarMappable(cc, self.cmap)
        return map.to_rgba(array)

    def temporarily_hide(self):
        """Temporarily makes the scatter disappear"""
        if self.num_dims == 2:
            self.scatt._offsets = ([[None, None]])  # REmoves extra points
            self.scatt._facecolors = self._facecolors
        else:
            self.scatt._offsets3d = [[], [], []]
            self.scatt._edgecolor3d = self._facecolors
            self.scatt._facecolor3d = self._facecolors

    def update_ring_location(self):
        """Updates the location of rings around self"""
        if hasattr(self, 'x_ring'):
            if self.num_dims == 2:
                data = self.x_ring + self.position[0], self.y_ring + self.position[1]
                data = np.c_[data[0], data[1]]
                self.ring_scatt._offsets = data
            else:
                data = self.x_ring + self.position[0], self.y_ring + self.position[1],
                self.z_ring + self.position[2]
                data = [[data[i]] for i in range(3)]
                self.ring_scatt._offsets3d = data

    def make_ring(self):
        "Makes a ring around self of using multiple points and pyploy.scatter"
        r = self.radius*6
        r = r/1.6 if self.num_dims == 2 else r
        self.t_ring = t = np.arange(0, np.pi * 2.0, 0.01)
        self.x_ring = r * np.cos(t)
        self.y_ring = r * np.sin(t)
        y = r * np.sin(t)
        x = r * np.cos(t)
        x = x + self.position[0]
        y = y + self.position[1]
        if self.num_dims == 2:
            self.ring_location = np.array([self.x_ring, self.y_ring])
            self.ring_scatt = self.ax.scatter(x, y, s=r/40)
        else:
            self.z_ring = z = np.zeros(len(x))
            z = z + self.position[2]
            self.ring_scatt = self.ax.scatter(x, y, z, s=r/40)
            self.ring_location = np.array([self.x_ring, self.y_ring, self.z_ring])

    def get_other_objects(self):
        """Returns list with all planets that might
        be applying forces on the planet being observed"""
        index = self.universe.objects.index(self)
        lis = self.universe.objects.copy()
        lis.pop(index)
        self.other_objects = lis

    def calculate_net_acc(self):
        self.get_other_objects() if self.other_objects == [] else None
        self.net_acc = self.universe.zeroes  # Reset forces every cycle
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

    def update_velocity(self):
        self.velocity = self.velocity + self.net_acc*self.universe.dt

    def update_position(self):
        self.position = self.position+self.velocity*self.universe.dt

    def make_scatt(self):
        """Makes scatter plots that can have their _offsets replaced easily
        It is called when the object is first made."""
        marker = self.marker
        cmap = self.cmap
        color = self.color
        area = int(self.radius*self.rel_size if self.rel_size else self.radius)
        if self.num_dims == 2:
            self.scatt = self.universe.ax.scatter(self.position[0], self.position[1],
                                                  cmap=cmap, s=area, c=color)
            self._offsets = self.scatt.get_offsets()  # Get's initial point!
            self._offsets3d = None
            self._facecolors = self.scatt._facecolors
            self._edgecolors = self.scatt._edgecolors
        elif self.num_dims == 3:
            datas = self.position
            self.scatt = self.universe.ax.scatter(datas[0], datas[1], datas[2], s=area, alpha=0.95,
                                                  marker=marker, cmap=cmap, c=color)
            self._offsets = None
            self._offsets3d = self.scatt._offsets3d
            self._facecolors = self.scatt._facecolor3d
            self._edgecolors = self.scatt._edgecolor3d
        else:
            self.scatt = self.universe.ax.scatter([], [])
            print("Weird shit just happened")
        self._sizes = self.scatt._sizes.copy()  # For when the plots have to be redrawn
        self.universe.cmap['cmap'] = cmap
        self.universe.colorbar.set_cmap(cmap)
        self.universe.cmap["current_txt"].set_text(cmap)
        self.universe.fig.canvas.draw()
        self.universe.fig.canvas.flush_events()


class Large_object(Object):
    """This class has better support for planetary motion"""
    instances = []

    def __init__(self, orbit=None, orbit_rand=False, *args, **kwargs):
        Object.__init__(self, *args, **kwargs)
        self.orbit = orbit  # Object that this large object will orbit
        # Orbit rand stands for random orbit
        self.check_orbit(orbit_rand)  # Ensure orbit is stabilished
        self.make_scatt()

    def check_orbit(self, orbit_rand):
        # flexibility with inputs
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
            if r_ < (self.radius+self.orbit.radius)*1.5:  # Checks for Large objects on same point
                self.init_p = np.zeros(self.num_dims)  # Sets position that eases calculations
                min = limit/5
                r_ = np.random.randint(min, limit)  # New distance
            v_ideal = np.sqrt(g*self.orbit.mass/r_)
            self.init_v = np.zeros(self.num_dims)
            self.init_p = np.zeros(self.num_dims)
            self.init_v[0] = v_ideal
            print(self.init_v, "INit v", v_ideal)
            self.init_p[0] = r_  # Assigns random distance to close objects along x axis
            orbit_rand = "true" if orbit_rand == True else "False" if orbit_rand == False else orbit_rand
            if not flex[orbit_rand.lower()]:  # The input may be weird
                if self.num_dims == 2:
                    self.init_p = self.init_p[::-1]  # Ensures perp velocity
                elif self.num_dims == 3:
                    self.init_p[0] = 0
                    self.init_p[1] = r_
            else:
                v = self.init_v[self.init_v != 0][0]/np.sqrt(2)  # More components
                self.init_v[0] = v
                self.init_v[1] = v
                while np.where(self.init_p != 0)[0][0] not in np.where(self.init_v == 0)[0]:
                    for x in range(3):
                        self.init_v[x] = self.init_v[x]*np.random.choice([-1, 1])  # Changes direction
                        self.init_p[x] = self.init_p[x]*np.random.choice([-1, 1])  # Changes direction
                    np.random.shuffle(self.init_p)
                    np.random.shuffle(self.init_v)
            self.init_v = self.init_v + self.orbit.init_v
            self.init_p = self.init_p + self.orbit.init_p
            self.velocity = self.init_v.copy()
            self.position = self.init_p.copy()
        print(self.position, self.velocity, f"are the init_v and p of {self.name}")
        self.universe.fig.canvas.draw()
        self.universe.fig.canvas.flush_events()


class Planet(Large_object):  # adapt class to work with Physics
    instances = []

    def __init__(self, category="planet", name='planet',
                 rel_size=2,  *args, **kwargs):
        super().__init__(category=category, name="planet",
                         rel_size=rel_size, *args, **kwargs)


class Sun(Large_object):
    instances = []

    def __init__(self, category="sun", name="sun", color="yellow",
                 rel_size=2, *args, **kwargs):
        super().__init__(category=category, name=name, color=color, *args, **kwargs)


class Moon(Large_object):
    """Creates an object orbiting another object"""
    instances = []

    def __init__(self, orbit=None, rad_orb=10, resize=False, category="moon",
                 color="white", name="moon", **kwargs):
        if orbit:
            kwargs["universe"] = orbit.universe
            self.rad_orb = rad_orb
            self.orbit = orbit
            self.color = color
            super().__init__(category=category, name=name,
                             color=color, orbit=self.orbit, **kwargs)
            self.check_orbit2(orbit)
        else:
            print("This object will not behave as a moon.")

    def print_v(self):
        v = np.sqrt(sum(self.velocity**2))
        print(v)

    def check_orbit(self, other):
        pass  # Overrides the orginal

    def check_orbit2(self, orbit):
        """sets planet's orbit around it's planet!
        This is done by changing their initial position and velocity.
        But it keelps the distance from the planet."""
        d = self.rad_orb
        g = self.universe.constants["G"]
        v_ideal = np.sqrt(g*orbit.mass/d)
        r = self.orbit.init_p - self.init_p  # distance vector
        r_ = np.sqrt(sum(r**2))
        if r_ < (self.radius+self.orbit.radius)*1.5:  # Checks for Large objects on same point
            self.init_p = np.zeros(self.num_dims)  # Sets position that eases calculations
            min = limit/5
            r_ = np.random.randint(min, limit)
            d = r_
        if self.universe.num_dims == 3:
            self.position = np.array([0, d, 0]) + orbit.position
            self.velocity = np.array([v_ideal, 0, 0]) + orbit.velocity
        else:
            self.position = np.array([0, d]) + orbit.position
            self.velocity = -1*np.array([v_ideal, 0]) + orbit.velocity
        self.init_p = self.position.copy()
        self.init_v = self.velocity.copy()
        
universe = Physics(num_dims=3, u_size=2000, show_time=True)
planet = Sun(universe=universe, density=1e14, ring=False, radius=40, cmap="summer")
# planet2 = Large_object(universe=universe, init_p=(-500, 0, 0), orbit=planet, orbit_rand=True)
# planet3 = Large_object(universe=universe, init_p=(-300, 0, 0), orbit=planet, orbit_rand=True)
for x in range(3):
    d = Planet(universe=universe, orbit=planet, orbit_rand=False, rel_size=2, cmap="spring",
               radius=10, density=1e12)
    c = Moon(orbit=d, orbit_rand=False, rel_size=1, cmap="summer", radius=2, rad_orb=20)
plt.show()
