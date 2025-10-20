from pulp import *
import data_preperation as dp
 
m=4
n=2
indexI = range(1,m+1)
indexJ = range(1,n+1)
indexK = range(1, 3)

A = [ [6, 4], [1, 2], [-1, 1], [0, 1] ]
B = [24, 6, 1, 2]
C = [5, 4]
A = makeDict([indexI, indexJ], A)
B = makeDict([indexI], B)
C = makeDict([indexJ], C)


model_Drinks = LpProblem("Drinks", LpMaximize)

X = []
#print(X[0][0][0])

Drinks = ["Iced Tea", "Sparkling Water", "Natural Juice","Flavored Mineral Water"]
Cities = ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"]
Factories = ["Portugal", "Spain", "France"]

for i in range(0,4):
    X.append([])
    for j in range(0,6):
        X[i].append([])
        for k in range(0,3):
            X[i][j].append(LpVariable(f"{Drinks[i]} in {Cities[j]} from {Factories[k]}", 0, None))
            #X[i][j].append(f"{Drink[i]} in {City[j]} from {Factory[k]}")

#print(X[0][0][0])

#Profit function
#price/l - cost/l - transport/l
model_Drinks += (lpSum([(var*(dp.price_df.iloc[j, i] - dp.cost_df.iloc[k, i] - dp.transport_df.iloc[k, j])) for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])), "Profit Function"


#Constraints for Maximum Demand
for i,drink in enumerate(Drinks):
    for j,city in enumerate(Cities):
        model_Drinks += lpSum(X[i][j]) <= dp.demand_df.loc[city, drink], f"Demand for {Drinks[i]} in {Cities[j]}"

#Constrains for Maximum Production
for i,drink in enumerate(Drinks):
    for k, factory in enumerate(Factories):
        model_Drinks += lpSum(
            [X[i][city][k] for city in range(len(Cities))]
            ) <= dp.capacity_df.loc[factory, drink], f"Prof. Cap. for {Drinks[i]} in {Factories[k]}"
        pass

#Production Cost Constraint
model_Drinks += (lpSum([var*dp.cost_df.iloc[k,i] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= dp.total_production_budget, "Production Budget Constraint"
#Transport Cost Constraint
model_Drinks += (lpSum([var*dp.transport_df.iloc[k,j] for i,drink in enumerate(X) for j,city in enumerate(drink) for k,var in enumerate(city)])) <= dp.total_transport_budget, "Transport Budget Constraint"
#print("\n".join([str(X[0][i][0]) for i in range(len(Cities))]))


model_Drinks.solve()

# 2. CHECK STATUS  
print("Status:", LpStatus[model_Drinks.status])

# 3. GET RESULTS
print("Optimal value =", value(model_Drinks.objective))
for variable in model_Drinks.variables():
    print(f"{variable.name} = {variable.varValue}") 