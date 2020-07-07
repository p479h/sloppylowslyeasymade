from PIL import Image, ImageTk
try:
    spring_icon = Image.open(r"icons\spring_icon.png")
except:
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    import numpy as np
    mpl.style.use("fast")
    """
        You can find the planet icon as a foto below.
        It is named: spring_icon
        """

    fig  = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(); #ax.axis("off")
    ax.set(xlim = (-0.06, 0.79), ylim = (0, 1))
    p = [[0.00, 0.3], [0.1, 0.5], [0.1, 0.8], [0.00, 0.6]]
    side = mpl.patches.Polygon(p,
                                transform = ax.transAxes,
                               edgecolor = "black",
                               lw=2)
    ax.add_patch(side)
    x = np.linspace(0,0.5, 12)
    y = [0.4 if i%2==0 else 0.7 for i in range(8)]
    h = 0.57#Height of straight ends
    y = [h, h]+y+[h, h]
    line, = ax.plot(x, y, lw=3, transform = ax.transData,
                    color = "black", )


    r=0.03;h=0.62
    x = 0.75

    p = np.array([[0.668, 0.42], [0.968, 0.42], [0.968, 0.72], [0.668, 0.72]])
    block = mpl.patches.Polygon(p,lw=3,
                                transform = ax.transAxes,
                                color = "yellow",)
    block.set_edgecolor("black")
    ax.add_patch(block)

    eye_left = mpl.patches.Circle([x, h], r, color="black",
                                  transform = ax.transAxes,
                                  )
    ax.add_patch(eye_left)

    eye_right = mpl.patches.Circle([x+0.14, h], r, color="black",
                                  transform = ax.transAxes,
                                  )

    ax.add_patch(eye_right)

    smile = mpl.patches.Arc([(2*x+0.14)/2, h], height = 0.2,
                            width = 0.35, theta1=225, theta2=310,
                            transform = ax.transAxes, lw=5)
    ax.add_patch(smile)
    #ax.axis('off')
    plt.show() if __name__ == "__main__" else None

    try:
        from icons.img_pack import get_img_from_ax
    except:
        from img_pack import get_img_from_ax
    size = (200, 200)
    img = get_img_from_ax(ax, size)

    if __name__ == "__main__":
        import tkinter as tk
        window = tk.Tk()
        window.geometry("500x500")
        img = ImageTk.PhotoImage(img)
        label = tk.Label(window)
        label.config(image=img)
        label.place(x=0, y=0)
        window.mainloop()


    """Below you can find the icon"""
    spring_icon = img.copy()
    spring_icon.save(r"icons\spring_icon.png", "PNG")
