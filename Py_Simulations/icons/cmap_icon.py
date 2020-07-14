try:
    from PIL import Image
    cmap_icon = Image.open(r"icons\cmap_icon.png")
except:
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from matplotlib.pyplot import show
    mpl.style.use("fast")

    """
        This module creates a picture called
        box_icon
        """
    gradient = np.linspace(0,1,50)
    gradient = np.vstack((gradient, gradient))

    fig, ax = plt.subplots(figsize = (4, 1))
    ax.axis("off")
    ax.set_position([0,0,1,1])
    ax.imshow(gradient, aspect = "auto", cmap = "gist_rainbow")

    #plt.show()

    if __name__ == "__main__":
        plt.show()
    else:
        try: from icons.img_pack import get_img_from_ax
        except: from img_pack import get_img_from_ax
    cmap_icon = get_img_from_ax(ax, size = (20, 90))
    cmap_icon.save(r"icons\cmap_icon.png", "PNG")
