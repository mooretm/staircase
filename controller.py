

###########
# Imports #
###########
# Import data science packages
import random

# Import GUI packages
import tkinter as tk
from tkinter import ttk

# Import custom modules
from models import staircase


#########
# Setup #
#########
# Randomly draw for which interval has stimulus
interval_order = [1,2]

# Staircase
s = staircase.Staircase(
    start_val=80,
    step_sizes=[4,2],
    nUp=1,
    nDown=2,
    nTrials=4,
    nReversals=2,
    rapid_descend=True,
    min_val=50,
    max_val=80
)

#############
# Functions #
#############
def _first_interval():
    if values[0] == 1:
        s.add_response(1)
    elif values[1] == 1:
        s.add_response(-1)


def _second_interval():
    if values[0] == 1:
        s.add_response(-1)
    elif values[1] == 1:
        s.add_response(1)


def _on_start():
    global values
    values = random.sample(interval_order, 2)
    int1.set(values[0])
    int2.set(values[1])


#########
# BEGIN #
#########
# Main window
root = tk.Tk()
global int1
global int2
int1 = tk.IntVar(value=None)
int2 = tk.IntVar(value=None)

# Frames
frm_main = ttk.Frame(root)
frm_main.grid(row=5, column=5, padx=10, pady=10)

# Widgets
ttk.Label(frm_main, text='Find the number 1').grid(
    row=5, column=5, columnspan=30)
ttk.Button(frm_main, text="START", command=_on_start).grid(
    row=10, column=5, columnspan=30, pady=5)

# Interval 1
ttk.Label(frm_main, textvariable=int1).grid(row=15, column=5)
ttk.Button(frm_main, text="1", command=_first_interval).grid(
    row=20, column=5, padx=10, pady=10)

# Interval 2
ttk.Label(frm_main, textvariable=int2).grid(row=15, column=10)
ttk.Button(frm_main, text="2", command=_second_interval).grid(
    row=20, column=10)

# Plot
ttk.Button(frm_main, text="Plot", command=s.plot_data).grid(row=25, column=5, columnspan=15)

root.mainloop()
