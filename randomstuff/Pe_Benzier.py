"""
    This is a helper for drawing with bezier curves
    It lets you reposition points to get the right relative positions
    for whatever drawing you want to make with bezier curves.
    All you have to do is run this file.

    """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

print(mpl.__file__)
fig = plt.figure()
ax = fig.add_axes([0, 0, 1, 1])
canvas = fig.canvas;
ax.axis("off");
fontd = {'fontfamily': 'Consolas',"size" : "10"}
p1 = [.1, .2]; p2 = [0.2,.2]; p3 = [.4,.5]; p4 = [.6, .2];
ps = [p1, p2, p3, p4];
patches = [];
for i,p in enumerate(ps):
    circ = mpl.patches.Circle(p, 0.02);
    circ.ind = i;
    label = 'p1, p2, p3, p4'.split(', ')[i];
    circ.text = plt.text(p[0]+0.02, p[1]+0.02, label, fontdict = fontd);
    ax.add_patch(circ);
    patches.append(circ);
print(dir(circ.text));
verts = np.array(ps);
path = mpl.path.Path(verts.copy(), (1, 4, 1, 1));
line = mpl.patches.PathPatch(path, fill = False);
text = plt.text(0.05, 0.9, r"[p1, p2, p3, p4]:",
         fontdict = fontd);
ax.add_patch(line);

lim = (0, 1);
ax.set(xlim = lim, ylim = lim)

pressed = False
def onclick(event):
    global pressed;
    pressed = True;
    for p in patches:
        p.ispressed = False
        if (p.contains(event))[0]:
            p.ispressed = True;
            break;
    global ix;
    global iy;
    ix, iy = event.xdata, event.ydata;
    
def onrelease(event):
    global pressed
    pressed = False
    found_flag = False;
    for p in patches:
        p.ispressed = False;
    global verts
    verts = line._path._vertices.copy();

def onhover(event):
    global pressed
    if not pressed: return;
    for p in patches:
        if p.ispressed:
            found_flag = True;
            break
        else:
            found_flag = False;
    if not found_flag or not (event.inaxes == p.axes): return;
    
    dx = event.xdata-ix;
    dy = event.ydata-iy;
    newverts = verts[p.ind]+[dx, dy];
    patches[p.ind]._center = verts[p.ind]+[dx, dy];
    patches[p.ind].text.set_x(newverts[0]+0.02);
    patches[p.ind].text.set_y(newverts[1]+0.02);
    line._path._vertices[p.ind] = verts[p.ind]+[dx, dy];
    text.set_text(f"{r'[p1, p2, p3, p4]: '+str(np.round(line._path._vertices, 2).tolist())}");
    canvas.draw();
    canvas.flush_events();

cid = fig.canvas.mpl_connect('button_press_event', onclick)
cid2 = fig.canvas.mpl_connect("motion_notify_event", onhover)
cid3 = fig.canvas.mpl_connect("button_release_event", onrelease)
plt.show()
