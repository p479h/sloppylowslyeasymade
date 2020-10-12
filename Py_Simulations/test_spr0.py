import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import time

class Physics:
    """
    Same as physics but trying new make plot style"""
    def __init__(self,page, dt=0.01, u_size = 20,
        show_force = True, show_energy=True, *args, **kwargs):
        self.u_size = u_size
        self.dt = dt
        self.t = 0
        self.show_energy = show_energy
        self.show_force = show_force
        self.page = page
        page.universe = self
        self.artists = []
        self.objects={}
        self.make_plot()

    def make_plot(self):
        page = self.page
        with plt.xkcd():
            fig = plt.figure(figsize=(6/1.2, 4/1.2))
        FCTKA = mpl.backends.backend_tkagg.FigureCanvasTkAgg
        self.canvas = FCTKA(fig, page.main_frame)
        page.canvas = self.canvas
        canvas = self.canvas
        page.fig = fig
        self.canvas.get_tk_widget().grid(
            row = 0, column=0, rowspan = 24, columnspan = 40,
            sticky = "NSEW")
        self.canvas.get_tk_widget().config(relief = "ridge", border = 1)
        with plt.xkcd():
            ax = fig.add_subplot(111)
        page.ax = ax
        self.fig, self.ax = fig, ax
        canvas.draw()
        s = self.u_size
        lim = -1*self.u_size, self.u_size
        ax.set(xlim = lim, ylim = lim)
        ax.set_yticklabels([])
        canvas.draw()
        ax.set_xticklabels([-s, -s/2, 0, s/2, s],size=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.yaxis.set_ticks([])
        canvas.draw()
        ax.set_position([0.05, 0.155, 0.55, 0.8])
        ax.set_xlabel(r"$x$/$m$", size=10)
        ax.text(0.5, 0.9, "Touch me", ha="center",
            transform = ax.transAxes, fontdict = {
                "family":"Consolas", "size": "19"})
        canvas.draw()

        with plt.xkcd():
            self.energy_ax = self.fig.add_axes([0.67, 0.6, 0.3, 0.3])
            page.energy_ax = self.energy_ax
        self.energy_ax.yaxis.set_ticks([])
        self.energy_ax.xaxis.set_ticks([])
        self.energy_ax.spines['top'].set_visible(False)
        self.energy_ax.spines['right'].set_visible(False)
        self.energy_ax.text(0.03, 1, "Energies", ha="left",
            fontdict = {"family":"Consolas","size":"10"},
            transform = self.energy_ax.transAxes)
        canvas.draw()

        self.energy_ax.set_xlabel(
            r"$t$/s", fontdict = {"family":"Consolas","size": "7"})

        with plt.xkcd():
            self.force_ax = self.fig.add_axes([0.67, 0.15, 0.3, 0.3])
            page.force_ax = self.force_ax
        self.force_ax.yaxis.set_ticks([])
        self.force_ax.xaxis.set_ticks([])
        self.force_ax.spines['top'].set_visible(False)
        self.force_ax.spines['right'].set_visible(False)
        self.force_ax.text(0.06, 1, "Force", ha="left",
            fontdict = {"family":"Consolas","size":"10"},
            transform = self.force_ax.transAxes)
        canvas.draw()

        self.force_ax.set_xlabel(
            r"$t$/s", fontdict = { "family":"Consolas", "size": "7"})

        self.canvas = fig.canvas
        t_label = ax.text(
            0.05, .02, "t / s:", fontdict = {"family":"Italics","size":"10"},
                                            transform = ax.transAxes)
        self.canvas.draw()
        self.canvas.flush_events()
        self.bg = self.canvas.copy_from_bbox(ax.bbox)
        self.energy_bg = self.canvas.copy_from_bbox(self.energy_ax.bbox)
        self.force_bg = self.canvas.copy_from_bbox(self.force_ax.bbox)
        self.t_text = ax.text(0.17, 0.02, "",
            fontdict = {"family":"Italics","size":"10"},
            transform = ax.transAxes)
        self.artists.append(self.t_text)
        canvas.draw()


    @staticmethod
    def normalize(self, min, max, value):
        normalizer = mpl.colors.Normalize(min, max)
        return normalizer(value)

    @staticmethod
    def translate_transforms(artist):
        ax = artist.axes
        axis_to_data = ax.transAxes + ax.transData.inverted()
        points_data = axis_to_data.transform(artist._path._vertices)
        artist.set_transform(ax.transData)
        artist._path._vertices = points_data


    def connect_canvas(self, *objects):
        """Makes canvas responsive to dragging artists"""
        spring = self.objects['spring']
        box = self.objects['box']
        self.lock = False
        def clicked(event):
            self.running = False
            self.canvas.draw()
            if not hasattr(self, "lock"):
                self.lock = False
            if (self.lock or event.inaxes!=self.ax): return
            self.lock = True
            self.x0, self.y0 = event.xdata, event.ydata
            self.t = 0
            tl, tr = self.t-60*self.dt, self.t+10*self.dt
            self.force_ax.set(xlim = (tl, tr))
            self.energy_ax.set(xlim = (tl, tr))

            for patch in self.artists:
                try:
                    patch.init_verts = patch._path._vertices.copy()
                except :
                    None

        def motion(event):
            if self.lock and event.inaxes:
                self.click_flag = True
                self.canvas.restore_region(self.force_bg)
                self.canvas.restore_region(self.energy_bg)
                self.canvas.restore_region(self.bg)
                spring.update_disp()
                spring.calc_force()
                spring.update_ep()
                ep = np.sqrt(np.sum(spring.ep**2))
                f = np.sqrt(np.sum(spring.force**2))
                box.force_plot.set_offsets([self.t, f])
                self.force_ax.draw_artist(box.force_plot)

                box.forcex_plot.set_offsets([self.t, spring.force[0]])
                self.force_ax.draw_artist(box.forcex_plot)

                box.forcey_plot.set_offsets([self.t, spring.force[1]])
                self.force_ax.draw_artist(box.forcey_plot)

                box.ep_plot.set_offsets([self.t, ep])
                self.energy_ax.draw_artist(box.ep_plot)
                dx, dy = event.xdata-self.x0, event.ydata-self.y0
                for object in objects:
                    object.translate(dx, dy)
                self.canvas.blit()
                self.canvas.flush_events()

        def release(event):
            box.ek_data = []
            box.ep_data = []
            box.sum_data = []
            box.force_data = []
            box.forcex_data = []
            box.forcey_data = []
            self.lock = False
            self.running = True if self.click_flag else False
            self.click_flag = False
            box.simulate()
            self.click_flag = False
            box.v=np.zeros(2)
            for a in self.artists:
                a.set_animated(False)
            try:
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
            except:
                None

        def resized(event):
            self.reset_bgs()


        self.canvas.mpl_connect("button_press_event", clicked)
        self.canvas.mpl_connect('motion_notify_event', motion)
        self.canvas.mpl_connect('button_release_event', release)
        self.canvas.mpl_connect("resize_event", resized)

    def reset_bgs(self):
        for a in self.artists:
            a.set_animated(True)
        self.canvas.draw()
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        self.energy_bg = self.canvas.copy_from_bbox(self.energy_ax.bbox)
        self.force_bg = self.canvas.copy_from_bbox(self.force_ax.bbox)
        for a in self.artists:
            a.set_animated(False)
        self.canvas.draw()
        self.canvas.flush_events()


class Spring:
    """
    This is the spring of the hook's law thingy
    """
    def __init__(self,n=13,universe = None,
        k = 1, *args, **kwargs):
        self.n = n
        self.k = k
        self.universe = universe
        universe.objects["spring"] = self
        self.make_plot()
        # try:
        self.update_energy_ax()
        # except :
        #     print("UNIVERSE MISSING ENERGY AX")
        # try:
        self.update_force_ax()
        # except :
        #     print("UNIVERSE MISSING ENERGY AX")

    def update_energy_ax(self):
        """Sets appropriate limits to energy_ax"""
        ax = self.universe.energy_ax
        max = self.calculate_max_EP()
        ax.set_ylim(-0.04*max, max*1.3)
        ax.set_xlim(0, 4)
        ax.yaxis.set_ticks([0, max])
        ax.tick_params(axis = "y", labelsize=8)

    def update_force_ax(self):
        max = self.calculate_max_force()
        ax = self.universe.force_ax
        ax.set_ylim(-0.04*max,max)
        ax.set_xlim(0,4)
        ax.yaxis.set_ticks([-max*1.3,0, max*1.3])
        ax.tick_params(axis = "y", labelsize=8)
        line = ax.axhline(0.5, ls = "--", alpha = 0.4, color="black")
        #self.universe.artists.append(line)

    def calculate_max_force(self):
        max = abs(self.ax.get_ylim()[1])
        return self.k*max

    def reset_position(self):
        self.plot._path._vertices = self.restart_verts.copy()

    def make_plot(self):
        u = self.universe
        self.fig = u.fig
        self.ax = u.ax
        self.canvas = u.canvas
        n = self.n

        init_x = np.linspace(0, 0.5, n)
        init_spr = (np.ones(n-3)*0.35).tolist()
        init_spr2 = (np.ones(n-3)*0.85).tolist()
        mixed = [init_spr[i] if i%2==0 else init_spr2[i] for i in range(n-4)]
        init_y = np.array(([0.5, 0.5]+mixed+[0.5, 0.5]))
        codes = [1]+[3 for x in range(n-2)]+[2]
        path = mpl.path.Path(np.c_[init_x, init_y],codes)
        self.plot = mpl.patches.PathPatch(
            path, color = "black", fill=False, lw=2,
            capstyle="round", joinstyle="round")
        self.canvas.draw()

        u.artists.append(self.plot)
        self.ax.add_patch(self.plot)
        u.__class__.translate_transforms(self.plot)
        self.plot.init_verts = p =self.plot._path._vertices.copy()
        self.x0, self.x1, self.y0, self.y1 = p[0, 0], p[-1,0], p[0, 1], p[-1, 1]
        self.lenx = self.x1 - self.x0
        self.leny = self.y1 - self.y0

    def translate(self, dx, dy):
        """This function makes a single translation that will
            depend on the object.plot's init_verts.
            For cummulative translations, init_verts must also be updated."""
        self.plot._path._vertices[:, 0]=self.plot.init_verts[:, 0]+np.linspace(0,dx, self.n)
        self.plot._path._vertices[:, 1]=self.plot.init_verts[:, 1]+np.linspace(0,dy, self.n)
        self.ax.draw_artist(self.plot)

    def update_disp(self):
        """
        Calculates the displacement, as a vector,
        of the spring, relative to it's initial position.
        It uses the front of the spring as reference.
        Instead of returning the vectors, those will be
        stored as self.ry and self.rx.
        Antention to the position of the elements.
        There will be no need to use negative signs as
        the vectors already point to the most stable spring length.
        """
        self.ry = self.y1 - self.plot._path._vertices[-1, 1]
        self.rx = self.x1 - self.plot._path._vertices[-1, 0]

    def calc_force(self):
        self.ry = self.y1 - self.plot._path._vertices[-1, 1]
        self.rx = self.x1 - self.plot._path._vertices[-1, 0]
        self.force = np.array([self.k*self.rx, self.k*self.ry])

    def calculate_max_EP(self):
        max = abs(self.ax.get_ylim()[1])
        return 1/2*self.k*max**2

    def update_ep(self):
        self.ep = 1/2*self.k*(self.rx**2 + self.ry**2)


class Block:
    def __init__(self, spring, mass = 1, marker = "s",
        universe = False, *args, **kwargs):
        self.mass = mass
        self.marker = marker
        self.spring = spring
        self.universe = universe
        universe.objects["box"] = self
        spring.box = self
        self.v = np.zeros(2)
        self.patches = []
        self.force_data = []
        self.forcex_data = []
        self.forcey_data = []
        self.ek_data = []
        self.sum_data = []
        self.ep_data = []
        self.make_plot()

    def make_plot(self):
        u = self.universe
        ax, fig, canvas = u.ax, u.fig, u.canvas
        self.ax, self.fig, self.canvas = ax, fig, canvas
        marker_path = mpl.markers.MarkerStyle("s").get_path()
        verts = np.array(marker_path._vertices)*0.3#+[0.5, 0.35]
        marker_path = mpl.path.Path(verts, marker_path.codes)
        self.plot = mpl.patches.PathPatch(
            marker_path, color = "yellow", lw=2,
            capstyle="round", joinstyle="round")
        canvas.draw()
        self.plot.set_edgecolor("black")
        u.artists.append(self.plot)
        self.patches.append(self.plot)
        ax.add_patch(self.plot)
        translate =u.__class__.translate_transforms
        translate(self.plot)
        self.plot.init_verts = self.plot._path._vertices.copy()
        canvas.draw()

        eyes = [[0.075, 0.2],[0.215, 0.2]]
        eye_path = mpl.path.Path.unit_circle()
        eye_path = mpl.path.Path(np.array(eye_path._vertices), eye_path.codes)
        eye_path2 = mpl.path.Path(np.array(eye_path._vertices), eye_path.codes)
        paths = [eye_path, eye_path2]
        self.body_parts = {}
        for index, eye in enumerate(eyes):
            patch = mpl.patches.PathPatch(paths[index], zorder=5, color = "black")
            patch._path._vertices*=0.04
            patch._path._vertices+=eye
            ax.add_patch(patch)
            translate(patch)
            u.artists.append(patch)
            self.patches.append(patch)
            patch.init_verts = patch._path._vertices.copy()
            if index == 0:
                self.body_parts['left eye'] = patch
            else:
                self.body_parts['right eye'] = patch

        mouth_verts = np.array([[0.080, 0.09],
                                [0.080, 0.06],
                                [0.135, 0.06],
                                [0.19, 0.06],
                                [0.19, 0.09]])+[0.009, 0]

        mouth_codes = (1, 3, 3, 3, 4)
        path = mpl.path.Path(mouth_verts, mouth_codes)
        patch = mpl.patches.PathPatch(path, lw=2, transform = ax.transAxes,
                                        fill = False, color = "blue",
                                        capstyle="round", joinstyle="round",)
        patch.set_edgecolor("black")
        ax.add_patch(patch)
        self.mouth = patch
        translate(patch)
        self.patches.append(self.mouth)
        u.artists.append(self.mouth)
        patch.init_verts = patch._path._vertices.copy()
        self.align_with_spring()

        self.ek_plot = u.energy_ax.scatter(
            [], [], label = r"Box $EK$ / $J$", s=10, alpha=0.6, zorder = 5)
        self.ep_plot = u.energy_ax.scatter(
            [], [], label = r"Spring $EP$ / $J$", s=10, alpha=0.6, zorder=4)
        self.sum_plot = u.energy_ax.scatter(
            [], [], label = r"Total $E$ / $J$", s=10, alpha = 0.6,
            c = 'cyan', edgecolor = "lightblue", zorder=3)

        self.force_plot = u.force_ax.scatter(
            [], [], label = r"Total Force / $N$", s=10,
            cmap = "viridis", alpha = 0.6, c = "red")

        self.forcex_plot = u.force_ax.scatter(
            [], [], label = r"Force x / $N$", s=10,
            cmap = "viridis", alpha = 0.6, c = "cornflowerblue")

        self.forcey_plot = u.force_ax.scatter(
            [], [], label = r"Force y / $N$", s=10,
            cmap = "viridis", alpha = 0.6, c = "magenta")

        a = u.energy_ax.legend(fontsize = 8,prop={'size':7},loc = 'upper right',
            labelspacing=0.04,)

        b = u.force_ax.legend(fontsize = 8,prop={'size':7},loc = 'upper right',
            labelspacing=0.04)


        self.canvas.draw()

        aa = a.get_bbox_to_anchor().inverse_transformed(ax.transAxes)
        bb = b.get_bbox_to_anchor().inverse_transformed(ax.transAxes)

        dx, dy = 0.05, 0.1
        aa.x0+=dx
        aa.x1+=dx
        bb.x1+=dx
        bb.x0+=dx

        aa.y0+=dy
        aa.y1+=dy
        bb.y0+=dy
        bb.y1+=dy

        a.set_bbox_to_anchor(aa, transform = ax.transAxes)
        b.set_bbox_to_anchor(bb, transform = ax.transAxes)

        for thing in (self.ek_plot,
                      self.ep_plot,
                      self.sum_plot,
                      self.force_plot,
                      self.forcex_plot,
                      self.forcey_plot,):
            u.artists.append(thing)

        self.spring.restart_verts = self.spring.plot._path._vertices.copy()
        self.restart_verts = self.plot._path._vertices.copy()
        self.mouth_restart_verts = self.mouth._path._vertices.copy()
        self.leye_restart_verts = self.body_parts['left eye']._path._vertices.copy()
        self.reye_restart_verts = self.body_parts['right eye']._path._vertices.copy()

    def reset_position(self):
        self.plot._path._vertices = self.restart_verts.copy()
        self.mouth._path._vertices = self.mouth_restart_verts.copy()
        self.body_parts['left eye']._path._vertices = self.leye_restart_verts.copy()
        self.body_parts['right eye']._path._vertices = self.reye_restart_verts.copy()


    def translate(self, dx, dy):
        """Translates the Yellow box, eyes and mouth"""
        for patch in self.patches:
            patch._path._vertices=patch.init_verts+[dx, dy]
            self.ax.draw_artist(patch)

    def align_with_spring(self):
        dx = self.spring.x1-self.spring.x0
        dy = self.spring.y0-(self.plot.init_verts[3, 1]+self.plot.init_verts[4, 1])/2
        self.translate(dx, dy)

    def calc_acc(self):
        self.spring.calc_force()
        self.acc = self.spring.force/self.mass

    def calc_disp(self):
        """Returns displacement and updates velocity"""
        self.v += self.acc*self.universe.dt
        return self.v*self.universe.dt

    def cycle(self):
        for patch in self.patches:
            patch.init_verts = patch._path._vertices.copy()
        self.spring.plot.init_verts = self.spring.plot._path._vertices.copy()
        self.canvas.restore_region(self.universe.bg)
        self.calc_acc()
        tl, tr = self.universe.t-60*self.universe.dt, self.universe.t+10*self.universe.dt
        if self.universe.show_energy:
            self.canvas.restore_region(self.universe.energy_bg)
            self.canvas.restore_region(self.universe.force_bg)
            self.calc_ek()
            self.calc_ep()
            self.calc_sum()
            self.universe.energy_ax.set(xlim = (tl, tr))
        if self.universe.show_force:
            self.calc_forcex()
            self.calc_forcey()
            self.calc_force()
            self.universe.force_ax.set(xlim = (tl, tr))
        disp = self.calc_disp()
        self.translate(*disp)
        self.spring.translate(*disp)
        self.universe.t+=self.universe.dt
        self.universe.t_text.set_text(f"{round(self.universe.t, 1)}")
        self.ax.draw_artist(self.universe.t_text)

    def calc_forcex(self):
        f = self.spring.force[0]
        self.forcex_data.append([self.universe.t,f])
        self.forcex_plot.set_offsets(self.forcex_data)
        self.universe.force_ax.draw_artist(self.forcex_plot)

    def calc_forcey(self):
        f = self.spring.force[1]
        self.forcey_data.append([self.universe.t,f])
        self.forcey_plot.set_offsets(self.forcey_data)
        self.universe.force_ax.draw_artist(self.forcey_plot)

    def calc_ek(self):
        """
        calculates the Kinetic energy of mass at present moment"""
        self.ek = 1/2*self.mass*np.sum(self.v**2)
        self.ek_data.append([self.universe.t, self.ek])
        if len(self.ek_data)>65:
            self.ek_data.pop(0)
        self.ek_plot.set_offsets(self.ek_data)
        self.universe.energy_ax.draw_artist(self.ek_plot)

    def calc_ep(self):
        self.spring.update_ep()
        self.ep_data.append([self.universe.t, self.spring.ep])
        if len(self.ep_data)>65:
            self.ep_data.pop(0)
        self.ep_plot.set_offsets(self.ep_data)
        self.universe.energy_ax.draw_artist(self.ep_plot)

    def calc_sum(self):
        total = self.ek+self.spring.ep
        self.sum_data.append([self.universe.t, total])
        if len(self.sum_data)>65:
            self.sum_data.pop(0)
        self.sum_plot.set_offsets(self.sum_data)
        self.universe.energy_ax.draw_artist(self.sum_plot)

    def calc_force(self):
        f = np.sqrt(np.sum(self.spring.force**2))
        self.force_data.append([self.universe.t,f])
        if len(self.force_data)>65:
            self.force_data.pop(0)
            self.forcey_data.pop(0)
            self.forcex_data.pop(0)
        self.force_plot.set_offsets(self.force_data)
        self.universe.force_ax.draw_artist(self.force_plot)


    def simulate(self):
        if not hasattr(self.universe, "running"):
            print("Here")
            self.universe.running = True
        i=0
        s = time.time()
        try:
            while self.universe.running:
                i+=1
                self.cycle()
                self.canvas.blit()
                self.canvas.flush_events()
        except:
            print("PROBLEM WITTH RUNTIME.")
            print(i/(time.time()-s))
            print("Was the relative efficiency.")
            print("Considered bad when lower than 200")
            print("Good when above 300")




def make_plot(page):
    universe = Physics(page, dt = 0.1, show_energy = True, show_force=True)
    page.universe = universe
    spring = Spring(universe = universe, k=1, n=17)
    square = Block(universe = universe, spring = spring, mass=1)
    universe.connect_canvas(square, spring)
