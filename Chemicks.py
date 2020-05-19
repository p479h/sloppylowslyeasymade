"""
This app allows you to calculate the molar mass of molecules where the numbers go up to 2 beggining_of_double_digits
Have fun using it in the lab!

----------------------------------
Each section has a function, and they are separated by ###########

---------------------------------
Now, go explore!
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import os
directory = os.getcwd() + r'\Benzenechemapp.PNG'


class back_ground(tk.Canvas):
    """This part of the code creates the background of the program"""

    def __init__(self, master=None, **kwargs):
        proportion = 100
        super().__init__(master, **kwargs)
        w = int(proportion*1.2)*5
        h = proportion*4
        self.image = Image.open(directory).resize((w, h), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        master.geometry(f"{w}x{h}+0+0")
        frame_background = tk.Label(master, image=self.image).place(x=0, y=0)


def check_indexes(chemical):
    """This function takes in a chemical formula as a string
    2 examples: CH3(NH2)2CH3 and C12H16O7. These formulas then
    have the indexes of numbers, parenthesis upper and lower cases
    and organizes them in lists that are later used to determine
    the molecular mass of the molecule.
    ATENTION: All the numbers in the chemical formula must contain
    2 digits OR LESS."""
    upper_index = []
    lower_index = []
    open_index = []
    close_index = []
    number_index = []
    for index, letter in enumerate(chemical):
        if letter.isupper():
            upper_index.append(index)
        elif letter.islower():
            lower_index.append(index)
        elif letter.isnumeric():
            number_index.append(index)
        elif letter == '(' or letter == ')':
            open_index.append(index) if letter == '(' else close_index.append(index)
        else:
            print('Please input something else')
    return (upper_index, lower_index, open_index, close_index, number_index)


def find_double_numbers_and_double_lowers(number_index, lower_index):
    """This function takes in the list of indexes of numbers and lowercases.
    These are used to get labels to places in the chemical formula where there
    are consecutive letters or lower digits. The lower digits were a mistake.
    But fixing it won't change the function's performance."""
    beggining_of_double_digits = []
    beggining_of_double_lowers = []
    for index1, index2 in enumerate(number_index):
        if index2-number_index[index1-1] == 1:
            beggining_of_double_digits.append(number_index[index1-1])
    for index1, index2 in enumerate(lower_index):
        if index2-lower_index[index1-1] == 1:
            beggining_of_double_lowers.append(lower_index[index1-1])
    return (beggining_of_double_digits, beggining_of_double_lowers)


def make_list_of_within_parenthesis(chemical, open_index, close_index):
    """This function gets all the chemical structures insise parenthesis.
    Their counts will be obtained in another function.
    NOTE: If there are parenthesis inside parenthesis. They function WILL NOT work."""
    list_of_parenthesis = []
    for index in zip(open_index, close_index):
        list_of_parenthesis.append(chemical[index[0]+1:index[1]])
    return list_of_parenthesis


def check_in_parenthesis_count(chemical, close_index):  # This is the new improved function still under tests/
    """It is not known yet if this function performs correctly 100% of the time. More updates needed."""
    ammount_in_parenthesis = []
    for x in close_index:
        if x <= len(chemical)-3:
            if chemical[x+1].isupper():
                ammount_in_parenthesis.append(1)
            elif chemical[x+1] == '(':
                ammount_in_parenthesis.append(1)
            elif chemical[x+1] == ')':
                print('You have made a terrible spelling mistake .|. ')
            elif chemical[x+1].isnumeric():
                if chemical[x+2].isnumeric():
                    ammount_in_parenthesis.append(int(chemical[x+1:x+3]))
                else:
                    ammount_in_parenthesis.append(int(chemical[x+1]))
        elif x == len(chemical)-2:
            if chemical[x+1].isupper():
                ammount_in_parenthesis.append(1)
            elif chemical[x+1].isnumeric():
                ammount_in_parenthesis.append(int(chemical[x+1]))

        elif x == len(chemical)-1:
            ammount_in_parenthesis.append(1)
        else:
            print('Problem with indexing')
    return ammount_in_parenthesis


def get_word_no_parenthesis(chemical, open_index, close_index, upper_index, number_index, beggining_of_double_digits):
    """This function 'cleans' the string containing the structural formula.
    It removes the parenthesis and numbers related to them."""
    clean_chemical = ''
    official_ends = []
    for index in close_index:
        if index <= len(chemical)-3:  # Searching if the we still have 2 or more  things after the closing parenthesis
            if (index+1 in upper_index) or (index+1 in open_index):
                if chemical[index]:
                    official_ends.append(index)
                else:
                    print('line 88')

            elif (index+1 in number_index) and (index+1 not in beggining_of_double_digits):
                if chemical[index+1]:
                    official_ends.append(index+1)
                else:
                    print('line 94')
            elif (index+1 in number_index) and (index+1 in beggining_of_double_digits):
                if chemical[index+2]:
                    official_ends.append(index+2)
                else:
                    print('line 99')
            elif (index+1 in open_index):
                official_ends.append(index)
            else:
                print('Missing scenario at get_word_no_parenthesis line 103')

        elif index == len(chemical)-2:  # Searching if we still have 1 thing after the closing parenthesis
            if index+1 in upper_index:
                official_ends.append(index)
            elif index+1 in number_index:
                official_ends.append(index+1)
        elif index == len(chemical)-1:  # Searching if there is nothing after the parenthesis
            official_ends.append(index)
        else:
            print('Something wronng with conditions in get_word_no_parenthesis line 114')

    ranges = []
    if len(official_ends) != len(open_index):
        print('GO BACK TO LINE 108. It appears there is some sort of error in this function.')

    for index, index2 in zip(open_index, official_ends):
        ranges += [ind for ind in range(index, index2+1)]

    for index, letter in enumerate(chemical):
        if index not in ranges:
            clean_chemical += letter
    return clean_chemical


def find_atomic_ammounts(clean_chemical):
    """This is the heart of the operation. It brings the other functions
    together to count the number of atoms in the structure. The reason
    this is the heart of the operation is that it is difficilt to teach
    a program to know where an atom beings, ends, and attributing a number
    to it."""
    upper_index, lower_index, open_index, close_index, number_index = check_indexes(clean_chemical)  # These are needed here. So they must be redefined
    beggining_of_double_digits, beggining_of_double_lowers = find_double_numbers_and_double_lowers(number_index, lower_index)
    index = 0
    Atoms = []
    Atoms_count = []
    while index < len(upper_index):
        single_upper = ((upper_index[index]+1) in upper_index)
        upper_and_1_lower = (upper_index[index]+1 in lower_index) and (upper_index[index]+2 in upper_index)
        upper_and_2_lower = (upper_index[index]+1 in beggining_of_double_lowers) and (upper_index[index]+3 in upper_index)
        upper_1_number = (upper_index[index]+1 in number_index) and (upper_index[index]+2 in upper_index)
        upper_2number = (upper_index[index]+1 in beggining_of_double_digits)
        upper_and_1_lower_1_number = (upper_index[index]+1 in lower_index) and (upper_index[index]+2 not in beggining_of_double_digits) and (upper_index[index]+2 in number_index)
        upper_and_1_lower_2_number = (upper_index[index]+1 in lower_index) and (upper_index[index]+2 in beggining_of_double_digits)
        upper_and_2_lower_1_number = (upper_index[index]+1 in beggining_of_double_lowers) and (upper_index[index]+3 in number_index) and (upper_index[index]+3 not in beggining_of_double_digits)
        upper_and_2_lower_2_number = (upper_index[index]+1 in beggining_of_double_lowers) and (upper_index[index]+3 in beggining_of_double_digits)
        Short_hand = upper_index[index]
        if single_upper:
            Atoms.append(clean_chemical[Short_hand])
            Atoms_count.append(int(1))
            index += 1
        elif upper_and_1_lower:
            Atoms.append(clean_chemical[Short_hand:Short_hand+2])
            Atoms_count.append(int(1))
            index += 1
        elif upper_and_2_lower:
            Atoms.append(clean_chemical[Short_hand:Short_hand+3])
            Atoms_count.append(int(1))
            index += 1
        elif upper_1_number:
            Atoms.append(clean_chemical[Short_hand])
            Atoms_count.append(int(clean_chemical[Short_hand+1]))
            index += 1
        elif upper_2number:
            Atoms.append(clean_chemical[Short_hand])
            Atoms_count.append(int(clean_chemical[Short_hand+1:Short_hand+3]))
            index += 1
        elif upper_and_1_lower_1_number:
            Atoms.append(clean_chemical[Short_hand:Short_hand+2])
            Atoms_count.append(int(clean_chemical[Short_hand+2]))
            index += 1
        elif upper_and_1_lower_2_number:
            Atoms.append(clean_chemical[Short_hand:Short_hand+2])
            Atoms_count.append(int(clean_chemical[Short_hand+2:Short_hand+4]))
            index += 1
        elif upper_and_2_lower_1_number:
            Atoms.append(clean_chemical[Short_hand:Short_hand+3])
            Atoms_count.append(int(clean_chemical[Short_hand+3]))
            index += 1
        elif upper_and_2_lower_2_number:
            Atoms.append(clean_chemical[Short_hand:Short_hand+3])
            Atoms_count.append(int(clean_chemical[Short_hand+3:Short_hand+5]))
            index += 1

        else:
            if Short_hand == len(clean_chemical)-3:
                if clean_chemical[Short_hand+1].isnumeric() and not clean_chemical[x+2].isnumeric():
                    Atoms.append(clean_chemical[Short_hand])
                    Atoms_count.append(int(clean_chemical[Short_hand+1]))
                    index += 1
                elif clean_chemical[Short_hand+1].isnumeric() and clean_chemical[x+2].isnumeric():
                    Atoms.append(clean_chemical[Short_hand])
                    Atoms_count.append(int(clean_chemical[Short_hand+1:Short_hand+3]))
                    index += 1
                elif clean_chemical[Short_hand+1].islower():
                    if clean_chemical[Short_hand+2].isnumeric():
                        Atoms.append(clean_chemical[Short_hand:Short_hand+2])
                        Atoms_count.append(int(clean_chemical[Short_hand+2]))
                        index += 1
                    elif clean_chemical[Short_hand+2].islower():
                        Atoms.append(clean_chemical[Short_hand:Short_hand+3])
                        Atoms_count.append(1)
                        index += 1
                else:
                    print('condition missing in line 223')
                    index += 1
            elif Short_hand == len(clean_chemical)-2:
                if clean_chemical[Short_hand+1].islower():
                    Atoms.append(clean_chemical[Short_hand:Short_hand+2])
                    Atoms_count.append(1)
                    index += 1
                elif clean_chemical[Short_hand+1].isnumeric():
                    Atoms.append(clean_chemical[Short_hand])
                    Atoms_count.append(int(clean_chemical[Short_hand+1]))
                    index += 1
            elif Short_hand == len(clean_chemical)-1:
                Atoms.append(clean_chemical[Short_hand])
                Atoms_count.append(1)
                index += 1
            else:
                print('FIX FUNC line 212')
                index += 1

    return Atoms, Atoms_count


def add_parenthesis_to_Atoms(Atoms, Atoms_count, list_of_parenthesis, ammount_in_parenthesis):
    """This function processes the chemical formulas inside parenthesis,
    adding them to the Atoms list."""
    updated_Atoms = []
    updated_Atoms_count = []
    updated_Atoms += Atoms
    updated_Atoms_count += Atoms_count
    for paren, ammou in zip(list_of_parenthesis, ammount_in_parenthesis):
        add_to_atoms, add_to_counts = find_atomic_ammounts(paren)
        add_to_counts = [x*ammou for x in add_to_counts]
        updated_Atoms += add_to_atoms
        updated_Atoms_count += add_to_counts
    return updated_Atoms, updated_Atoms_count


def get_molecular_mass(chemical):
    """This function brings all other functions together"""
    upper_index, lower_index, open_index, close_index, number_index = check_indexes(chemical)
    beggining_of_double_digits, beggining_of_double_lowers = find_double_numbers_and_double_lowers(number_index, lower_index)
    ammount_in_parenthesis = check_in_parenthesis_count(chemical, close_index)
    list_of_parenthesis = make_list_of_within_parenthesis(chemical, open_index, close_index)
    clean_chemical = get_word_no_parenthesis(chemical, open_index, close_index, upper_index, number_index, beggining_of_double_digits)
    Atoms, Atoms_count = find_atomic_ammounts(clean_chemical)
    # print(f'Chemical: {chemical}\nList in Parenthesis: {list_of_parenthesis}\nAmmount in parenthesis: {ammount_in_parenthesis}\nClean_chemical: {clean_chemical}')
    # print(f'Atoms: {Atoms}, Atomic_counts: {Atoms_count}')
    mol_masses = {'H': 1.00794, 'He': 4.002602, 'Li': 6.941, 'Be': 9.012182, 'B': 10.811, 'C': 12.0107, 'N': 14.0067,
                  'O': 15.9994, 'F': 18.9984032, 'Ne': 20.1797, 'Na': 22.98976928, 'Mg': 24.305, 'Al': 26.9815386,
                  'Si': 28.0855, 'P': 30.973762, 'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.0983, 'Ca': 40.078,
                  'Sc': 44.955912, 'Ti': 47.867, 'V': 50.9415, 'Cr': 51.9961, 'Mn': 54.938045,
                  'Fe': 55.845, 'Co': 58.933195, 'Ni': 58.6934, 'Cu': 63.546, 'Zn': 65.409, 'Ga': 69.723, 'Ge': 72.64,
                  'As': 74.9216, 'Se': 78.96, 'Br': 79.904, 'Kr': 83.798, 'Rb': 85.4678, 'Sr': 87.62, 'Y': 88.90585,
                  'Zr': 91.224, 'Nb': 92.90638, 'Mo': 95.94, 'Tc': 98.9063, 'Ru': 101.07, 'Rh': 102.9055, 'Pd': 106.42,
                  'Ag': 107.8682, 'Cd': 112.411, 'In': 114.818, 'Sn': 118.71, 'Sb': 121.760, 'Te': 127.6,
                  'I': 126.90447, 'Xe': 131.293, 'Cs': 132.9054519, 'Ba': 137.327, 'La': 138.90547, 'Ce': 140.116,
                  'Pr': 140.90465, 'Nd': 144.242, 'Pm': 146.9151, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25,
                  'Tb': 158.92535, 'Dy': 162.5, 'Ho': 164.93032, 'Er': 167.259, 'Tm': 168.93421, 'Yb': 173.04,
                  'Lu': 174.967, 'Hf': 178.49, 'Ta': 180.9479, 'W': 183.84, 'Re': 186.207, 'Os': 190.23, 'Ir': 192.217,
                  'Pt': 195.084, 'Au': 196.966569, 'Hg': 200.59, 'Tl': 204.3833, 'Pb': 207.2, 'Bi': 208.9804,
                  'Po': 208.9824, 'At': 209.9871, 'Rn': 222.0176, 'Fr': 223.0197, 'Ra': 226.0254, 'Ac': 227.0278,
                  'Th': 232.03806, 'Pa': 231.03588, 'U': 238.02891, 'Np': 237.0482, 'Pu': 244.0642, 'Am': 243.0614,
                  'Cm': 247.0703, 'Bk': 247.0703, 'Cf': 251.0796, 'Es': 252.0829, 'Fm': 257.0951, 'Md': 258.0951,
                  'No': 259.1009, 'Lr': 262, 'Rf': 267, 'Db': 268, 'Sg': 271, 'Bh': 270, 'Hs': 269, 'Mt': 278,
                  'Ds': 281, 'Rg': 281, 'Cn': 285, 'Nh': 284, 'Fl': 289, 'Mc': 289, 'Lv': 292, 'Ts': 294, 'Og': 294,
                  'ZERO': 0}
    cummulative_mass = 0
    Atoms, Atoms_count = add_parenthesis_to_Atoms(Atoms, Atoms_count, list_of_parenthesis, ammount_in_parenthesis)
    if len(Atoms) != len(Atoms_count):
        print('The lengths of atoms\'s list and their respective counts\'s list are different')
    for atom, count in zip(Atoms, Atoms_count):
        if atom in mol_masses:
            cummulative_mass += float(count)*float(mol_masses[atom])

        else:
            print('This atom does not exist')
    return round(cummulative_mass, 2)


##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


class concentration_frame(tk.Frame):
    """Creates a frame in a  window/root.
    This frame contains the skeleton of the application
    Functions related to the GUI-function interactions
    are also here."""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.config(height=180, width=400)
        y_line1 = 40
        y_line2 = 100
        self.units = 'g'
        self.label_chemical = tk.Label(self, text='Chem formula\n   or   \nMolec mass', font=('TkDefaultFont', 9))
        self.label_chemical.place(y=y_line1-19, x=1)

        self.entry_chemical = tk.Entry(self, width=10)
        self.entry_chemical.place(y=y_line1, x=90)

        self.label_volume = tk.Label(self, text='Volume')
        self.label_volume.place(y=y_line1, x=250)

        self.entry_volume = tk.Entry(self, width=5)
        self.entry_volume.place(y=y_line1, x=300)

        self.unit_volume = tk.StringVar(self)
        self.unit_volume.set('l')

        self.option_unit_volume = tk.OptionMenu(self, self.unit_volume, "l", "ml")  # GET FROM HERE LATER
        self.option_unit_volume.place(y=y_line1-10, x=340)

        self.label_concentration = tk.Label(self, text='Concentration')
        self.label_concentration.place(x=1, y=y_line2)

        self.entry_concentration = tk.Entry(self, width=5)
        self.entry_concentration.place(x=90, y=y_line2)

        self.unit_concentration = tk.StringVar(self)
        self.unit_concentration.set('mol/l')

        self.option_unit_concentration = tk.OptionMenu(self, self.unit_concentration, "mol/l", "mmol/l")  # GET FROM HERE LATER
        self.option_unit_concentration.place(y=y_line2-5, x=130)

        self.button_calculate_ammount = tk.Button(self, text='Calculate :)', command=self.find_ammounts_chemical, width=10)
        self.button_calculate_ammount.place(y=y_line2-5, x=220)

        self.label_result = tk.Label(self, text='')
        self.label_result.place(y=y_line2-5, x=325)

        self.multiplier_button = tk.Button(self, text='Calculate :)', command=self.multiplier)
        self.multiplier_button.place(y=y_line2+45, x=175)

        self.multiplier_label = tk.Label(self, text='Input expression\nthat multiplies\nrequired ammount.', font=('TkDefaultFont', 7))
        self.multiplier_label.place(y=y_line2+40, x=4)

        self.multiplier_entry = tk.Entry(self, width=9)
        self.multiplier_entry.place(y=y_line2+50, x=100)

        self.multiplier_result = tk.Label(self, text='')
        self.multiplier_result.place(y=y_line2+50, x=265)

        # Here we can add an option using the density to give the Volume
    def multiplier(self):
        try:
            unit_vol = self.unit_volume.get()
            unit_concentration = self.unit_concentration.get()
            chemical, final_vol, concentration = (self.entry_chemical.get(), self.entry_volume.get(), self.entry_concentration.get())
            constant = float(eval(self.multiplier_entry.get()))

            try:
                ammount_chemical = float(concentration) * float(final_vol)
                if chemical.isnumeric():
                    mass_chemical = float(chemical)*float(ammount_chemical)
                else:
                    mass_chemical = get_molecular_mass(chemical)*float(ammount_chemical)
                if unit_vol == 'ml':
                    mass_chemical = mass_chemical/1000
                if unit_concentration == 'mmol/l':
                    mass_chemical = mass_chemical/1000
                self.multiplier_result['text'] = str(round(mass_chemical*constant, 7))+' '+self.units

            except:
                messagebox.showwarning('You messed up', 'As you just read:\nYou messed up.\nPlease imput numbers that make sense')

        except:
            messagebox.showwarning('Please input something.', 'You heard the title. Please input something')

    def find_ammounts_chemical(self):
        """This function takes in a chemical formula and other parameters
        from the entries and organizes the actions that follow"""
        unit_vol = self.unit_volume.get()
        unit_concentration = self.unit_concentration.get()
        chemical, final_vol, concentration = (self.entry_chemical.get(), self.entry_volume.get(), self.entry_concentration.get())
        try:
            if (int(self.entry_chemical.get()), int(self.entry_volume.get()), int(self.entry_concentration.get())) == (69, 69, 69):
                messagebox.showwarning('You have unlocked the secret message', 'Secret message/interesting title .|.')
        except:
            pass
        try:
            ammount_chemical = float(concentration) * float(final_vol)
            if chemical.isnumeric():
                mass_chemical = float(chemical)*float(ammount_chemical)
            else:
                mass_chemical = get_molecular_mass(chemical)*float(ammount_chemical)
            if unit_vol == 'ml':
                mass_chemical = mass_chemical/1000
            if unit_concentration == 'mmol/l':
                mass_chemical = mass_chemical/1000
            self.label_result['text'] = str(round(mass_chemical, 7))+' '+self.units

        except:
            messagebox.showwarning('You messed up', 'As you just read:\nYou messed up.\nPlease imput numbers that make sense')


def main_concentration():
    """This function creates the initial window"""
    window = tk.Tk()
    window.title('Having fun yet? :)')
    picture = back_ground(window)
    picture.pack()
    frame = concentration_frame(window)
    frame.place(x=0, y=0)
    window.mainloop()


##########################################################################################################
##########################################################################################################
##########################################################################################################
###########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

"""This document contains the app that gives moleculas mass from molecular formula
it requires Improved_functions_to_get_molar_mass to be in the same directory."""


class GUI(tk.Frame):
    """This class contains the frame that contrains all the buttons of the application
    This application gives molecular mass from molecular formula."""
    proportion = 100
    units = 'g/mol'

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        proportion = 100
        self.columnconfigure([0, 2], weight=0, minsize=proportion)
        self.columnconfigure([1, 3], weight=0, minsize=proportion/2)
        self.rowconfigure([1], weight=0, minsize=proportion)

        introduction = tk.Label(self, text='Wellcome to the molecular mass calculator\nInput a simple molecular formula with digit numbers')
        introduction.grid(column=0, row=0, columnspan=3, sticky='w')

        label1 = tk.Label(self, text='Simplified molecular formula:')
        label1.grid(column=0, row=1)
        self.entry1 = tk.Entry(self)
        self.entry1.grid(column=1, row=1)

        button1 = tk.Button(self, text='Calc', command=self.give_result)
        button1.grid(column=2, row=1)
        self.label2 = tk.Label(self, text='')
        self.label2.grid(column=3, row=1)

        button2 = tk.Button(self, text='Calc', command=self.give_results)
        button2.grid(column=2, row=3)

        label_counts = tk.Label(self, text='Amount of this molecule:')
        label_counts.grid(column=0, row=3)

        self.entry_counts = tk.Entry(self)
        self.entry_counts.grid(column=1, row=3)

        self.result_mult = tk.Label(self, text='')
        self.result_mult.grid(column=3, row=3)

        test_label = tk.Button(self, text='Press me\nTo change\nunits', command=self.change_units)
        test_label.place(x=370, y=1)
        # test_label.bind('<Button-1>', self.change_units)

    def check_for_entry(self, ent):
        if not ent:
            messagebox.showwarning('Warning', 'You need to imput something :)')

    def give_result(self):
        """Gives result of computation of molecular mass using the moleculas formula from the entry1"""
        try:
            ent = self.entry1.get()
            total = get_molecular_mass(ent)
            if GUI.units == 'g/mol':
                self.label2['text'] = str(total) + ' '+GUI.units
            else:
                self.label2['text'] = str(total/1000) + ' '+GUI.units
        except:
            self.check_for_entry(self.entry1.get())

    def give_results(self):
        """This function displays the results in the GUI interface"""
        try:
            ent = self.entry1.get()
            ent2 = float(self.entry_counts.get())
            total = get_molecular_mass(ent)
            if GUI.units == 'g/mol':
                self.result_mult['text'] = str(round(total*ent2, 2)) + ' ' + GUI.units
            else:
                self.result_mult['text'] = str(round(total*ent2/1000, 6)) + ' ' + GUI.units
        except:
            try:
                self.check_for_entry(self.entry1.get())
            except:
                self.check_for_entry(self.entry_counts.get())

    def change_units(self):
        """This function changes the units of the output using inputs"""
        if GUI.units == 'g/mol':
            GUI.units = 'kg/mol'
            messagebox.showinfo('JK', f'This is still experimental. \nYour new units are: {GUI.units}')
        else:
            GUI.units = 'g/mol'
            messagebox.showinfo('JK', f'This is still experimental. \nYour new units are: {GUI.units}')


def main():
    root = tk.Tk()
    root.title('Predro Molecular mass calculator')
    picture = back_ground(root)
    picture.pack()
    window = GUI(master=root)
    window.place(x=10, y=10)
    root.mainloop()


##########################################################################################################
##########################################################################################################
##########################################################################################################
################################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

class Opening(tk.Frame):
    """This class contains the buttons that can take you to another app"""

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg='blue')

        button_open_converter_improved = tk.Button(self, text='Calculate molar mass from molecule-BETA', command=self.open_improved_converter)
        button_open_converter_improved.pack()
        button_open_making_solution_helper = tk.Button(self, text='Get the ammounts needed for solution', command=self.open_concentrations)
        button_open_making_solution_helper.pack()

    @staticmethod
    def open_improved_converter():
        global to_open
        to_open = 'open_improved_converter'
        window.destroy()

    @staticmethod
    def open_concentrations():
        global to_open
        to_open = 'open_concentrations'
        window.destroy()


"""The next part, when run, opens the opnening page and from there, the subsequent pages."""

window = tk.Tk()
picture = back_ground(window)
picture.pack()
window.title('The best app ever :)')
Initial_frame = Opening(window)
Initial_frame.place(x=0, y=0)
window.mainloop()

try:
    if to_open == 'open_improved_converter':
        main()
    elif to_open == 'open_concentrations':
        main_concentration()
except:
    print('Too bad you did not press any buttons :(')
