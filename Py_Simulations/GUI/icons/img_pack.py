from PIL import Image, ImageTk
import matplotlib.pyplot as plt
def get_img_from_ax(ax, size = (50, 50)):
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

"""
    Now we check the images we have
    """
if __name__ == "__main__":
    import tkinter as tk
    from question import question_icon
    from planet_icon import planet_icon
    from box import box_icon
    size = 200, 200

    question_icon.save("question.png")
    planet_icon.save("planet.png")
    box_icon.save("box.png")

    window = tk.Tk()
    quicky = ImageTk.PhotoImage
    question = quicky(question_icon.resize(size))
    planet = quicky(planet_icon.resize(size))
    box = quicky(box_icon.resize(size))
    label1 = tk.Label(window, image = question).pack(side = "left")
    label2 = tk.Label(window, image = planet).pack()
    label3 = tk.Label(window, image = box).pack(side = "right")

    window.mainloop()
