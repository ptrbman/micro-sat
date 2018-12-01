from microbit import *

# A formula is made up of (up to) 4 clauses with 5 variables each (A, B, C, D, E)


cls1 = [1, 1, 0, 0, 0] # A v B
cls2 = [1, -1, 0, 0, 0] # A v !B
cls3 = [-1, 0, 1, 0, 0] # -A v C
cls4 = [0, 0, 0, 0, 0] # %

formula = [cls1, cls2, cls3, cls4]

def displayFormula(form):
    for i in range(4):      
        for j in range(5):
            if (form[i][j] == 1):
                display.set_pixel(j, i, 9)
            elif (form[i][j] == -1):
                display.set_pixel(j, i, 5)
            else:
                display.set_pixel(j, i, 0)


def clear():
    for i in range(5):
        for j in range(5):
            display.set_pixel(i, j, 0)
            


posx = 0
posy = 0
light = 0
lightdir = 1
while True:
    sleep(50)    
    ba = button_a.was_pressed()
    bb = button_b.was_pressed()
    
    if ba and bb:
        if (posy < 4):
            if (formula[posy][posx] == 0):
                formula[posy][posx] = 1
            elif (formula[posy][posx] == 1):
                formula[posy][posx] = -1
            else:
                formula[posy][posx] = 0
            
            ba = False
            bb = False
        else:
            display.scroll("SAT SOLVING")
    
    if ba:
        posx = (1 + posx) % 5
    if bb:
        posy = (1 + posy) % 5
    
    light = light+lightdir
    if light == 9:
        lightdir = -1
    elif light == 0:
        lightdir = 1

    display.clear()
    displayFormula(formula)    
    display.set_pixel(posx, posy, light)
    