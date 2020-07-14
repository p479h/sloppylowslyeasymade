from PIL import Image, ImageTk
try:
    planet_icon = Image.open(r"icons\planet_icon.png")
except:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    mpl.style.use("fast")

    """
        You can find the planet icon as a foto below.
        It is named: planet_icon
        """

    fig  = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot()
    lim = -8.7, 8.7
    ax.set(xlim = lim, ylim = lim)
    patch2 = mpl.patches.Circle([0,0], 6, fill = True, edgecolor = "black",
                                linewidth=20)
    patch = mpl.patches.Arc([0,-0.2], 15, 4, angle =10, theta1 = 165 ,theta2 = 14.5,
                            fill = False, edgecolor = "black", linewidth = 65)
    patch3 = mpl.patches.Arc([0,-0.2], 15, 4, angle =10, theta1 = 165 ,theta2 = 14.5,
                            fill = False, edgecolor = "white", linewidth = 36)
    wed = mpl.patches.Wedge([0,0], 6, theta1 = 8, theta2 = 192,
                             zorder=2)
    ax.add_patch(wed)
    ax.add_patch(patch2)
    ax.add_patch(patch)
    ax.add_patch(patch3)
    try:
        from icons.img_pack import get_img_from_ax
    except:
        from img_pack import get_img_from_ax
    size = (200, 200)
    img = get_img_from_ax(ax, size)

    if __name__ == "__main__":
        import tkinter as tk
        img2 = Image.open("planet.png").resize(size)
        window = tk.Tk()
        window.geometry("500x500")
        img = ImageTk.PhotoImage(img)
        img2 = ImageTk.PhotoImage(img2)
        label = tk.Label(window)
        label.config(image=img)
        label.place(x=0, y=0)
        label2 = tk.Label(window)
        label2.config(image=img2)
        label2.place(x=250, y=0) 
        window.mainloop()


    """Below you can find the icon"""
    planet_icon = img.copy()
    planet_icon.save(r"icons\planet_icon.png", "PNG")
