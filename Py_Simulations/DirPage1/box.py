import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from itertools import product, combinations
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mpl_toolkits.mplot3d.art3d as art3d

    
mpl.style.use("fast")

def make_box_interactive(self):
    if hasattr(self, "canvas"): return
    self.fig = plt.figure(figsize=(1, 1))
    parent_color = self.master["background"]
    self.canvas = FigureCanvasTkAgg(self.fig, self.box_labin)
    self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                    fill=tk.BOTH,
                                    expand=True,
                                    )
    self.canvas.get_tk_widget().config(
        width=160, height=155, background = parent_color)
    #self.box_labin.update()
    fig  = self.fig
    fig.patch.set_alpha(0)
    canvas = fig.canvas
    ax = fig.add_subplot(projection = "3d")
    ax.patch.set_alpha(0)
    self.ax = ax
    ax.view_init(19, -62)
    a = 0.96
    xl, yl, zl = (-a, a), (-a, a), (-a, a)
    ax.set(xlim=xl, ylim = yl, zlim = zl)
    ax.set_position([0, 0, 1, 1])
    children = []
    ax.axis("off")
    a = 1
    verts = [[a, a], [-a, a], [-a,-a], [a, -a]]
    plane1 =mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    plane2 =mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    plane3 = mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    plane4 =mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    plane5 =mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    plane6 = mpl.patches.Polygon(verts, color = "black", alpha=1, fill=True, zorder=-6)
    [ax.add_patch(patch) for patch in (plane1, plane2, plane3,
                                       plane4, plane5, plane6)]
    art3d.pathpatch_2d_to_3d(plane1, z=-1, zdir="x")
    art3d.pathpatch_2d_to_3d(plane2, z=1, zdir="y")
    art3d.pathpatch_2d_to_3d(plane3, z=-1, zdir="z")
    art3d.pathpatch_2d_to_3d(plane4, z=1, zdir="x")
    art3d.pathpatch_2d_to_3d(plane5, z=-1, zdir="y")
    art3d.pathpatch_2d_to_3d(plane6, z=1, zdir="z")

    
    #Now making cube and stars
    r = [-1, 1]
    lines = []
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            line,=ax.plot(*zip(s, e), color="white", alpha = 0.8,
                          zorder=9)
            if s[1] == e[1] == 1 or s[0]==e[0]==1:
                line.set_zorder(50)
            lines.append(line)
            canvas.draw()
            canvas.flush_events()

    x, y, z = np.random.rand(3, 100)
    cstring = ("blue ""red "+"white "*10).split()
    cstring = [np.random.choice(cstring) for i in range(100)]
    x[::3]*=-1; y[::2]*=-1; z[::4]*=-1
    for i in range(100):
        line, = ax.plot([x[i]], [y[i]], [z[i]], marker = "*",
                        markersize=np.random.rand(),
                        color=cstring[i],
                        zorder=11)
        lines.append(line)
        if i%10==0:
            canvas.draw()
            canvas.flush_events()


    #Now we make a small solar system
    sunline, = ax.plot(*[[0], [0], [0]], markersize=4, color="yellow",
                      marker="o",zorder=11)
    lines.append(sunline)
    canvas.draw()
    canvas.flush_events()

    t = np.linspace(0, 2*3.1415, 100)
    r1 = 0.45
    r2 = 0.55
    r3 = 0.65
    r4 = 0.75
    x = np.cos(t)
    y = np.sin(t)
    z = np.zeros(len(t))

    for r in (r1, r2, r3, r4):
        line, = ax.plot(x*r, y*r, z, lw=1, color="cornflowerblue",
                        zorder=11)
        lines.append(line)
        linepos = np.array(list(zip(x*r, y*r, z)))[np.random.randint(0,len(x))].reshape((3, 1))
        line, = ax.plot(*linepos, marker="o",
                       markersize=np.random.choice([d+0.1 for d in range(4)]),
                        zorder=11,
                        )
        lines.append(line)
        canvas.draw()
        canvas.flush_events()
    


