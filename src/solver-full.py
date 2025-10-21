from pulp import *
import data_preperation as data
import pandas as pd
 
model_Drinks = LpProblem("Drinks", LpMaximize)

X = []

Drinks = ["Iced Tea", "Sparkling Water", "Natural Juice","Flavored Mineral Water"]
Cities = ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"]
Factories = ["Portugal", "Spain", "France"]

variables = pd.DataFrame(columns=["Coeff", "Optimal Value"])
matrix = pd.DataFrame()

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
        

#Constrains for Maximum Production
for i,drink in enumerate(Drinks):
    for k, factory in enumerate(Factories):
        model_Drinks += lpSum(
            [X[i][city][k] for city in range(len(Cities))]
            ) <= data.capacity_df.loc[factory, drink], f"Prod. Cap. for {Drinks[i]} in {Factories[k]}"
        pass

#Production Cost Constraint
model_Drinks += (lpSum([var*data.cost_df.iloc[k,i] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= data.total_production_budget, "Production Budget Constraint"
#Transport Cost Constraint
model_Drinks += (lpSum([var*data.transport_df.iloc[k,j] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= data.total_transport_budget, "Transport Budget Constraint"
#print("\n".join([str(X[0][i][0]) for i in range(len(Cities))]))


for k, factory in enumerate(Factories):
    for i, drink in enumerate(Drinks):
        #[0.5*var if drink in var.name else -0.5*var for var in X[][][]]
        model_Drinks += (lpSum([0.5*X[i][j][k] if drink in X[i][j][k].name else -0.5*X[i][j][k] for i in range(len(Drinks)) for j in range(len(Cities))])) <= 0, f"check {drink} in {factory}"

model_Drinks.solve()

solution_dict = {v.name: v.varValue for v in model_Drinks.variables()}

if hasattr(model_Drinks.objective, 'items'):
    for var, coeff in model_Drinks.objective.items():
        variables.loc[var.name] = [coeff, solution_dict[var.name]]

variables.to_csv("Profit_Function.csv", index=True, index_label='Variable_Name')









def solve_without():
    model_Drinks.solve()

    # 2. CHECK STATUS  
    print("Status:", LpStatus[model_Drinks.status])

    # 3. GET RESULTS
    print("Optimal value =", value(model_Drinks.objective))
    for variable in model_Drinks.variables():
        print(f"{variable.name} = {variable.varValue}")


#solve_without()

#Additional constraint:
#Idea: a <= 0.5*(a+b)  is equi to 0.5*a - 0.5*b<=0
def solve_with():
    pass

    
model_Drinks.solve()
if hasattr(model_Drinks.objective, 'items'):
    print("\nCoefficients:")
    for var, coeff in model_Drinks.objective.items():
        print(f"  {var.name}: {coeff}")


    # 2. CHECK STATUS  
    #print("Status:", LpStatus[model_Drinks.status])

    # 3. GET RESULTS
print("Optimal value =", value(model_Drinks.objective))
for variable in model_Drinks.variables():
    print(f"{variable.name} = {variable.varValue}")



#solve_with()
#model_Drinks.solve()
print("=== CONSTRAINT INFORMATION ===")
for name, constraint in model_Drinks.constraints.items():
    slack = constraint.slack
    shadow_price = constraint.pi  # Dual value
    print(f"{name}: {constraint}")
    print(f"  Slack = {slack}")
    print(f"  Shadow Price = {shadow_price}")
#print("\n".join([str(X[i][j][0]) for i in range(len(Drinks)) for j in range(len(Cities))]))

print("number constraints: " + str(len(model_Drinks.constraints)))
print("number vars: " + str(len(model_Drinks.variables())))




print("Full objective:", model_Drinks.objective)
print("Objective name:", model_Drinks.objective.name)
print("Objective value:", value(model_Drinks.objective))  # After solving

# Get coefficients (if linear expression)
if hasattr(model_Drinks.objective, 'items'):
    print("\nCoefficients:")
    for var, coeff in model_Drinks.objective.items():
        print(f"  {var.name}: {coeff}")




print("\n")
print(variables.head())