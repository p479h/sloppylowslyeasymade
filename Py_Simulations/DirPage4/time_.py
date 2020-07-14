"""This is the code that makes up the clock in page 4"""
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk
import datetime
from math import pi
import time
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
mpl.style.use("fast")
mpl.use("TkAgg")
"""
    This is just to test the graphics
    """

def make_clock(self):
    if not hasattr(self, "canvas"):
        self.fig = plt.figure()
        self.canvas = FigureCanvasTkAgg(self.fig, self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM,
                                        fill=tk.BOTH,
                                        expand=True,
                                        )
        fig  = self.fig
        self.ax = fig.add_subplot()
        ax = self.ax
        ax.axis("off")
        ax.patch.set_alpha(0.001)
        outer_arc = mpl.patches.Arc((0.5,0.5), 0.95, 0.95, transform = ax.transAxes,
                                    color = "black", alpha = 0.001)

        #inner_arc = mpl.patches.Arc((0.5,0.5), 0.82, 0.82, transform = ax.transAxes,
        #                            color = "black", alpha = 0.001)
        between_ = mpl.patches.Arc((0.5,0.5), 0.87, 0.87, transform = ax.transAxes,
                                    color = "darkorange", lw=7, alpha = 0.001)

        between_2 = mpl.patches.Arc((0.5,0.5), 0.87, 0.87, transform = ax.transAxes,
                                    color = "darkblue", lw=15, zorder=-1, alpha = 0.001)

        innercirc = mpl.patches.Circle((0.5,0.5), 0.42, transform = ax.transAxes,
                                    color = "white", zorder=-2, alpha = 0.001)
        ax.add_patch(innercirc)
        ax.add_patch(outer_arc)
        ax.add_patch(between_2)
        ax.add_patch(between_)
        #ax.add_patch(inner_arc)
        fig.patch.set_facecolor("gray")
        fig.patch.set_alpha(0.001)
        x, y = [np.array(f) for f in ([0.41, 0.40], [0.5, 0.5])]
        theta = 0
        ticks = []
        for i in range(12):
            x_ = 0.5+x*np.cos(theta)
            y_ = 0.5+x*np.sin(theta)
            line, = ax.plot(x_, y_, transform = ax.transAxes,
                            lw = 10, color='black')
            theta+=pi/6
            ticks.append(line)
            self.canvas.draw()
            time.sleep(0.08)

        hour_line, = ax.plot([0.5, 0.7], [0.5, 0.5], transform = ax.transAxes,
                             lw=8, color="darkblue", alpha = 0.001)
        min_line, = ax.plot([0.5, 0.5], [0.5, 0.8], transform = ax.transAxes,
                             lw=8, color = "darkorange", alpha = 0.001)
        sec_line, = ax.plot([0.5, 0.5], [0.5, 0.8], transform = ax.transAxes,
                             lw=6, color = "red", alpha = 0.001)

        ticks.append(hour_line)
        ticks.append(min_line)
        ticks.append(sec_line)
        #ticks.append(inner_arc)
        ticks.append(innercirc)
        ticks.append(between_2)
        ticks.append(between_)
        ticks.append(outer_arc)

        for line in (hour_line, min_line, sec_line):
            if line == hour_line:
                h = datetime.datetime.now().minute/60 + datetime.datetime.now().hour
                theta1 = h*2*pi/12+pi/2
                l = 0.22
            elif line == min_line:
                theta1 = datetime.datetime.now().minute*2*pi/60+pi/2
                l = 0.30
            else:
                theta1 = datetime.datetime.now().second*2*pi/60+pi/2
                l = 0.33
            x = 0.5-l*np.cos(-theta1)
            y = 0.5-l*np.sin(-theta1)
            line.set_data([0.5, x], [0.5, y])

        #ax.set_facecolor("blue")
        self.lineh = hour_line
        self.linem = min_line
        self.lines = sec_line
        self.running = False
        #self.canvas.draw()
        try:
            for x in range(20):
                self.fig.patch.set_alpha(x/20+0.05)
                for o in ticks:
                    o.set_alpha(x/20+0.05)
                self.canvas.draw()
                self.canvas.flush_events()
        except :
            print("Time interupted")

        #plt.show()

def set_data(line, flag):
    """Flag is hour, sec, min"""
    if flag == "hour":
        h = datetime.datetime.now().minute/60 + datetime.datetime.now().hour
        theta1 = h*2*pi/12+pi/2
        l = 0.22
    elif flag == "min":
        theta1 = datetime.datetime.now().minute*2*pi/60+pi/2
        l = 0.30
    else:
        theta1 = datetime.datetime.now().second*2*pi/60+pi/2
        l = 0.33
    x = 0.5-l*np.cos(-theta1)
    y = 0.5-l*np.sin(-theta1)
    line.set_data([0.5, x], [0.5, y])
    line._axes.draw_artist(line)

def show_time(self):
    if not hasattr(self, "canvas"): return
    ticks = self.fig.get_children()
    self.fig.patch.set_alpha(0.99)
    for o in ticks:
        o._alpha=0.99
    self.canvas.draw()
    self.canvas.flush_events()
    self.running =True
    lineh = self.lineh
    linem = self.linem
    lines = self.lines
    for line in (lineh, linem, lines):
        line.set_animated(True)
    self.canvas.draw()
    bg = self.canvas.copy_from_bbox(line.axes.bbox)
    try:
        while self.running:
            self.canvas.restore_region(bg)
            set_data(lineh, "hour")
            set_data(linem, "min")
            set_data(lines, "sec")
            self.canvas.blit()
            self.canvas.flush_events()
            time.sleep(0.3)
        if hasattr(self,'canvas'):
            for line in (lineh, linem, lines):
                line.set_animated(False)
            self.canvas.draw()
    except:
        print("Execution was interrupted.")
        print("You can ignore this message and keep having fun.")
