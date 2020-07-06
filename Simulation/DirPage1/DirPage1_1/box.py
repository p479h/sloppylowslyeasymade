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
        width=60, height=140, background = parent_color)
    self.box_labin.update()
    fig  = self.fig
    fig.patch.set_alpha(0)
    canvas = fig.canvas
    ax = fig.add_subplot(projection = "3d",)
    self.ax = ax
    ax.view_init(19, -62)
    ax.set_alpha(0)
    a = 0.96
    xl, yl, zl = (-a, a), (-a, a), (-a, a)
    ax.set(xlim=xl, ylim = yl, zlim = zl)
    ax.patch._alpha=0.0
    ax.set_position([0.1, 0, 0.8, 1])
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
    


    r = [-1, 1]
    lines = []
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            line,=ax.plot(*zip(s, e), color="white", alpha = 0.8,
                          zorder=11, lw=0.5)
            lines.append(line)
            canvas.draw()
            canvas.flush_events()

    #Now making cube and stars
    r = [-1, 1]
    lines = []

    x, y, z = np.random.rand(3, 30)
    cstring = ("blue ""red "+"white "*10).split()
    cstring = [np.random.choice(cstring) for i in range(20)]
    x[::3]*=-1; y[::2]*=-1; z[::4]*=-1
    for i in range(20):
        line, = ax.plot([x[i]], [y[i]], [z[i]], marker = "*",
                        markersize=np.random.rand(),
                        color=cstring[i],
                        zorder=10)
        lines.append(line)
        if i%5==0:
            canvas.draw()
            canvas.flush_events()
    m = self.marker_drop.get()
    sunline, = ax.plot(*[[0], [0], [0]], markersize=0.01, color="blue",
                      marker=m,zorder=10, animated = True, alpha=0.97)
    self.sunline = sunline

    t = np.linspace(0, 2*3.1415, 50)
    x_ = np.cos(t)
    y_ = np.sin(t)
    z_ = np.zeros(len(t))
    fig.canvas.draw()
    bg = fig.canvas.copy_from_bbox(ax.bbox)

    rs = np.linspace(0.45,0.6, 10)
    self.rings = []
    lines = []
    for r in rs:
        lines.append(
            ax.plot([0],[0],[0],
            animated = True,
        color="white", zorder=10)[0])
        self.rings.append(lines[-1])
        lines[-1].set_visible(True if self.ring_val.get() else False)
        

    for x in range(30):
        fig.canvas.restore_region(bg)
        sunline._markersize = x/2
        ax.draw_artist(sunline)
        fig.canvas.blit()
        
    for x in range(50):
        for i, line in enumerate(lines):
            line.set_data(rs[i]*x_[:x+1],rs[i]*y_[:x+1])
            line.set_3d_properties(rs[i]*z_[:x+1])
            ax.draw_artist(line)
        if x%3==0:
            ax.draw_artist(sunline)
            fig.canvas.blit()
            fig.canvas.flush_events()
    sunline.set_animated(False)
    [line.set_animated(False) for line in lines]
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    


