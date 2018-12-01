CLAUSE_WIDTH=4

# cls1 = [1, 1, 0, 0, 0] # A v B
# cls2 = [1, -1, 0, 0, 0] # A v !B
# cls3 = [-1, 0, 1, 0, 0] # -A v C
# cls4 = [0, 0, 0, 0, 0] # %

cls1 = [1, 0, 1, 0] # %
cls2 = [-1, 0, -1, -1] # %
cls3 = [-1, 1, 0, 0] # %
cls4 = [1, 0, 1, 0] # %
cls5 = [-1, -1, 0, -1] # %


formula = [cls1, cls2, cls3, cls4, cls5]


def findUnitClause(formula):
    for cls in range(len(formula)):
        if formula[cls].count(0) == (CLAUSE_WIDTH-1):
            for lit in range(CLAUSE_WIDTH):
                if formula[cls][lit] != 0:
                    return (formula[cls], lit, formula[cls][lit])
    return (-1,0,0)

# def handleUnitClause(formula, unitClause, partialModel):
#     lit = -1
#     val = -1
#     for i in range(CLAUSE_WIDTH):
#         if unitClause[i] == 1:
#             lit = i
#             val = 1
#         elif unitClause[i] == -1:
#             lit = i
#             val = -1

    
#     partialModel[lit] = val
    

def findPureLiteral(formula):
    for i in range(CLAUSE_WIDTH):
        val = 0
        for f in formula:
            if (val == 0):
                val = f[i]
            elif (f[i] != 0 and f[i] != val):
                val = -2
        if (val != -2 and val != 0):
            return (i, val)
    return (-1, 0)

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
            
def printModel(partialModel):
    strs = ["A", "B", "C", "D"]

    for i in range(4):
        if (partialModel[i] != 0):
            print("%s: %d" % (strs[i], partialModel[i]))    
        
def solve(formula):
    partialModel = {} # 1 is T, -1 is F, 0 is UNDEF
    # Extract variables
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
                    print("Decision: %d := %d" % (decisionLit, -1))
                    partialModel[decisionLit] = -1
                    newDecision = True
                    change = True


        
        (cls, lit, val) = findUnitClause(formula)
        if (cls != -1):
            change = True
            print("UnitClause: %d := %d" % (lit, val))
            partialModel[lit] = val
            formula.remove(cls)
            # handleUnitClause(formula, formula[unitCls], partialModel)

        (lit, val) = findPureLiteral(formula)
        if (lit != -1):
            change = True
            print("PureLiteral: %d := %d" % (lit, val))            
            partialModel[lit] = val

        if not change:
            decisionLit = firstUnassigned(partialModel)
            
            old_formulas.append(formula.copy())
            decisions.append((decisionLit, 1))
            print("Decision: %d := %d" % (decisionLit, 1))

            partialModel[decisionLit] = 1

        # Check if we are done (i.e. all formulas are satisfied)


(result, model) = solve(formula)
print(result)
if (result == "SAT"):
    printModel(model)
    
