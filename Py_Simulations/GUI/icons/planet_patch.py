import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.art3d as art3d


class PlanetPatch(mpl.patches.Circle):
    cz = 0
    def __init__(self, xy, radius,
                 color = None, linewidth = 20,
                 edgecolor = "black", ringcolor = "white",
                 *args, **kwargs):
        ratio = radius/6
        mpl.patches.Circle.__init__(self, xy, radius,
                                    linewidth = linewidth*ratio,
                                    color = color,
                                    zorder = PlanetPatch.cz,
                                    *args, **kwargs)
        self.set_edgecolor(edgecolor)
        xy_ringcontour = np.array(xy)+[0, radius*-0.2/6]
        self.xy_ringcontour = xy_ringcontour - np.array(xy)
        self.ring_contour = mpl.patches.Arc(xy_ringcontour,
                                15*radius/6, 4*radius/6,
                                angle =10, theta1 = 165,
                                theta2 = 14.5,
                                fill = False, 
                                linewidth = 65*linewidth*ratio/20,
                                zorder = 1+PlanetPatch.cz)
               
        self.ring_inner = mpl.patches.Arc(xy_ringcontour,
                                 15*radius/6, 4*radius/6,
                                 angle = 10, theta1 = 165 ,
                                 theta2 = 14.5,fill = False,
                                 linewidth = 36*linewidth*ratio/20,
                                 zorder = 2+PlanetPatch.cz)
        
        self.top = mpl.patches.Wedge([0,0], radius, theta1 = 8,
                                     theta2 = 192,
                                     zorder=3+PlanetPatch.cz)
        self.xy_init = xy
        self.top._path._vertices=self.top._path._vertices+xy

        self.ring_contour._edgecolor = self._edgecolor
        self.ring_inner.set_edgecolor(ringcolor)
        self.top._facecolor = self._facecolor
            
    def add_to_ax(self, ax):
        ax.add_patch(self)
        ax.add_patch(self.ring_contour)
        ax.add_patch(self.ring_inner)
        ax.add_patch(self.top)
        

    def translate(self, dx, dy):
        self._center = self.center + [dx,dy]
        self.ring_inner._center = self.ring_inner._center +[dx, dy]
        self.ring_contour._center = self.ring_contour._center + [dx,dy]
        self.top._path._vertices = self.top._path._vertices + [dx,dy]
        #self.update_secondary()

    def set_xy(self, new_xy):
        new_xy = np.array(new_xy)
        self._center = new_xy
        self.ring_inner._center = self.xy_ringcontour + new_xy
        self.ring_contour._center = self.xy_ringcontour + new_xy
        self.top._path._vertices += new_xy - self.xy_init 

fig  = plt.figure(figsize=(6, 6))
ax = fig.add_subplot()
lim = -8.5, 8.6
ax.set(xlim = lim, ylim = lim,
       facecolor = "white")
planets = []
colors = mpl.colors.cnames
colors = [c for c in colors]
for x in range(100):
    xy = np.random.randint(-7, 7, 2)
    r = np.random.randint(1, 15)/30
    color = np.random.choice(colors)
    planet = PlanetPatch(xy, r, linewidth = 20,
                         color = color,
                         ringcolor = np.random.choice(colors),
                         edgecolor = np.random.choice(colors))
    planet.add_to_ax(ax)
    planets.append(planet)


fig.canvas.draw()
#plt.savefig("planet.png", dpi=10)
plt.show()
