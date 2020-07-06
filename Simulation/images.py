"""
    This document provides a dictionary with all the necessary images
    for the GUI.
    """
from icons.question import question_icon
from icons.planet_icon import planet_icon
from icons.box import box_icon
from icons.time_icon import time_icon
from icons.arrow_icon import arrow_right, arrow_left
from icons.spring_icon import spring_icon
from icons.magnifying_icon import magnifying_icon
from icons.record_icon import record_icon
from icons.star_icon import star_icon
from icons.replay_icon import replay_icon
from icons.play_icon import play_icon
from icons.pause_icon import pause_icon
from icons.cmap_icon import cmap_icon

icons = (question_icon, planet_icon, box_icon, time_icon,
         arrow_right, arrow_left, spring_icon, magnifying_icon,
         record_icon, star_icon, replay_icon,play_icon, pause_icon,
         cmap_icon)



size = 100, 100
if __name__ == "__main__":
    import tkinter as tk
    from PIL import Image, ImageTk

##    question_icon.save("question.png")
##    planet_icon.save("planet.png")
##    box_icon.save("box.png")

    window = tk.Tk()
    labels = []
    frame1 = tk.Frame(window)
    frame1.pack(side="top")
    frame2 = tk.Frame(window)
    frame2.pack(side="bottom")
    for index, icon in enumerate(icons):
        if index>len(icons)/2:
            window = frame1
        else:
            window = frame2
        img = ImageTk.PhotoImage(icon.resize(size))
        label = tk.Label(window, image = img)
        label.pack(side = "left")
        labels.append(label); labels.append(img)
    window.mainloop()

else:
    IMAGES = {}
    IMAGES["planet_icon"] = planet_icon
    IMAGES["question_icon"] = question_icon
    IMAGES["box_icon"] = box_icon
    IMAGES["time_icon"] = time_icon
    IMAGES["arrow_right"] = arrow_right
    IMAGES["arrow_left"] = arrow_left
    IMAGES["spring_icon"] = spring_icon
    IMAGES["magnifying_icon"] = magnifying_icon
    IMAGES["record_icon"] = record_icon
    IMAGES["star_icon"] = star_icon
    IMAGES["play_icon"] = play_icon
    IMAGES["replay_icon"] = replay_icon
    IMAGES["pause_icon"] = pause_icon
    IMAGES["cmap_icon"] = cmap_icon
