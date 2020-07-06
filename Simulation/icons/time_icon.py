import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
mpl.style.use("fast")
"""
    You can find the planet icon as a foto below.
    It is named: planet_icon
    """

fig  = plt.figure(figsize=(6, 6))
ax = fig.add_subplot()
outer_arc = mpl.patches.Arc((0.5,0.5), 0.95, 0.95, transform = ax.transAxes,
                            color = "black")
ax.add_patch(outer_arc)

inner_arc = mpl.patches.Arc((0.5,0.5), 0.82, 0.82, transform = ax.transAxes,
                            color = "black")
between_ = mpl.patches.Arc((0.5,0.5), 0.87, 0.87, transform = ax.transAxes,
                            color = "darkorange", lw=7)
ax.add_patch(between_)
between_2 = mpl.patches.Arc((0.5,0.5), 0.87, 0.87, transform = ax.transAxes,
                            color = "darkblue", lw=20, zorder=-1)
ax.add_patch(between_2)
ax.add_patch(inner_arc)

innercirc = mpl.patches.Circle((0.5,0.5), 0.42, transform = ax.transAxes,
                            color = "white", zorder=-2)
ax.add_patch(innercirc)
fig.patch.set_facecolor("gray")
x, y = [np.array(f) for f in ([0.41, 0.40], [0.5, 0.5])]
theta = 0
for i in range(12):
    x_ = 0.5+x*np.cos(theta)
    y_ = 0.5+x*np.sin(theta)
    line, = ax.plot(x_, y_, transform = ax.transAxes,
                    lw = 15, color='black')
    theta+=3.14/6
hour_line, = ax.plot([0.5, 0.7], [0.5, 0.5], transform = ax.transAxes,
                     lw=15, color="darkblue")
min_line, = ax.plot([0.5, 0.5], [0.5, 0.8], transform = ax.transAxes,
                     lw=15, color = "darkorange")
#ax.set_facecolor("blue")

ax.axis("off")
plt.show() if __name__ == "__main__" else None

try:
    from icons.img_pack import get_img_from_ax
except:
    from img_pack import get_img_from_ax
size = (200, 200)
img = get_img_from_ax(ax, size)

if __name__ == "__mai__":
    import tkinter as tk
    #img2 = Image.open("planet.png").resize(size)
    window = tk.Tk()
    window.geometry("500x500")
    img = ImageTk.PhotoImage(img)
    #img2 = ImageTk.PhotoImage(img2)
    label = tk.Label(window)
    label.config(image=img)
    label.place(x=0, y=0)
    label2 = tk.Label(window)
    #label2.config(image=img2)
    label2.place(x=250, y=0)
    window.mainloop()


"""Below you can find the icon"""
time_icon = img.copy()
