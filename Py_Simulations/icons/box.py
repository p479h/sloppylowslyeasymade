from PIL import Image, ImageTk
try:
    box_icon = Image.open(r"icons\box_icon.png")
except:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    import tkinter as tk
    from matplotlib.colors import to_rgba
    from itertools import product, combinations
    import mpl_toolkits.mplot3d.art3d as art3d

        
    mpl.style.use("fast")

    fig = plt.figure(figsize = (6, 6))
    bgc  = to_rgba("#F0F0F0")
    fig.patch.set_facecolor("black")
    fig.patch._alpha = 0.0
    canvas = fig.canvas
    canvas.draw()
    ax = fig.add_subplot(projection = "3d",
                         facecolor = bgc,)
    ax.view_init(19, -62)
    a = 0.96
    xl, yl, zl = (-a, a), (-a, a), (-a, a)
    ax.set(xlim=xl, ylim = yl, zlim = zl)
    ax.patch._alpha=0.0
    ax.set_position([0, 0, 1, 1])
    children = []
    for child in ax.get_children():
        if child not in (ax.w_zaxis.pane, ax.w_xaxis.pane, ax.w_yaxis.pane):
            children.append(child)
            
    for pane in (ax.w_zaxis.pane, ax.w_xaxis.pane, ax.w_yaxis.pane):
        children+=pane.get_children()

    for pane in (ax.w_zaxis, ax.w_xaxis, ax.w_yaxis):
        children+=pane.get_children()
        
    for child in children:
        try: child._visible = False
        except: None
    ax.grid(False)

    for pane in (ax.w_zaxis.pane, ax.w_xaxis.pane, ax.w_yaxis.pane):
        pane._facecolor = (0., 0., 0., 1.)
        pane._alpha = 1


    #Now making cube and stars
    r = [-1, 1]
    lines = []
    for s, e in combinations(np.array(list(product(r, r, r))), 2):
        if np.sum(np.abs(s-e)) == r[1]-r[0]:
            line,=ax.plot(*zip(s, e), color="white", alpha = 0.8,
                          zorder=3)
            lines.append(line)

    x, y, z = np.random.rand(3, 100)
    cstring = ("blue ""red "+"white "*10).split()
    cstring = [np.random.choice(cstring) for i in range(100)]
    x[::3]*=-1; y[::2]*=-1; z[::4]*=-1
    for i in range(100):
        line, = ax.plot([x[i]], [y[i]], [z[i]], marker = "*",
                        markersize=np.random.rand()*9,
                        color=cstring[i], alpha=0.95,
                        zorder=2)
        lines.append(line)
        
                        

    lines.append(ax.plot([-1, 1.2],[-1.2, -1.2],[-1, -1], lw=2, color="blue",
            )[0])
    lines.append(ax.plot([1.2, 1.2],[-1.2, 1],[-1, -1], lw=2, color="green",
            )[0])
    lines.append(ax.plot([1.2, 1.2],[1, 1],[-1, 1], lw=2, color="red",
            )[0])


    #Now we make a small solar system
    sunline, = ax.plot(*[[0], [0], [0]], markersize=19, color="yellow",
                      marker="o",zorder=2, alpha=1.)
    lines.append(sunline)

    t = np.linspace(0, 2*3.1415, 100)
    r1 = 0.45
    r2 = 0.55
    r3 = 0.65
    r4 = 0.75
    x = np.cos(t)
    y = np.sin(t)
    z = np.zeros(len(t))

    for r in (r1, r2, r3, r4):
        line, = ax.plot(x*r, y*r, z, lw=2.5, color="cornflowerblue",
                        zorder=-2)
        lines.append(line)
        linepos = np.array(list(zip(x*r, y*r, z)))[np.random.randint(0,len(x))].reshape((3, 1))
        line, = ax.plot(*linepos, marker="o",
                       markersize=np.random.choice([d+4 for d in range(5)]),
                        zorder=2,
                        )
        lines.append(line)


    t=ax.text(-1.4, -1, -1.87, "Universe side length", "x",
            fontdict={"color":"black",
                      "fontfamily":"Consolas",
                      "fontsize":"23",
                      "stretch": "ultra-expanded",
                      "weight":"800"}, )

    flag = True
    flag2 = False
    def rotation_(event):
        t.remove()
        global flag
        global flag2
        i=0
        if flag2:
            flag = False
        flag2 = True
        
        while flag:
            i+=1
            ax.view_init(20, i)
            canvas.draw()
            canvas.flush_events()

    canvas.mpl_connect("button_press_event", rotation_) if __name__ == "__main__" else None
        
        

    canvas.draw()
    #t.remove() if __name__ == "__main__" else None
    plt.show() if __name__ == "__main__" else None
    size=2000,2000
    a = fig.canvas.tostring_argb()
    a=np.frombuffer(
        fig.canvas.tostring_argb(),
        dtype = np.uint8).reshape(*canvas.get_width_height(), 4)
    plt.close("all")
    img  = Image.fromarray(a)
    a,r,g,b = img.split()
    img = Image.merge('RGBA', (r,g,b,a)).resize(size)
    box_icon = img.copy()
    box_icon.save(r"icons\box_icon.png", "PNG")
    #box_icon.show() if __name__ == "__main__" else None

