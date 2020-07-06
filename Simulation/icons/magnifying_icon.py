import time
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#Making the plot
fig, ax = plt.subplots(figsize = (4, 4))
lim =-5, 5
ax.set(xlim = lim, ylim = lim)

#Making the patch
marker = mpl.markers.MarkerStyle("o")
marker.transform = mpl.transforms.Affine2D().scale(2.4).translate(2, 2)+ax.transData

patch = mpl.patches.PathPatch(marker.get_path(), lw=7, fill = True, color = "white")
patch._edgecolor = (0, 0, 0, 1)
ax.add_patch(patch)
patch.set_transform(marker.transform)

#Then we make the body
marker = mpl.markers.MarkerStyle("|")
marker.transform = mpl.transforms.Affine2D().scale(3).rotate(-3.14/4).translate(-1.8, -1.8)+ax.transData

patch = mpl.patches.PathPatch(marker.get_path(), lw=10,  fill = True, color = "black")
patch._edgecolor = (0, 0, 0, 1)
ax.add_patch(patch)
patch.set_transform(marker.transform)

if __name__ == "__main__":
    plt.show()
else:
    try: from icons.img_pack import get_img_from_ax
    except: from img_pack import get_img_from_ax
magnifying_icon = get_img_from_ax(ax)
