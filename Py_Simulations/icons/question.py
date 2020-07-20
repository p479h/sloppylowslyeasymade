try:
    from PIL import Image
    question_icon = Image.open(r"icons\question_icon.png")
except:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.path import Path
    import matplotlib.markers as m
    mpl.style.use("fast")

    """
        This file creates a backgroundless picture called
        question_icon
        """

    fig, ax = plt.subplots(figsize = (5, 5))
    lim = -5.8, 5.7
    ax.set(xlim = lim, ylim = lim)


    marker_obj = m.MarkerStyle('$?$')
    path = marker_obj.get_path().transformed(marker_obj.get_transform())

    path._vertices = np.array(path._vertices)*8 #To make it larger
    path._vertices[4] = [0,0]#This is where the vertices close
    full_codes = path.codes
    full_vertices = path._vertices
    mark_vertices = full_vertices[5:]
    mark_codes = full_codes[5:]

    circ_path = Path.unit_circle()
    circ_verts = circ_path._vertices*0.65+[0.1, -3]
    circ_codes = circ_path.codes

    ##print(circ_verts)
    ##print(circ_codes)

    new_vertices = np.append(circ_verts, mark_vertices, axis=0)-[0,0.5]
    new_codes = np.append(circ_codes, mark_codes, axis = 0)

    """All this stuff that is commented out was used to make this path.
    when ? was used to create the path. The little dot under the ? was
    shown as a square, not a circle. So I had to modify the geometric
    descriptors of the patch to make it look better. DO NOT ATTEMPT
    THIS ON IMPORTANT FILES"""

    ##print(new_vertices)
    ##print(new_codes)
    ##
    ##print(dir(path))
    ##print(path.codes)
    ##print(path._vertices)

    path._vertices = new_vertices
    path._codes = new_codes

    patch = mpl.patches.PathPatch(path, facecolor="cornflowerblue", lw=2)
    ax.add_patch(patch)

    def translate_verts(patch, i=0, j=0, z=None):
        patch._path._vertices = patch._path._vertices + [i, j]

    def rescale_verts(patch, factor = 1):
        patch._path._vertices = patch._path._vertices * factor

    #translate_verts(patch, i=-0.7, j=-0.1)
    inside = mpl.patches.Circle((0,0), 5, color = "white",
                                zorder=-1)
    ax.add_patch(inside)
    #fig.set_facecolor("gray")

    circ = mpl.patches.Arc([0,0], 11, 11,
                           angle=0.0, theta1=0.0, theta2=360.0,
                           lw=10, facecolor = "cornflowerblue",
                           edgecolor = "black")
    ax.add_patch(circ)#One of the rings around the questionmark

    circ = mpl.patches.Arc([0,0], 10.5, 10.5,
                           angle=0.0, theta1=0.0, theta2=360.0,
                           lw=10, edgecolor = "cornflowerblue")
    ax.add_patch(circ)#Another one of the rings around the question mark

    circ = mpl.patches.Arc([0,0], 10, 10,
                           angle=0.0, theta1=0.0, theta2=360.0,
                           lw=10, edgecolor = "black")
    ax.add_patch(circ)


    if __name__ == "__main__":
        ax.axis("off")
        ax.set_position([0, 0, 1, 1])
        #fig.canvas.draw()
        #plt.savefig("question.png", dpi=40)
        plt.show()

    else:
        try:
            from icons.img_pack import get_img_from_ax
        except:
            from img_pack import get_img_from_ax
        size = (400, 400)
        img = get_img_from_ax(ax, size)
        question_icon = img.copy()
        question_icon.save(r"icons\question_icon.png", "PNG")
