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

Drink = ["Iced Tea", "Sparkling Water", "Natural Juice","Flavored Mineral Water"]
City = ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"]
Factory = ["Portugal", "Spain", "France"]

for i in range(0,4):
    X.append([])
    for j in range(0,6):
        X[i].append([])
        for k in range(0,3):
            X[i][j].append(LpVariable(f"{Drink[i]} in {City[j]} from {Factory[k]}", 0, None))
            #X[i][j].append(f"{Drink[i]} in {City[j]} from {Factory[k]}")

#print(X[0][0][0])

#Profit function
#price/l - cost/l - transport/l
model_Drinks += (lpSum([(var*(dp.price_df.iloc[j, i] - dp.cost_df.iloc[k, i] - dp.transport_df.iloc[k, j])) for i,drinks in enumerate(X) for j,cities in enumerate(drinks) for k,var in enumerate(cities)])), "Profit Function"


#Constraints for Maximum Demand
for i,drinks in enumerate(Drink):
    for j,cities in enumerate(City):
        model_Drinks += lpSum(X[i][j]) <= dp.demand_df.loc[cities, drinks], f"Demand for {Drink[i]} in {City[j]}"
