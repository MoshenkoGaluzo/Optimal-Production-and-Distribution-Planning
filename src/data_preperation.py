import numpy as np
import pandas as pd


#production capacity
data = {
    "Factory": ["Portugal", "Spain", "France"],
    "Iced Tea": [20000, 25000, 18000],
    "Sparkling Water": [15000, 20000, 15000],
    "Natural Juice": [10000, 12000, 10000],
    "Flavored Mineral Water": [8000, 10000, 9000]
}
capacity_df = pd.DataFrame(data)

#production cost
data = {
    "Factory": ["Portugal", "Spain", "France"],
    "Iced Tea": [0.90, 1.00, 1.10],
    "Sparkling Water": [0.60, 0.65, 0.70],
    "Natural Juice": [1.20, 1.15, 1.30],
    "Flavored Mineral Water": [1.10, 1.05, 1.20]
}
cost_df = pd.DataFrame(data)

#selling prices (€ per liter)
data = {
    "Market": ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"],
    "Iced Tea": [1.80, 1.75, 1.85, 2.00, 1.95, 1.70],
    "Sparkling Water": [1.20, 1.25, 1.30, 1.40, 1.35, 1.15],
    "Natural Juice": [2.10, 2.00, 2.05, 2.20, 2.15, 2.00],
    "Flavored Mineral Water": [2.00, 1.95, 1.98, 2.10, 2.05, 1.90]
}
price_df = pd.DataFrame(data)

#maximum demand (l per month)
data = {
    "Market": ["Lisbon", "Madrid", "Barcelona", "Paris", "Marseille", "Porto"],
    "Iced Tea": [10000, 12000, 9000, 15000, 10000, 8000],
    "Sparkling Water": [8000, 9000, 7000, 10000, 8000, 6000],
    "Natural Juice": [5000, 6000, 4500, 7000, 6000, 4000],
    "Flavored Mineral Water": [4000, 5000, 4000, 6000, 5000, 3500]
}
demand_df = pd.DataFrame(data)

#transport cost (€ per liter)
data = {
    "From → To": ["Portugal", "Spain", "France"],
    "Lisbon": [0.10, 0.20, 0.35],
    "Madrid": [0.20, 0.10, 0.30],
    "Barcelona": [0.25, 0.15, 0.25],
    "Paris": [0.40, 0.35, 0.10],
    "Marseille": [0.45, 0.30, 0.08],
    "Porto": [0.05, 0.25, 0.40]
}
transport_df = pd.DataFrame(data)

#Budgets (€)
total_production_budget = 120000
total_transport_budget = 40000

