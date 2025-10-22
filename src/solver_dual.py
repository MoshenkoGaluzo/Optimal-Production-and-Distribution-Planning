import pandas as pd
from pulp import *

matrix = pd.read_csv("csv_files/Matrix.csv", header=None).transpose()
RHS_old = pd.read_csv("csv_files/RHS.csv")
Profit_Function_old = pd.read_csv("csv_files/Profit_Function.csv")

model_dual = LpProblem("Drinks_Dual", LpMinimize)


index = range(len(RHS_old["Value"]))
Y = LpVariable.dicts("y", index, 0, None)

model_dual += (lpSum([  round(RHS_old["Value"][i], 2) * Y[i] for i in index]),"Minimize")

for i, row in matrix.iterrows():
    model_dual += lpSum([row[j]*Y[j] for j in index]) >= Profit_Function_old["Coeff"][i]

model_dual.solve()
