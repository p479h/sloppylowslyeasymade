from tkinter import messagebox
import tkinter
from tkinter import *


def get_parenthesis_index(chemical):
    global closing_index
    global opening_index
    opening_index = []
    closing_index = []
    for index, letter in enumerate(chemical):
        if letter == '(':
            opening_index.append(index)
        elif letter == ')':
            closing_index.append(index)
    # print(f'opening: {opening_index}\nclosing: {closing_index}')
    #
    # print(f'This is the chemical: {chemical}')


def check_in_parenthesis_count(chemical, closing_index):
    global ammount_in_parenthesis
    global index_of_ammounts
    ammount_in_parenthesis = []
    index_of_ammounts = []
    for index, letter in enumerate(chemical):
        if index in closing_index:
            try:
                if chemical[index+1].isdigit():
                    ammount_in_parenthesis.append(int(chemical[index+1]))
                    index_of_ammounts.append(index+1)
            except:
                ammount_in_parenthesis.append(1)
                index_of_ammounts.append(None)
    # print(f'ammount in parenthesis: {ammount_in_parenthesis}\nindex of ammount: {index_of_ammounts}')


def get_word_no_parenthesis(chemical, opening_index, closing_index, index_of_ammounts):
    global clean_chemical
    global ranges
    clean_chemical = ''
    ranges = []
    for index, index2 in enumerate(closing_index):
        ranges += [ind for ind in range(opening_index[index], index2+1)]

    for index, letter in enumerate(chemical):
        if index not in ranges:
            try:
                if chemical[index-1] == ')' and not chemical[index].isdigit():
                    clean_chemical += letter
                elif chemical[index-1] == ')' and chemical[index].isdigit():
                    pass
                else:
                    clean_chemical += letter

            except:
                print('EXCEPTION WAS RAISED IN GET WORD NO PARENTHESIS')

    # print(ranges)

    # print(f'Chemical without parenthesis:{clean_chemical}')


def make_list_of_within_parenthesis(chemical, opening_index, closing_index):
    global list_of_parenthesis
    list_of_parenthesis = []
    for index in zip(opening_index, closing_index):
        list_of_parenthesis.append(chemical[index[0]+1:index[1]])
    # print(list_of_parenthesis)


def find_atomic_ammounts(clean_chemical):
    global list_of_elements
    global list_of_ammounts
    list_of_elements = []
    list_of_ammounts = []
    index_of_capitals = []
    for index, letter in enumerate(clean_chemical):
        if letter.isupper():
            index_of_capitals.append(index)
    for index in index_of_capitals:
        try:
            if clean_chemical[index+1].islower() and clean_chemical[index+2].isupper():
                list_of_elements.append(clean_chemical[index:index+2])
                list_of_ammounts.append(1)
            elif clean_chemical[index+1].islower() and clean_chemical[index+2].isdigit():
                list_of_elements.append(clean_chemical[index:index+2])
                list_of_ammounts.append(int(clean_chemical[index+2]))
            elif clean_chemical[index+1].isupper() and clean_chemical[index+1].isupper():
                list_of_elements.append(clean_chemical[index])
                list_of_ammounts.append(1)
            elif clean_chemical[index+1].isdigit():
                list_of_elements.append(clean_chemical[index])
                list_of_ammounts.append(int(clean_chemical[index+1]))

        except:
            try:  # THIS IS FOR THE elements with 2 letters
                if clean_chemical[index+1].islower():
                    list_of_elements.append(clean_chemical[index:index+2])
                    list_of_ammounts.append(1)
                elif clean_chemical[index+1].isdigit():
                    list_of_elements.append(clean_chemical[index])
                    list_of_ammounts.append(int(clean_chemical[index+1]))
            except:
                list_of_elements.append(clean_chemical[index])
                list_of_ammounts.append(1)
    # print(f'list el{list_of_elements}\nammounts{list_of_ammounts}')


# test = 'CH3(CH3)2CBrH5(CH4)3O7Br2'
# get_parenthesis_index(test)
# check_in_parenthesis_count(test, closing_index)
# get_word_no_parenthesis(test, opening_index, closing_index, index_of_ammounts)
# make_list_of_within_parenthesis(test, opening_index, closing_index)
# find_atomic_ammounts(clean_chemical)

def get_molecular_mass(molecule):
    get_parenthesis_index(molecule)  # Obtains the indexes of begginings and endings of parenthesis as lists: opening_index, closing_index
    check_in_parenthesis_count(molecule, closing_index)  # Checks how much of each molecule inside parenthesis there are. It outputs it as ammount_in_parenthesis
    get_word_no_parenthesis(molecule, opening_index, closing_index, index_of_ammounts)  # Obtains the chemical without parenthesis, named as clean_molecule
    make_list_of_within_parenthesis(molecule, opening_index, closing_index)  # makes a list with everything that is inside the parenthesis. Its name is list_of_parenthesis
    global list_of_parenthesis
    global ammount_in_parenthesis
    list_of_parenthesis += [clean_chemical]
    ammount_in_parenthesis += [1]
    # print(list_of_parenthesis, ammount_in_parenthesis)
    global atoms
    global ammount_of_atoms
    atoms = []
    ammount_of_atoms = []
    for index, clean_chem in enumerate(list_of_parenthesis):
        find_atomic_ammounts(clean_chem)
        atoms += list_of_elements
        ammount_of_atoms += [x*ammount_in_parenthesis[index] for x in list_of_ammounts]
    # print(f'Atoms:{atoms}\nAtomic_counts{ammount_of_atoms}\nlengths: {len(atoms)} and {len(ammount_of_atoms)}')
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
                  'Cm': 247.0703, 'Bk': 247.0703, 'Cf': 251.0796}
    cummulative_mol_mass = 0
    for index, atom in enumerate(atoms):
        cummulative_mol_mass += mol_masses[atom]*int(ammount_of_atoms[index])
    cummulative_mol_mass = round(cummulative_mol_mass, 2)
    return cummulative_mol_mass


# get_molecular_mass('H3(PO4)2')

def check_for_entry(ent):
    if not ent:
        messagebox.showwarning('Warning', 'You need to imput something :)')


def give_result():
    try:
        ent = entry1.get()
        total = get_molecular_mass(ent)
        label2['text'] = str(total) + 'g/mol'
    except:
        check_for_entry(entry1.get())


def give_results():
    try:
        ent = entry1.get()
        ent2 = float(entry_counts.get())
        total = get_molecular_mass(ent)
        result_mult['text'] = str(round(total*ent2, 2)) + 'g/mol'
    except:
        try:
            check_for_entry(entry1.get())
        except:
            check_for_entry(entry_counts.get())


window = Tk()
proportion = 100
window.title('Predro Molecular mass calculator')
window.columnconfigure([0, 2], weight=0, minsize=proportion)
window.columnconfigure([1, 3], weight=0, minsize=proportion/2)
# window.rowconfigure([0], weight=0, minsize=proportion/2)
window.rowconfigure([1], weight=0, minsize=proportion)
frame_above = Frame(window)
frame_above.grid(columnspan=3, column=0, row=0)
introduction = Label(frame_above, text='Wellcome to the molecular mass calculator\nInput a simple molecular formula where all numbers have 1 digit')
introduction.grid(column=0, row=0, columnspan=4)

label1 = Label(window, text='Simplified molecular formula')
label1.grid(column=0, row=1)
entry1 = Entry(window)
entry1.grid(column=1, row=1)

button1 = Button(window, text='Calc', command=give_result)
button1.grid(column=2, row=1)
label2 = Label(window, text='')
label2.grid(column=3, row=1)

button2 = Button(window, text='Calc', command=give_results)
button2.grid(column=2, row=3)

label_counts = Label(window, text='Amount of this molecule')
label_counts.grid(column=0, row=3)

entry_counts = Entry(window)
entry_counts.grid(column=1, row=3)

result_mult = Label(window, text='')
result_mult.grid(column=3, row=3)

window.mainloop()
