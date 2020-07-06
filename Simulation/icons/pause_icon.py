import time
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#Making the plot
fig, ax = plt.subplots(figsize = (4, 4))
lim =-5, 5
ax.set(xlim = lim, ylim = lim)

#Making the patch
marker = mpl.markers.MarkerStyle("|")
marker.transform = mpl.transforms.Affine2D().scale(4).translate(-1.5, 0)+ax.transData

marker2 = mpl.markers.MarkerStyle("|")
marker2.transform = mpl.transforms.Affine2D().scale(4).translate(1.5, 0)+ax.transData

patch = mpl.patches.PathPatch(marker.get_path(), lw=40)
patch2 = mpl.patches.PathPatch(marker2.get_path(), lw = patch._linewidth)

ax.add_patch(patch)
ax.add_patch(patch2)
patch.set_transform(marker.transform)
patch2.set_transform(marker2.transform)

if __name__ == "__main__":
    plt.show()
else:
    try: from icons.img_pack import get_img_from_ax
    except: from img_pack import get_img_from_ax
pause_icon = get_img_from_ax(ax)
