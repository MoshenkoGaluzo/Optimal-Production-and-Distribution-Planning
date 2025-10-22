import pandas as pd
from pulp import *

matrix = pd.read_csv("csv_files/full/Matrix.csv", header=None).transpose()
RHS_old = pd.read_csv("csv_files/full/RHS.csv")
Profit_Function_old = pd.read_csv("csv_files/full/Profit_Function.csv")

model_dual = LpProblem("Drinks_Dual", LpMinimize)


index = range(len(RHS_old["Value"]))
Y = LpVariable.dicts("y", index, 0, None)

model_dual += (lpSum([  round(RHS_old["Value"][i], 2) * Y[i] for i in index]),"Minimize")

for i, row in matrix.iterrows():
    model_dual += lpSum([row[j]*Y[j] for j in index]) >= Profit_Function_old["Coeff"][i]

model_dual.solve()


variables = pd.DataFrame(columns=["Coeff", "Optimal Value"])
RHS = pd.DataFrame(columns=["Slack", "Value"])



solution_dict = {v.name: v.varValue for v in model_dual.variables()}

if hasattr(model_dual.objective, 'items'):
    for var, coeff in model_dual.objective.items():
        variables.loc[var.name] = [round(coeff,2), solution_dict[var.name]]

RHS["Slack"] = [constraint.slack for name, constraint in model_dual.constraints.items()]
RHS["Value"] = Profit_Function_old["Coeff"]

variables.to_csv("csv_files/dual/Profit_Function_dual.csv", index=True, index_label='Variable_Name')
matrix.to_csv("csv_files/dual/Matrix_dual.csv", index=False, header=False)
RHS.to_csv("csv_files/dual/RHS_dual.csv", index=False)
