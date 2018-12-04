# micro-sat
The first SAT-solver for the Micro:bit

![micro-sat](https://user-images.githubusercontent.com/16174559/49434385-62e2ba00-f7b4-11e8-8520-069882730188.JPG)

# Input formulas on the fly!
The creative input method allows for creating formulas (on CNF) with 4 variables and up to 5 clauses!

![formula](https://user-images.githubusercontent.com/16174559/49434387-62e2ba00-f7b4-11e8-9b02-c405207e6620.JPG)

# Now you carry the answer in your pocket!
Using the well-established method of DPLL you can quickly find out the answer to your SAT-formulas!

![model](https://user-images.githubusercontent.com/16174559/49434386-62e2ba00-f7b4-11e8-90be-5b85e9f04399.JPG)

# Installation instructions
Just clone the repository, load the main.py-file in MU and upload it to your Micro:bit to get started!

# Usage
Use button A and button B to navigate screen (flashing dot indicates current position of cursor). 

Each line corresponds to one clause in the formula (from left-to-right is "A", "B", "C" and "D"). Last column is reserved for menu. For example, in first column, first row, strong light is A, weak light is not A and no light is the absence of A from the first clause.

Pressing A+B simultaneously changes the current position of the formula (No light => Strong light => Weak light => No light). 

There are two special actions. If the top right corner is activated, the formula is cleared. If bottom right corner is activated, sat-solver is started.

When solver is started, if X is displayed, that means formula is UNSAT, other wise model is displayed. There are up to four boxes. Top left box is A, top right B, bottom left C and bottom right D. Strong light corresponds to that the literal is True, weak light that the literal is False, no light that the literal is undefined.
