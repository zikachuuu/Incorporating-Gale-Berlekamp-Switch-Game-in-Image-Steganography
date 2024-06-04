import gurobipy as gp
from gurobipy import GRB

def GB_Solver3(lightGrid, columnSwitch, rowSwitch, n):
    # Create a new model
    model = gp.Model("GB_Problem")

    # Decision Variables
    H = model.addVars(n, n, vtype=GRB.BINARY, name="H")
    X = model.addVars(n, vtype=GRB.BINARY, name="X")
    Y = model.addVars(n, vtype=GRB.BINARY, name="Y")
    Z = model.addVars(n, n, vtype=GRB.BINARY, name="Z")
    ALT_R = model.addVars(n, vtype=GRB.BINARY, name="ALT_R")
    ALT_C = model.addVars(n, vtype=GRB.BINARY, name="ALT_C")
    T = model.addVars(n, vtype=GRB.BINARY, name="T")
    S = model.addVars(n, vtype=GRB.BINARY, name="S")

    # Objective Function
    model.setObjective(
        gp.quicksum(lightGrid[i][j] * (1 - H[i, j]) for i in range(n) for j in range(n)) +
        gp.quicksum((1 - lightGrid[i][j]) * H[i, j] for i in range(n) for j in range(n)) +
        gp.quicksum(ALT_R[i] for i in range(n)) +
        gp.quicksum(ALT_C[j] for j in range(n)),
        GRB.MINIMIZE)

    # Constraints
    for i in range(n):
        for j in range(n):
            model.addConstr(H[i, j] <= X[i] - Y[j] + 2 * Z[i, j])
            model.addConstr(H[i, j] >= X[i] - Y[j] - 2 * Z[i, j])
            model.addConstr(X[i] - Y[j] + 1 <= 2 * (1 - Z[i, j]))
            model.addConstr(H[i, j] >= Y[j] - X[i])

    for i in range(n):
        model.addConstr(rowSwitch[i] + X[i] == 2 * T[i] + ALT_R[i])

    for j in range(n):
        model.addConstr(columnSwitch[j] + Y[j] == 2 * S[j] + ALT_C[j])

    # Optimize model
    model.optimize()

    optimizedMatrix = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                optimizedMatrix[0][j] = int(ALT_C[j-1].X)
            elif j == 0:
                optimizedMatrix[i][0] = int(ALT_R[i-1].X)
            else:
                optimizedMatrix[i][j] = int(lightGrid[i-1][j-1] * (1 - H[i-1, j-1].X) + (1 - lightGrid[i-1][j-1]) * H[i-1, j-1].X)

    return optimizedMatrix, model.objVal

