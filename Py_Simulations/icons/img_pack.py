from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import  numpy as np
def get_img_from_ax_og(ax, size = (50, 50)):
    """Returns PIL image that has it's background removed
        It removes all colors that are equal to the color
        of the leftmost pixel in the figure."""
    fig = ax.figure
    canvas = fig.canvas
    ax.set_axis_off()
    ax.set_position([0, 0, 1, 1])
    fig.patch.set_facecolor("#b1d2ca") #Random color that is unlikely to be in your picture
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.close("all")#Without this the image glitches for some reason.
    img = Image.frombytes('RGB', canvas.get_width_height(),
                          fig.canvas.tostring_rgb()).resize(size).convert("RGBA")
    pixels = img.load()
    reference = pixels[0,0]
    for i in range(img.size[0]):    # for every col:
        for j in range(img.size[1]):    # For every row
            if pixels[i, j] == reference:
                pixels[i,j] = (0, 0, 0, 0) # set the colour accordingly
    return img

def get_img_from_ax(ax, size = (50, 50)):
    """Newer version of the function above.
    For some reason this version does not work
    on arrows.
    Avantage is that without the for loop, it runs a
    lot faster."""
    fig = ax.figure
    canvas = fig.canvas
    ax.axis("off")
    ax.set_position([0, 0, 1, 1])
    ax.patch.set_alpha(0.0)
    fig.patch.set_alpha(0.0)
    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.close("all")#Without this the image glitches for some reason.
    a=np.frombuffer(
        fig.canvas.tostring_argb(),
        dtype = np.uint8).reshape(*canvas.get_width_height()[::-1], 4)
    img  = Image.fromarray(a)
    a,r,g,b = img.split()
    img = Image.merge('RGBA', (r,g,b,a))#.resize(size)
    return img




"""
    Now we check the images we have
    """
if __name__ == "__main__":
    import tkinter as tk
    from question import question_icon
    from planet_icon import planet_icon
    from box import box_icon
    from time_icon import time_icon
    from spring_icon import spring_icon
    from arrow_icon import arrow_right, arrow_left
    size = 200, 200

    #question_icon.save("question.png")
    #planet_icon.save("planet.png")
    #box_icon.save("box.png")

    window = tk.Tk()
    quicky = ImageTk.PhotoImage
    question = quicky(question_icon.resize(size))
    planet = quicky(planet_icon.resize(size))
    box = quicky(box_icon.resize(size))
    time = quicky(time_icon.resize(size))
    arrow_right = quicky(arrow_right.resize(size))
    arrow_left = quicky(arrow_left.resize(size))
    label1 = tk.Label(window, image = question).pack(side = "left")
    label2 = tk.Label(window, image = planet).pack(side = "left")
    label3 = tk.Label(window, image = box).pack(side = "right")
    label4 = tk.Label(window, image = time).pack(side = "right")
    label5 = tk.Label(window, image = arrow_right).pack(side = "right")
    label6 = tk.Label(window, image = arrow_left).pack(side = "right")

    window.mainloop()
