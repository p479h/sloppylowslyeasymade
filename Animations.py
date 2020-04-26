import numpy as np
from matplotlib import pyplot as plt
import time
from matplotlib.widgets import Button
t = np.linspace(0, 2, 100)
x = np.linspace(0, 10, 100)
y = np.sin(x*3)*t

fig = plt.figure()
ax = fig.add_subplot(111)

ax.set(xlim=(0, 10), ylim=(-2, 2))
line, = ax.plot([])

updatedx = []
updatedy = []


def start(event):
    print('hellooo')
    global updatedx
    global updatedy
    for index, t in enumerate(x):
        updatedx.append(t)
        updatedy.append(y[index])
        line.set_xdata(updatedx)
        line.set_ydata(updatedy)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.0001)


ax2 = fig.add_axes([0.5, 0.05, 0, 0])
button = Button(ax2, 'Button', color='yellow', hovercolor='blue')
cid = fig.canvas.mpl_connect('button_press_event', start)
button.on_clicked(start)
plt.show()
