import time
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

#Making the plot
fig, ax = plt.subplots(figsize = (4, 4))
lim =-5, 5
ax.set(xlim = lim, ylim = lim)

#Making the patch
marker = mpl.markers.MarkerStyle("<")
marker.transform = mpl.transforms.Affine2D().scale(4).rotate_deg(270)+ax.transData
#marker._vertices = marker.transform(marker.get_path()._vertices)

patch = mpl.patches.PathPatch(marker.get_path(), lw=10)
ax.add_patch(patch)
patch.set_transform(marker.transform)

if __name__ == "__main__":
    plt.show()
else:
    try: from icons.img_pack import get_img_from_ax
    except: from img_pack import get_img_from_ax
play_icon = get_img_from_ax(ax)
