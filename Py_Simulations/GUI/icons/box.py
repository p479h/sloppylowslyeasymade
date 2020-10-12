import numpy as np
import matplotlib as mpl
from matplotlib.pyplot import show

"""
    This module creates a picture called
    box_icon
    """

vertices = \
     [[-0.253125, -0.15000000000000002], [-0.06562499999999999, -0.14375],
      [-0.021874999999999978, -0.07083333333333336], [-0.021874999999999978, 0.12916666666666665],
         [-0.19687499999999997, 0.1166666666666667], [-0.26249999999999996, 0.04791666666666661],
         [-0.253125, -0.15000000000000002]]

fig, ax = mpl.pyplot.subplots()
lim = -.21, .2
ax.set(xlim=(-0.33, 0.05), ylim=(-0.23,0.15), facecolor="#F0F0F0")
box = mpl.patches.Polygon(vertices, closed=True,
                            color="black", zorder=1,)
stars = np.random.uniform(-0.35, 0.2, size=(200, 2))
ax.add_patch(box)
for star in stars:
    """Checks if star will be inside the box"""
    if box.get_path().contains_point(star):
        patch = ax.scatter(star[0], star[1], c='white',
                           marker="*", zorder=2, s=10)
ax.plot([-0.253125, -0.0656], [-0.15002-0.02, -0.14375-0.02])
ax.plot([-0.021874999999999978+0.02, -0.021874999999999978+0.02], [-0.07083333333333336, 0.12916666666666665])
ax.plot([-0.0626, -0.021874+0.02], [-0.1400-0.02, -0.07083333333333336])
ax.text(-0.27, -0.2, s='Universe side length', size=20)

if __name__ == "__main__": mpl.pyplot.show()

else:
    from img_pack import get_img_from_ax
    size = (500, 500)
    img = get_img_from_ax(ax, size)
    box_icon = img.copy()
