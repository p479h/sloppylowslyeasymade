from Pages import Page, IMAGES, Main_page, ImageTk, plt
from Page1 import Page1
from DirPage1.DirPage1_1.box import make_box_interactive
from messages import page1_1messages
import numpy as np
import tkinter as tk
from tkinter import ttk

class Page1_1(Page):
    """
    This page is inside page 1. It contains everything
    that concerns planets.
    """
    def __init__(self, *args, **kwargs):
        Page.__init__(self, name = "page1_1", *args, **kwargs)
        self.master.geometry("510x400")
        self.master.update()

        #The next part makes the use of grid easier
        #The idea is to use many squares like large pixels
        grid_len = [x for x in range(30)]
        minsize = (self.master.winfo_width()/30,
                   self.master.winfo_height()/30)

        self.columnconfigure(grid_len,
                             minsize = minsize[0],
                             weight = 1,
                             )

        self.rowconfigure(grid_len,
                          minsize = minsize[1],
                          weight=1,
                          )


        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=1, row=2, sticky="NSEW",
                             columnspan=28, rowspan = 27,
                             )


        self.main_frame = ttk.Frame(self.notebook,
                                   border = 1,
                                   )

        self.edit_frame = ttk.Frame(self.notebook,
                                    border=self.main_frame["border"],)

        self.notebook.add(self.main_frame, text="Making object")
        self.notebook.add(self.edit_frame, text = "Edit objects")


        self.main_frame.update()
        grid_len = [x for x in range(30)]
        minsize = (self.main_frame.winfo_width()/32,
                   self.main_frame.winfo_height()/32)
        self.main_frame.rowconfigure(grid_len+list(range(30, 32)),
                                     minsize = minsize[1],
                                     weight =1
                                     )
        self.label_main = tk.Label(self,
                                   text = "Objects",
                                   font = ("Consolas","13","bold"),
                                   )

        self.label_main.grid(row=0, rowspan=3,
                             column = 1, columnspan = 5,
                             sticky = "N")

        self.main_frame.columnconfigure(grid_len+[30, 31],
                                        minsize = minsize[0],
                                        weight = 1,
                                        )

        ###
        self.edit_frame.rowconfigure(grid_len+list(range(30, 32)),
                                     minsize = minsize[1],
                                     weight =1
                                     )

        self.edit_frame.columnconfigure(grid_len+[30, 31],
                                        minsize = minsize[0],
                                        weight = 1,
                                        )

        self.make_navigation_buttons(forward = "page1_2",backward = "page1")
        self.forward_button.grid(row = 27, column = 28,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )

        self.backward_button.grid(row = 27, column = 26,
                                 rowspan = 2, columnspan = 2,
                                 sticky = "NSEW",
                                 )

        #The next function ensures that plots are deleted
        #This is done for efficiency purpuses
        self.backward_button.config(
            command = lambda:[
                              self.box_interactive.set(False),
                              self.update_box(),
                              self.change_page("page1")(),#Note the ()!!! Change page is a wraper!
                              ])

        self.forward_button.config(
            command = lambda:[
                              self.box_interactive.set(False),
                              self.update_box(),
                              self.change_page("page1_2")(),#Note the ()!!! Change page is a wraper!
                              self.master.geometry("600x500"),
                              ])




        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to Labels   ############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to Labels   ############
        ###############################################################
        ###############################################################


        #These two will just help the code stay cleaner in the
        #following lines
        self.font = ("Consolas","9","bold")
        self.gridparams = dict(column=0, columnspan=9, rowspan=3,
                               sticky = "w", row=1)
        rowstep = 3
        columnstep = 8


        self.type_label = tk.Label(self.main_frame,
                                   text = "Object type",
                                   font = self.font,
                                   justify = "left",
                                   )
        self.type_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep

        #oclor = object color
        self.ocolor_label = tk.Label(self.main_frame,
                                    text = "Object color",
                                    font = self.font,
                                    justify = "left",
                                    )
        self.ocolor_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep

        #
        self.marker_label = tk.Label(self.main_frame,
                                 text = "Shape",
                                 font = self.font,
                                 justify = "left",
                                 )

        self.marker_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep

        self.ring_label = tk.Label(self.main_frame,
                                     text="Give ring",
                                     font = self.font,
                                     justify = "left",
                                     )

        self.ring_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        custom = ttk.Style()
        custom.configure("size.TMenubutton",font = self.font)
        self.charge_type = tk.StringVar()
        self.charge_label = ttk.OptionMenu(self.main_frame,
                                      self.charge_type,
                                      "Chrg density",
                                    *("Chrg density","Total Charge"),
                                      style ="size.TMenubutton"
                                      )


        self.charge_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep



        #iv = initial velocity; ip = initial position
        self.iv_label = tk.Label(self.main_frame,
                                    text="Init velocity",
                                    font = self.font,
                                    justify = "left",
                                    )

        self.iv_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep

        self.ip_label = tk.Label(self.main_frame,
                                   text = "Init position",
                                   font = self.font,
                                   justify = "left",
                                   )

        self.ip_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        #rm = radius mass
        self.rm_val = tk.StringVar()
        self.rm = ttk.OptionMenu(self.main_frame,
                                 self.rm_val,
                                 "Mass",
                                 *["Mass","Radius"],
                                 style = "size.TMenubutton",
                                 )
        self.rm.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.density_label = tk.Label(
            self.main_frame,
            text = "Density",
            font = self.font,
            )

        self.density_label.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.markersizelabel = tk.Label(
            self.main_frame,
            text ="Markersize",
            font = self.font,)
        self.markersizelabel.grid(**self.gridparams)

        self.gridparams["row"]-=rowstep*2-rowstep



        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this 2nd col#########
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this 2nd col#########
        ###############################################################
        ###############################################################


        ####Now we make the second column
        self.gridparams["row"] = self.type_label.grid_info()["row"]
        self.gridparams["column"]+=columnstep

        #Creating new style with white background
        s = ttk.Style()
        s.configure("white.TMenubutton",
                    highlightbackground = "white",
                    background = "white", highlightcolor = "white",
                    bg = "white",
                    font = self.font)


        self.type_val = tk.StringVar()
        self.type_drop = ttk.OptionMenu(
            self.main_frame, self.type_val, "Planet", *[
                "Planet", "Sun", "Moon", "Other",
                ],
            style = "white.TMenubutton"
            )
        self.type_drop.grid(**self.gridparams)
        self.gridparams["row"] += rowstep


        #pc = planet color
        self.pc_val = tk.StringVar()
        self.color_drop = ttk.OptionMenu(
            self.main_frame, self.pc_val,
            "random", *self.colors,
            style = "white.TMenubutton") #Self.colors is made in Pages.py

        self.color_drop.grid(**self.gridparams)
        self.gridparams["row"] += rowstep


        self.marker_drop = ttk.Combobox(
            self.main_frame, values = self.markers[2:24],
            style = "white.TMenubutton",
            width = self.type_drop.winfo_width()*6,
            font = self.font, justify = tk.CENTER
            )

        self.marker_drop.set("o")

        self.marker_drop.grid(**self.gridparams)
        self.gridparams["row"] += rowstep


        self.ring_val = tk.BooleanVar()
        self.ring_val.set(False)
        self.ring_check = ttk.Checkbutton(
            self.main_frame, variable = self.ring_val,
            text = "yes",
            onvalue = True, offvalue =False,
            takefocus = 0,)
        self.ring_check.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.charge_entry = ttk.Entry(
            self.main_frame, width = 12,)
        self.charge_entry.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep
        self.charge_entry.insert(0, "0")


        self.v_entries = {}
        self.p_entries = {}
        self.commas = []
        self.parenthesis = []

        for p in ("x", "y", "z"):
            self.v_entries[p] = ttk.Entry(
                self.main_frame, width=2)
            self.p_entries[p] = ttk.Entry(
                self.main_frame, width=2)
        for x in range(4):
           self.commas.append(tk.Label(self.main_frame, text=","))
           j = tk.Label(self.main_frame, text = "(" if x%2==0 else ")",
                        font = (self.font[0],"13"))
           self.parenthesis.append(j)

        r = self.gridparams["row"]+1; c = self.gridparams["column"]+1
        cs, rs = 1, 3
        st = "EW"

        self.v_entries["x"].grid(row = r-1, column=c-1,sticky = st, rowspan = 3)
        self.v_entries["y"].grid(row = r-1, column=c+1, sticky = st, rowspan = 3)
        self.v_entries["z"].grid(row =r-1, column = c+3, sticky = st, rowspan = 3)
        self.p_entries["x"].grid(row = r+2, column=c-1,sticky = st, rowspan = 3)
        self.p_entries["y"].grid(row = r+2, column=c+1, sticky = st, rowspan = 3)
        self.p_entries["z"].grid(row =r+2, column = c+3, sticky = st, rowspan = 3)
        self.commas[0].grid(row = r-1,column = c,rowspan = rs,columnspan = cs,sticky = st,)
        self.commas[1].grid(row = r-1,column = c+2,rowspan = rs,columnspan = cs,sticky = st,)
        self.commas[2].grid(row = r-1+rowstep,column = c,rowspan = rs,columnspan = cs,sticky = st,)
        self.commas[3].grid(row = r-1+rowstep,column = c+2,rowspan = rs,columnspan = cs,sticky = st,)
        rs+=1
        r-=1
        self.parenthesis[0].grid(row = r-1,column = c-2,rowspan = rs,columnspan = cs,sticky = st,)
        self.parenthesis[1].grid(row = r-1,column = c+4,rowspan = rs,columnspan = cs,sticky = st,)
        self.parenthesis[2].grid(row = r-1+rowstep,column = c-2,rowspan = rs,columnspan = cs,sticky = st,)
        self.parenthesis[3].grid(row = r-1+rowstep,column = c+4,rowspan = rs,columnspan = cs,sticky = st,)

        self.gridparams["row"]+=2*rowstep


        self.rad_m_entry = ttk.Entry(
            self.main_frame, width = 12)
        self.rad_m_entry.insert(0, "1e10")
        self.rad_m_entry.grid(**self.gridparams)
        self.gridparams["row"] += rowstep


        self.density_entry = ttk.Entry(self.main_frame,
                                       width =12)
        self.density_entry.insert(0, "1e10")

        self.density_entry.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.markersize_entry = ttk.Entry(
            self.main_frame, width=12,)
        self.markersize_entry.insert(0, "10")
        self.markersize_entry.grid(**self.gridparams)


        self.gridparams["row"]-=rowstep


        ###############################################################
        #####The follwoing lines are exclusive to this page############
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this 3rd col#########
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this 3rd col#########
        ###############################################################
        ###############################################################


        self.gridparams["row"], self.gridparams["column"] = 13, 14
        self.gridparams["rowspan"], self.gridparams["columnspan"] = 3, 4
        self.gridparams["sticky"] = "NSEW"

        #cd stands for charge density
        self.units_cd = tk.StringVar()
        self.units_cd_ = "C, C/kg, C/g, C/mg".split(", ")
        self.units_cd_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_cd,
                                          "C/kg", *self.units_cd_,
                                          )
        self.units_cd_drop.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.units_v = tk.StringVar()
        self.units_v_ = "km/s, m/s".split(", ")
        self.units_v_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_v,
                                          "m/s", *self.units_v_,
                                          )
        self.units_v_drop.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.units_p = tk.StringVar()
        self.units_p_ = "km, m, cm, mm".split(", ")
        self.units_p_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_p,
                                          "m", *self.units_p_,
                                          )
        self.units_p_drop.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep

        #Radius
        self.units_rm = tk.StringVar()
        self.units_rm_ = "km, m, cm, mm, kg, g".split(", ")
        self.units_rm_drop = ttk.OptionMenu(self.main_frame,
                                          self.units_rm,
                                          "kg", *self.units_rm_,
                                          )
        self.units_rm_drop.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep


        self.units_den_val = tk.StringVar()
        self.units_den_drp = ttk.OptionMenu(
            self.main_frame, self.units_den_val,
            "kg/m3", *"kg/m3, g/m3".split(", "))
        self.units_den_drp.grid(**self.gridparams)



        ###############################################################
        #####The follwoing lines are question button and plot##########
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are question button and plot##########
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are question button and plot##########
        ###############################################################
        ###############################################################
        self.gridparams["row"], self.gridparams["column"] = 1, 18
        self.gridparams["rowspan"], self.gridparams["columnspan"] = 3, 2
        self.gridparams["sticky"] = "NSEW"


        self.question_icon = ImageTk.PhotoImage(IMAGES["question_icon"].resize((19, 19)))
        for x in range(10):
            but = tk.Button(self.main_frame,
                            image = self.question_icon,
                            relief = "raised", border=0,
                            )
            but.grid(**self.gridparams)
            self.gridparams["row"]+=rowstep
            setattr(self, f"help_b{x}", but)
        self.give_function_to_help_bs()
        self.gridparams["row"]-=rowstep

        self.box_img2 = ImageTk.PhotoImage(IMAGES['planet_icon'].resize((100,100)))
        self.box_lab = ttk.LabelFrame(
            self.main_frame, text = "Visuals",)
        self.box_labin = tk.Label(
            self.box_lab, image = self.box_img2)
        self.box_labin.pack(fill = "both")
        self.box_lab.grid(row=2, column=21, rowspan = 13,
                          columnspan = 10, sticky = "NSEW")



        self.box_interactive = tk.BooleanVar()
        self.interactive_check = ttk.Checkbutton(self.main_frame,
                                       variable = self.box_interactive,
                                       text="Interactive",
                                       onvalue = True,
                                       offvalue = False,
                                       takefocus = 0,
                                       command = self.update_box
                                       )

        self.interactive_check.grid(row=0, column=20, columnspan=7,
                                    rowspan=2, sticky="S")


        ###############################################################
        #####The follwoing lines are exclusive to this butt handling###
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this butt handling###
        ###############################################################
        ###############################################################
        ###############################################################
        #####The follwoing lines are exclusive to this butt handling###
        ###############################################################
        ###############################################################

        self.gridparams["sticky"] = "NSEW"


        #Button that will set all the previous options to defaults.
        s = ttk.Style()
        s.configure("myred_button.TButton", font =self.font,
                    foreground = 'orangered',
                    highlightcolor = "orangered",
                    )
        s.configure("myblue_button.TButton", font =self.font,
                    foreground = 'blue',
                    highlightcolor = "blue",
                    )
        s.configure("mygreen_button.TButton", font =self.font,
                    foreground = 'green',
                    highlightcolor = "green",
                    )
        s.configure("mypurple_button.TButton", font =self.font,
                    foreground = 'purple',
                    highlightcolor = "purple",
                    )

        #Resets current display properties to default
        self.def_but = ttk.Button(
            self.main_frame, text = 'Reset object',
            command = self.reset_entries,
            style = "myred_button.TButton",
            takefocus = 0, width=20
            )

        #Adds object to list of objects
        self.add_but = ttk.Button(
            self.main_frame, text = 'Add object',
            style = "mygreen_button.TButton",
            takefocus = 0, width=20,
            command = self.get_values,
            )

        #Adds object to list of objects
        self.edit_but = ttk.Button(
            self.main_frame, text = 'Edit object',
            command = lambda: \
            self.notebook.select(self.notebook.children[self.edit_frame._name]),
            style = "myblue_button.TButton",
            takefocus = 0, width=20,
            )


        #Update button
        self.update_b = ttk.Button(
            self.main_frame, text = "Update plot",
            style = "mypurple_button.TButton", takefocus = 0,
            width=20, command = self.update_planet,
            )



        self.gridparams["column"]+=3
        self.gridparams["row"]+=-12
        self.gridparams["columnspan"] = 10
        self.gridparams["rowspan"] = 3

        self.update_b.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep
        self.add_but.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep
        self.edit_but.grid(**self.gridparams)
        self.gridparams["row"]+=rowstep
        self.def_but.grid(**self.gridparams)



        ###############################################################
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ############ NOW IT IS TIME TO EDIT SELF.EDIT_FRAME ###########
        ###############################################################
        ###############################################################

        self.tree_frame = tk.Frame(self.edit_frame,)
        self.tree_frame1 = tk.Frame(self.edit_frame,)
        self.tree_frame2 = tk.Frame(self.edit_frame,)

        self.tree_frame.grid(row =0, column=0,
                       rowspan = 28, columnspan=30, sticky ="NSEW")

        self.tree_frame1.grid(row =0, column=30,
                       rowspan = 28, columnspan=1, sticky ="NSEW")
        self.tree_frame2.grid(row =28, column=0,
                       rowspan = 1, columnspan=31, sticky ="NSEW")

        self.tree = ttk.Treeview(self.tree_frame,
                                 columns = (
                                     "Name",
                                     "Color",
                                     "Markersize",
                                     "Ring",
                                     "Charge",
                                     "Velocity",
                                     "Position",
                                     "Mass",
                                     "Marker",
                                     "Orbit",
                                     ),
                                 )
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        #A frame is made to facilitate scaling up and down.
        self.tree.pack(expand = True, fill = "y")

        self.vsb = ttk.Scrollbar(self.tree_frame1,
                            orient="vertical", command=self.tree.yview)
        self.vsb.pack(expand = True, fill = "y")
        self.tree.configure(yscrollcommand=self.vsb.set)

        self.vsb2 = ttk.Scrollbar(self.tree_frame2,
                            orient="horizontal", command=self.tree.xview)
        self.vsb2.pack(expand = True, fill = "x")
        self.tree.configure(xscrollcommand=self.vsb2.set)

        w, wm = 60, 30
        self.tree.column("#0", width =30, minwidth=30, stretch = tk.NO)
        self.tree.column("Name", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Color", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Markersize", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Ring", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Charge", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Velocity", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Position", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Mass", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Marker", width =w, minwidth=wm, stretch = tk.NO)
        self.tree.column("Orbit", width =w, minwidth=wm, stretch = tk.NO)

        self.tree.heading("#0",text="ID",anchor=tk.W)
        self.tree.heading("Name",text="Name",anchor=tk.W)
        self.tree.heading("Color", text="Color",anchor=tk.W)
        self.tree.heading("Markersize", text="Markersize",anchor=tk.W)
        self.tree.heading("Ring", text="Ring",anchor=tk.W)
        self.tree.heading("Charge",text="Chrg",anchor=tk.W)
        self.tree.heading("Velocity", text="Velocity",anchor=tk.W)
        self.tree.heading("Position", text="Position",anchor=tk.W)
        self.tree.heading("Mass", text="Mass",anchor=tk.W)
        self.tree.heading("Marker", text="Marker",anchor=tk.W)
        self.tree.heading("Orbit", text="Orbit",anchor=tk.W)

        self.tree_pop_up = tk.Menu(self, tearoff=0)
        self.tree_pop_up.add_command(label="Delete", command=lambda:
            self.tree.delete(self.tree.selection()[0]))
        self.tree_pop_up.add_command(label = "Orbit", command =  lambda:
            self.set_orbit_relationship())

        self.tree.bind("<Button-3>", self.popup)

        self.del_but = ttk.Button(self.edit_frame,
                                   text = "Delete",
                                   command = self.delete_object,
                                   style = "myred_button.TButton",
                                   takefocus = False)
        self.del_but.grid(
            column=0, row = 29, rowspan=4, columnspan=7, sticky = "NSEW")

        self.orbit_but = ttk.Button(self.edit_frame,
                                    text = "Set orbit",
                                    command = self.set_orbit_relationship,
                                    style = "mypurple_button.TButton",
                                    takefocus = False)
        self.orbit_but.grid(
            column=7, row = 29, rowspan=4, columnspan=7, sticky = "NSEW")

        self.new_object_but = ttk.Button(
            self.edit_frame, text = "Add object",
            style = "myred_button.TButton",
            takefocus = False,
            command = lambda: \
            self.notebook.select(self.notebook.children[self.main_frame._name]),
            )
        self.new_object_but.grid(
            column=14, row = 29, rowspan=4, columnspan=7, sticky = "NSEW")


        self.begin_simulation_but = ttk.Button(
            self.edit_frame, text ="BEGIN",
            takefocus = False, style = "myblue_button.TButton",
            command = self.forward_button['command'],
            )
        self.begin_simulation_but.grid(
            column=21, row = 29, rowspan=4, columnspan=7, sticky = "NSEW")

        self.grid_forget()

    def popup(self, event):
        iid = self.tree.identify_row(event.y)
        if iid:
            # mouse pointer over item
            self.tree.selection_set(iid)
            self.tree_pop_up.post(event.x_root, event.y_root)
        else:
            #No action
            pass

    def get_final_object_dictionary(self):
        """
        Returns a dictionary of planet's, keyworded by their names.
        """
        planet_dictionaries = {}

        for child_id in self.tree.get_children():
            child = self.tree.item(child_id)["values"]
            dictionary = dict(
                name = child[0],
                color = child[1],
                markersize = float(child[2]),
                ring = eval(child[3]),
                total_charge = float(child[4]),
                init_v = np.array(eval(child[5]), dtype = np.float64),
                init_p = np.array(eval(child[6]), dtype = np.float64),
                mass = float(child[7]),
                marker = child[8],
                orbit = child[9],
                )
            planet_dictionaries[dictionary["name"]] = dictionary
        return planet_dictionaries


    def delete_object(self):
        """
        Deletes a row from self.treeview
        """
        try:
            answer = tk.messagebox.askyesno(
                "Warning!", "Are you reaaaaally sure you want to delete this object?")
            self.tree.delete(self.tree.selection()[0]) if answer else None
        except :
            tk.messagebox.showerror(
                "Missing information",
                "If you have already selected a planet and still get this error, contact Pedro."
                )

    def reset_entries(self):
        """
        Reset the interactive entry values to default
        """
        self.type_val.set("Planet")
        self.pc_val.set("Random")
        self.marker_drop.current(0)
        self.ring_val.set(False)
        self.charge_entry.delete(0, tk.END)
        self.charge_entry.insert(0, "0")
        self.rad_m_entry.delete(0, tk.END)
        self.rad_m_entry.insert(0, "1e10")
        self.density_entry.delete(0, tk.END)
        self.density_entry.insert(0, "1e10")
        self.markersize_entry.delete(0, tk.END)
        self.markersize_entry.insert(0, "300")


    def on_tree_select(self, event):
        """
        Gets the selected values of the tree"""
        item = self.tree.selection()[0]
        values = self.tree.item(item,"values")
##        print(values, "Are the values of Item")
        if not hasattr(self, "setting_orbit"):
            """
            This will be deleted after setting orbit"""
            self.currently_selected_object = item
            #Item refers to the ID of th row in the treeview.

    def set_orbit_relationship(self):
        """
        This function interacts with on_tree_select()
        to stabilish orbits between two objects or more.
        It works like this...
        You press a row that has a planet that you wish to orbit another planet.
        Then you press the button to "set" orbit.
        Then you press the planet that you want to be the center of the orbit.
        Then you press the button to set the orbit again!
        """
        if not hasattr(self, "currently_selected_object"):
            tk.messagebox.showwarning(
                "Problem Sir.", "You must select the object that will orbit the other object.")
            return
        else:
            if not hasattr(self, "setting_orbit"):
                self.setting_orbit = True
                self.orbit_but.config(text="Select obj\nto orbit")
                return
            else:
                to_set_in_orbit = self.tree.item(self.currently_selected_object,"values")
                to_be_in_center = self.tree.item(self.tree.selection()[0],"values")
                answer = tk.messagebox.askyesno("Question","Are you sure you want to set this orbit?")
                if answer and to_set_in_orbit[0]!=to_be_in_center[0]:
                    to_set_in_orbit = list(to_set_in_orbit)
                    to_set_in_orbit[-1] = to_be_in_center[0]
                    print(to_be_in_center[0], "will be the center")
                    to_set_in_orbit = tuple(to_set_in_orbit)
                    print("updated tuple", to_set_in_orbit)
                    self.tree.item(self.currently_selected_object,
                                   values = to_set_in_orbit)
                    del self.currently_selected_object
                    del self.setting_orbit
                    tk.messagebox.showinfo(
                        "Success", f"{to_set_in_orbit[0]} now orbits {to_set_in_orbit[-1]}")
                    self.orbit_but.config(text="Set orbit")
                else:
                    answer = tk.messagebox.askyesno("Question","Do you want to stop setting this orbit?")
                    if answer:
                        del self.currently_selected_object
                        del self.setting_orbit
                        self.orbit_but.config(text="Set orbit")




    def get_values(self):
        """
        Get the inputs of all widgets and place them in
        a dictionary.
        AALLL Units are converted to STI using a dictionary
        made in PAGES.py
        Then it adds that dictionary to the treeview.
        """
        try:
            if not hasattr(self, "i"):
                self.i = 0
            dictionary = self.get_dict_from_inputs()
            self.tree.insert("", "end", text = f"{self.i}".strip(),
                             values = (
                f"{dictionary['category']}_{self.i}",
                f"{dictionary['color']}",
                f"{dictionary['markersize']}",
                f"{dictionary['ring']}",
                f"{dictionary['total_charge']}",
                f"{dictionary['init_v']}",
                f"{dictionary['init_p']}",
                f"{dictionary['mass']}",
                f"{dictionary['marker']}",
                "None...Yet"))
            self.i+=1
            tk.messagebox.showinfo("Success",
                                   "Object was successfuly added ☻",)
        except: None

    def get_dict_from_inputs(self):
        """Does not add the dictionary to the treeview."""
        conversions = self.__class__.conversions
        init_v, init_p = [],[]
        for key in "x y z".split():
            init_v.append(float(self.v_entries[key].get())
                          if self.v_entries[key].get().isnumeric()
                          else 0)
            init_p.append(float(self.p_entries[key].get())
                          if self.p_entries[key].get().isnumeric()
                          else 0)

        i = self.__class__.instances["page1"].num_dims.get()

        init_v = (np.array(init_v[:i])*conversions[self.units_v.get()]).tolist()
        init_p = (np.array(init_p[:i])*conversions[self.units_p.get()]).tolist()

        color = (np.random.choice(self.all_colors)
                 if self.pc_val.get() == "random"
                 else self.pc_val.get())
        try:
            if self.rm_val.get() == "Mass":
                mass = float(self.rad_m_entry.get())*conversions[self.units_rm.get()]
            else:
                mass = 4/3*np.pi*float(self.density_entry.get())*(float(self.rad_m_entry.get())**3)
                mass = mass*conversions[self.units_den_val.get()]*conversions[self.units_rm.get()]
            if self.charge_type.get() == "Chrg density":
                total_charge = mass*float(self.charge_entry.get())*conversions[self.units_cd.get()]
            else:
                total_charge = float(self.charge_entry.get())*conversions[self.units_cd.get()]
            dictionary = dict(
                name = f"{self.type_val.get()}_{self.i}",
                total_charge = total_charge,
                mass = mass,
                category = self.type_val.get(),
                color = color,
                marker = self.marker_drop.get(),
                ring = self.ring_val.get(),
                init_v = init_v, init_p = init_p,
                markersize = self.markersize_entry.get(),
                )
            return dictionary
        except:
            tk.messagebox.showwarning(
                "PROBLEM", "You did not complete all fields. ⚠")



    def update_planet(self):
        if hasattr(self, "canvas"):
            color = self.pc_val.get()
            marker = self.marker_drop.get()
            if color == "random":
                color = np.random.choice(self.all_colors)
            if marker not in self.markers:
                if marker[0]!="$":
                    if marker == "random":
                        marker = np.random.choice(self.markers)
                    elif marker not in self.markers:
                        marker = "o"

            if self.ring_val.get():
                for planet_ring in self.rings:
                    planet_ring.set_visible(True)
            else:
                 for planet_ring in self.rings:
                    planet_ring.set_visible(False)

            self.sunline.set(color = color, marker = marker)
            #Self.sunline is defined in Dir1_1/box.py
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()



    def update_box(self):
        if self.box_interactive.get():
            self.delete_canvas()#Just a check
            make_box_interactive(self)
        else:
            plt.close("all")
            self.delete_canvas()



    def give_function_to_help_bs(self):
        """
            This function will provide the information about each
            entry in the form of tkinter messageboxes.

            Help buttons follow the following name system:
            name(x) = help_b{x}

            where x goes from 0 till n, where n is the number of
            help buttons in the page.

            0 is to top help button.

            It uses premade messages that come from
            messages.py
            """
        mess = page1_1messages
        command = lambda x: lambda : tk.messagebox.showinfo(
                                        "Helpful information", mess[x])
        for x in range(10):
            button = getattr(self, f"help_b{x}")
            button.config(
                command = command(x)
                )




if __name__ == "__main__":
    """This part is just for testing"""
    from Page4 import Page4
    window = tk.Tk()
    main_page = Main_page(window)
    page1 = Page1(window)
    page1_1 = Page1_1(window)
    #page4 = Page4(window)
    window.mainloop()
