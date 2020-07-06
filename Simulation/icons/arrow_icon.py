import numpy as np
import matplotlib as mpl
from matplotlib.pyplot import show
mpl.style.use("fast")

"""
    This module creates a picture called
    box_icon
    """
fig, ax = mpl.pyplot.subplots()

arrow = mpl.patches.FancyArrowPatch((0.05, 0.5), (0.95, 0.5),
                                    mutation_scale=420,
                                    lw=15,
                                    facecolor = 'white',
                                    )
ax.add_patch(arrow)

if __name__ == "__main__": mpl.pyplot.show()

else:
    try:from icons.img_pack import get_img_from_ax 
    except: from img_pack import get_img_from_ax 
    size = (200, 200)
    img = get_img_from_ax(ax, size)
    arrow_right = img.copy()

fig2, ax2 = mpl.pyplot.subplots()
arrow2 = mpl.patches.FancyArrowPatch((0.95, 0.5), (0.05, 0.5),
                                    mutation_scale=420,
                                    lw=15,
                                    facecolor = 'white',
                                    )

ax2.add_patch(arrow2)
if __name__ == "__main__": mpl.pyplot.show() 

else:
    try:from icons.img_pack import get_img_from_ax 
    except: from img_pack import get_img_from_ax 
    size = (200, 200)
    img = get_img_from_ax(ax2, size)
    arrow_left = img.copy()


    
