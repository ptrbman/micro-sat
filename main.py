from microbit import *

CLAUSE_WIDTH=4
CLAUSE_COUNT=5
FALSE_LIGHT=5

cls1 = [1, 0, 0, 0] # %
cls2 = [1, 0, 0, 0] # %
cls3 = [-1, 0, 0, 0] # %
cls4 = [1, 0, 0, 0] # %
cls5 = [1, 0, 0, 0] # %
ocls1 = [1, 0, 0, 0] # %
ocls2 = [1, 0, 0, 0] # %
ocls3 = [-1, 0, 0, 0] # %
ocls4 = [1, 0, 0, 0] # %
ocls5 = [1, 0, 0, 0] # %

formula = [cls1, cls2, cls3, cls4, cls5]
oformula = [ocls1, ocls2, ocls3, ocls4, ocls5]



def propagate(formula, partialModel):
    to_remove = []
    for cls in formula:
        for lit in range(CLAUSE_WIDTH):        
            if (partialModel[lit] != 0):
                # If the model agrees here, lets remove the clause
                if cls[lit] == partialModel[lit]:
                    if cls not in to_remove:
                        to_remove.append(cls)
                # If the model disagrees, remove this literal
                if cls[lit] != partialModel[lit]:
                    cls[lit] = 0

    for clause in to_remove:
        formula.remove(clause)    

def firstUnassigned(partialModel):
    for i in range(CLAUSE_WIDTH):
        if partialModel[i] == 0:
            return i

def isContradicting(formula, partialModel):
    contradiction = True
    for clause in formula:
        satisfiable = False
        for i in range(CLAUSE_WIDTH):
            if (clause[i] == 1) and (partialModel[i] != -1):
                satisfiable = True
            if (clause[i] == -1) and (partialModel[i] != 1):
                satisfiable = True
        if satisfiable:
            contradiction = False
    return contradiction

def solve(formula):
    partialModel = {}
    for lit in range(CLAUSE_WIDTH):
        partialModel[lit] = 0

    decisions = []
    old_formulas = []

    while True:
        change = False
        propagate(formula, partialModel)
        
        if len(formula) == 0:
            return ("SAT", partialModel)
        
        if isContradicting(formula, partialModel):
            # Backtrack
            newDecision = False
            while (not newDecision):
                if (len(old_formulas) == 0):
                    return ("UNSAT", partialModel)
                formula = old_formulas.pop()
                (dLit, dVal) = decisions.pop()
                if (dVal == 1):
                    old_formulas.append(formula.copy())
                    decisions.append((decisionLit, -1))
                    partialModel[decisionLit] = -1
                    newDecision = True
                    change = True
        
        
        for cls in range(len(formula)):
            if formula[cls].count(0) == (CLAUSE_WIDTH-1):
                for lit in range(CLAUSE_WIDTH):
                    if formula[cls][lit] != 0 and partialModel[lit] == 0:
                        change = True
                        partialModel[lit] = formula[cls][lit]
                        toRemove.append(formula[cls])

        for i in range(CLAUSE_WIDTH):
            if (partialModel[i] == 0):
                val = 0
                for f in formula:
                    if (val == 0):
                        val = f[i]
                    elif (f[i] != 0 and f[i] != val):
                        val = -2
                if (val != -2 and val != 0 and partialModel[i] == 0):
                    change = True
                    partialModel[i] = val

        if not change:
            decisionLit = firstUnassigned(partialModel)
            old_formulas.append(formula.copy())
            decisions.append((decisionLit, 1))
            partialModel[decisionLit] = 1

def setSquare(coords, val):
    lights = [FALSE_LIGHT, 0, 9]
    for (x,y) in coords:
        display.set_pixel(x, y, lights[val+1])
        
def solveFormula(formula):
    (result, model) = solve(formula)
    display.show(result)
    if (result == "SAT"):
        display.clear()
        setSquare([(0,0), (0,1), (1,0), (1,1)], model[0])
        setSquare([(3,0), (3,1), (4,0), (4,1)], model[1])
        setSquare([(0,3), (0,4), (1,3), (1,4)], model[2])   
        setSquare([(3,3), (3,4), (4,3), (4,4)], model[3])
    while (not button_a.was_pressed() and not button_b.was_pressed()):
        pass
    
def displayFormula(form):
    for i in range(CLAUSE_COUNT):      
        for j in range(CLAUSE_WIDTH):
            if (form[i][j] == 1):
                display.set_pixel(j, i, 9)
            elif (form[i][j] == -1):
                display.set_pixel(j, i, 5)
            else:
                display.set_pixel(j, i, 0)

def menu(formula):
    posx = 0
    posy = 0
    light = 0
    lightdir = 1
    while True:
        sleep(200)    
        ba = button_a.was_pressed()
        bb = button_b.was_pressed()
        
        if ba and bb:
            if (posx < CLAUSE_WIDTH):
                if (formula[posy][posx] == 0):
                    formula[posy][posx] = 1
                elif (formula[posy][posx] == 1):
                    formula[posy][posx] = -1
                else:
                    formula[posy][posx] = 0
                
                ba = False
                bb = False
            elif posy == 0:
                for i in range(CLAUSE_COUNT):
                    for j in range(CLAUSE_WIDTH):
                        formula[i][j] = 0
            elif (posy == 4):
                return formula
        
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
        
while True:
    display.clear()
    menu(formula)
    for i in range(CLAUSE_COUNT):
        oformula[i] = formula[i].copy()
    solveFormula(formula)
    formula = []
    for i in range(CLAUSE_COUNT):
        formula.append(oformula[i].copy())



