try:
    from PIL import Image
    replay_icon = Image.open(r"icons\replay_icon.png")
except:
    import time
    import pandas as pd
    import matplotlib as mpl
    import matplotlib.pyplot as plt

    #Making the plot
    fig, ax = plt.subplots(figsize = (4, 4))
    lim =-8, 8
    ax.set(xlim = lim, ylim = lim)

    #Making the patch
    #This patch will be made with 3 patches,
    #A wedge for the round part; A small square to cover the edge of the wedge;
    #A triangular marker for the head.

    patch1 = mpl.patches.Wedge(0.0, 5, 210, 135+360, width = 2, color = 'green',
                               lw = 10)
    patch1.set_edgecolor("black")
    ax.add_patch(patch1)

    marker = mpl.markers.MarkerStyle("<")
    marker.transform = mpl.transforms.Affine2D().scale(1).scale(1.6).rotate_deg(20).translate(-3.90, 2.1)+ax.transData
    #marker._vertices = marker.transform(marker.get_path()._vertices)

    patch = mpl.patches.PathPatch(marker.get_path(), lw=10, facecolor="green")
    ax.add_patch(patch)
    patch.set_transform(marker.transform)


    marker = mpl.markers.MarkerStyle("s")
    marker.transform = mpl.transforms.Affine2D().scale(1.49, 1.32).rotate_deg(47).translate(-3.05, 1.56)+ax.transData
    #marker._vertices = marker.transform(marker.get_path()._vertices)

    patch = mpl.patches.PathPatch(marker.get_path(), lw=0, facecolor="green")
    ax.add_patch(patch)
    patch.set_transform(marker.transform)


    if __name__ == "__main__":
        plt.show()
    else:
        try: from icons.img_pack import get_img_from_ax
        except: from img_pack import get_img_from_ax
    replay_icon = get_img_from_ax(ax)
    replay_icon.save(r"icons\replay_icon.png", "PNG")
