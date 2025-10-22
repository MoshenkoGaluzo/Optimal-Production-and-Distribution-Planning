import pandas as pd
from pulp import *

matrix = pd.read_csv("csv_files/full/Matrix.csv", header=None)
RHS = pd.read_csv("csv_files/full/RHS.csv").iloc[:38]
Profit_Function = pd.read_csv("csv_files/full/Profit_Function.csv", index_col="Variable_Name")

model_we = LpProblem("Drinks_WE", LpMaximize)


index = range(len(Profit_Function["Coeff"]))
X = LpVariable.dicts("x", index, 0, None)

model_we += (lpSum([round(Profit_Function["Coeff"][i], 2) * X[i] for i in index]),"Maximize")

for i, row in matrix.iloc[:38].iterrows():
    model_we += lpSum([row[j]*X[j] for j in index]) <= RHS["Value"][i]

model_we.solve()


solution_dict = {v.name: v.varValue for v in model_we.variables()}

cnt_var = 0
if hasattr(model_we.objective, 'items'):
    for var, coeff in model_we.objective.items():
        Profit_Function.iloc[cnt_var] = [coeff, solution_dict[var.name]]
        cnt_var += 1

RHS["Slack"] = [constraint.slack for name, constraint in model_we.constraints.items()]
#print(RHS)

Profit_Function.to_csv("csv_files/without_extra/Profit_Function_WE.csv", index=True, index_label='Variable_Name')
matrix.iloc[:38].to_csv("csv_files/without_extra/Matrix_WE.csv", index=False, header=False)
RHS.to_csv("csv_files/without_extra/RHS_WE.csv", index=False)


print(Profit_Function.head())