from pulp import *
import data_preperation as data
import pandas as pd
 
model_Drinks = LpProblem("Drinks", LpMaximize)

X = []

Drinks = ["Iced Tea", "Sparkling Water", "Natural Juice","Flavored Mineral Water"]
Cities = ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"]
Factories = ["Portugal", "Spain", "France"]

columns = [f"var_{i}" for i in range(72)]

variables = pd.DataFrame(columns=["Coeff", "Optimal Value"])
matrix = pd.DataFrame(columns=columns, dtype=float)
RHS = pd.DataFrame(columns=["Slack", "Value"])
cnst_number = 0


for i in range(0,4):
    X.append([])
    for j in range(0,6):
        X[i].append([])
        for k in range(0,3):
            X[i][j].append(LpVariable(f"{Drinks[i]} in {Cities[j]} from {Factories[k]}", 0, None))
            #X[i][j].append(f"{Drink[i]} in {City[j]} from {Factory[k]}")

#Profit function
#price/l - cost/l - transport/l
model_Drinks += (lpSum([(var*(data.price_df.iloc[j, i] - data.cost_df.iloc[k, i] - data.transport_df.iloc[k, j])) for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])), "Profit Function"


#Constraints for Maximum Demand
for i,drink in enumerate(Drinks):
    for j,city in enumerate(Cities):
        model_Drinks += lpSum(X[i][j]) <= data.demand_df.loc[city, drink], f"Demand for {Drinks[i]} in {Cities[j]}"
        matrix.loc[cnst_number] = [0]*(i*18 + j*3) + [1]*3 + [0]*(69 - i*18 - j*3)
        RHS.loc[cnst_number] = [0, data.demand_df.loc[city, drink]]
        cnst_number += 1
        

#Constrains for Maximum Production
for i,drink in enumerate(Drinks):
    for k, factory in enumerate(Factories):
        model_Drinks += lpSum(
            [X[i][city][k] for city in range(len(Cities))]
            ) <= data.capacity_df.loc[factory, drink], f"Prod. Cap. for {Drinks[i]} in {Factories[k]}"
        matrix.loc[cnst_number] = [0]*(18*i) + ([0]*(k) + [1] + [0]*(2-k))*6 + [0]*(54-18*i)
        RHS.loc[cnst_number] = [0, data.capacity_df.loc[factory, drink]]
        cnst_number += 1
        pass

#Production Cost Constraint
model_Drinks += (lpSum([var*data.cost_df.iloc[k,i] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= data.total_production_budget, "Production Budget Constraint"
matrix.loc[cnst_number] = [data.cost_df.iloc[k,i] for i in range(len(Drinks)) for j in range(len(Cities)) for k in range(len(Factories))]
RHS.loc[cnst_number] = [0, data.total_production_budget]
cnst_number += 1
#Transport Cost Constraint
model_Drinks += (lpSum([var*data.transport_df.iloc[k,j] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= data.total_transport_budget, "Transport Budget Constraint"
matrix.loc[cnst_number] = [data.transport_df.iloc[k,j] for i in range(len(Drinks)) for j in range(len(Cities)) for k in range(len(Factories))]
RHS.loc[cnst_number] = [0, data.total_transport_budget]
cnst_number += 1
#print("\n".join([str(X[0][i][0]) for i in range(len(Cities))]))


for k, factory in enumerate(Factories):
    for i, drink in enumerate(Drinks):
        #[0.5*var if drink in var.name else -0.5*var for var in X[][][]]
        model_Drinks += (lpSum([0.5*X[i][j][k] if drink in X[i][j][k].name else -0.5*X[i][j][k] for i in range(len(Drinks)) for j in range(len(Cities))])) <= 0, f"check {drink} in {factory}"
        matrix.loc[cnst_number] = [0]*(18*i) + ([-0.5]*(k) + [0.5] + [-0.5]*(2-k))*6 +[0]*(54-18*i)
        RHS.loc[cnst_number] = [0, 0]
        cnst_number += 1





model_Drinks.solve()



solution_dict = {v.name: v.varValue for v in model_Drinks.variables()}

if hasattr(model_Drinks.objective, 'items'):
    for var, coeff in model_Drinks.objective.items():
        variables.loc[var.name] = [coeff, solution_dict[var.name]]


RHS["Slack"] = [constraint.slack for name, constraint in model_Drinks.constraints.items()]

variables.to_csv("Profit_Function.csv", index=True, index_label='Variable_Name')
matrix.to_csv("Matrix.csv", index=False, header=False)
RHS.to_csv("RHS.csv", index=False)