# -----------------------------------------------------------------------------------------------------------------
# SOLVE EACH METHOD: STAGE 2 SOLUTION
# -----------------------------------------------------------------------------------------------------------------

# import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import math
import copy
import random

from vrplib import read_solution
from pyvrp import Model, read
from pyvrp.plotting import (
    plot_coordinates,
    plot_instance,
    plot_result,
    plot_route_schedule,
)
from pyvrp.stop import MaxIterations, MaxRuntime
from pyvrp.plotting import plot_solution
from pyvrp.Result import Result
from pyvrp.plotting.plot_solution import plot_solution
from pyvrp import ProblemData, Solution
from pyvrp.Statistics import Statistics
from pyvrp._pyvrp import CostEvaluator, Solution
import os

# -----------------------------------------------------------------------------------------------------------------

output_path = 'C:/Users/felix/OneDrive/Dokumente/RSM/Master Thesis/MSc Thesis - mechanics company/Modeling/Modeling improved/pickle files improved/'

# -----------------------------------------------------------------------------------------------------------------
# import customer decision scenarios
with open(output_path + 'customer_decision_scenarios.pickle', 'rb') as file:
    scenarios = pickle.load(file)


np.random.seed(999)

# Sample random sublists for different set sizes
small_set_scenarios = []
medium_set_scenarios = []
large_set_scenarios = []

# Choose random indices of sublists
small_indices = np.random.choice(range(len(scenarios)), 10, replace=False)
medium_indices = np.random.choice(range(len(scenarios)), 50, replace=False)
large_indices = np.random.choice(range(len(scenarios)), 100, replace=False)

# Append the chosen sublists to the result lists
for idx in small_indices:
    small_set_scenarios.append(scenarios[idx])

for idx in medium_indices:
    medium_set_scenarios.append(scenarios[idx])

for idx in large_indices:
    large_set_scenarios.append(scenarios[idx])


# -----------------------------------------------------------------------------------------------------------------
# read depot data
with open(output_path + 'depot_locations.pickle', 'rb') as file:
    [depot_utrecht_df, depot_zuidholl_df, depot_overijssel_df] = pickle.load(file)


# -----------------------------------------------------------------------------------------------------------------
########################                            CVRP-SKIP                              ######################## 
# -----------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------
# load the data from pickle: 
with open(output_path + 'route_based_dfs.pickle', 'rb') as file:
    [utrecht_32_route_based_dfs, utrecht_64_route_based_dfs, utrecht_128_route_based_dfs, 
                 zuidholl_64_route_based_dfs, overijssel_64_route_based_dfs] = pickle.load(file)
    

# -----------------------------------------------------------------------------------------------------------------
# creating a function for haversine distance

def haversine(lon1, lat1, lon2, lat2):
    # Convert degrees to radians
    lon1 = math.radians(lon1)
    lat1 = math.radians(lat1)
    lon2 = math.radians(lon2)
    lat2 = math.radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return round(c * r)  # Round the result to the nearest integer


# -----------------------------------------------------------------------------------------------------------------

# calculate the total distance for each scenario and store the value in a list for each of the dataframes in route_based_with_scenarios_split[p][i][j][s][d]


def skip_approach_distances(df):
    """
    Computes the route distances following the sequence given by the 'final_route_order' column.
    When reaching the maximum final_route_order, returns to the depot (row index 0).
    
    Parameters:
    df (pd.DataFrame): The input dataframe with columns 'Longitude' and 'Latitude'.
    
    Returns:
    list: The distances between consecutive points in the route, including the return to the depot.
    """
    distances = []
    
    # Iterate over the DataFrame
    for i in range(len(df)):
        lon1, lat1 = df.loc[df['final_route_order'] == i, ['Longitude', 'Latitude']].values[0]
        
        # Get the index of the next point based on final_route_order
        next_index = (i + 1) % len(df)
        
        lon2, lat2 = df.loc[df['final_route_order'] == next_index, ['Longitude', 'Latitude']].values[0]
        
        # Calculate the distance using Haversine formula and round to the nearest integer
        distance = haversine(lon1, lat1, lon2, lat2)
        distances.append(distance)
    
    return distances



# -----------------------------------------------------------------------------------------------------------------
# Utrecht 32 -> small set of scenarios
# -----------------------------------------------------------------------------------------------------------------

# create dfs for each final route of 8 customers
utrecht_32_route_based_with_scenarios = []
for i in range(len(utrecht_32_route_based_dfs)):
    df_per_dataset = []
    for j in range(len(utrecht_32_route_based_dfs[i])):
        df_per_cluster = []
        for s in range(len(medium_set_scenarios)):
            df = copy.deepcopy(utrecht_32_route_based_dfs[i][j])
            df['decision'] = medium_set_scenarios[s]
            df_per_cluster.append(df)
        df_per_dataset.append(df_per_cluster)
    utrecht_32_route_based_with_scenarios.append(df_per_dataset)


# split each of the dataframes into two dataframes: one for each decision value
utrecht_32_route_based_with_scenarios_split = []
for i in range(len(utrecht_32_route_based_with_scenarios)):
    df_per_dataset = []
    for j in range(len(utrecht_32_route_based_with_scenarios[i])):
        df_per_cluster = []
        for s in range(len(utrecht_32_route_based_with_scenarios[i][j])):
            df = copy.deepcopy(utrecht_32_route_based_with_scenarios[i][j][s])
            df_decision_1 = df[df['decision'] == 1]
            df_decision_2 = df[df['decision'] == 2]
            # add depot utrecht to each dataframe
            df_decision_1 = pd.concat([depot_utrecht_df, df_decision_1])
            df_decision_2 = pd.concat([depot_utrecht_df, df_decision_2])
            # insert 0 in "route_position" column for depot
            df_decision_1.loc[0, 'route_position'] = 0
            df_decision_2.loc[0, 'route_position'] = 0

            # Sort the DataFrame by "route_position"
            df_decision_1 = df_decision_1.sort_values(by='route_position')
            df_decision_2 = df_decision_2.sort_values(by='route_position')
            
            # Create "final_route_order" column
            df_decision_1['final_route_order'] = range(len(df_decision_1))
            df_decision_2['final_route_order'] = range(len(df_decision_2))
            df_per_cluster.append([df_decision_1, df_decision_2])
        df_per_dataset.append(df_per_cluster)
    utrecht_32_route_based_with_scenarios_split.append(df_per_dataset)



CVRP_SKIP_utr32 = []
for i in range(len(utrecht_32_route_based_with_scenarios_split)):
    df_per_dataset = []
    for j in range(len(utrecht_32_route_based_with_scenarios_split[i])):
        df_per_cluster = []
        for s in range(len(utrecht_32_route_based_with_scenarios_split[i][j])):
            total_distances_per_decision = []  # List to store total distances for each decision
            for d in range(len(utrecht_32_route_based_with_scenarios_split[i][j][s])):
                df = utrecht_32_route_based_with_scenarios_split[i][j][s][d]
                distances = skip_approach_distances(df)
                total_distance = sum(distances)
                total_distances_per_decision.append(total_distance)
            df_per_cluster.append(total_distances_per_decision)
        df_per_dataset.append(df_per_cluster)
    CVRP_SKIP_utr32.append(df_per_dataset)



# -----------------------------------------------------------------------------------------------------------------
# Generate Skip for each size and province in big for loop -> obtain 5 dimensional list CVRP_SKIP_results[p][i][j][s][d] 
# where p is the province, i is the dataset, j is the cluster, s is the scenario and d is the decision
# -----------------------------------------------------------------------------------------------------------------

"""
help for exploration of results:

[p] : 0 = utrecht32, 1 = utrecht64, 2 = utrecht128, 3 = zuidholl64, 4 = overijssel64
[i] : 0-9 for each of the 10 datasets
[j] : 2 clusters for  utrecht32, 4 clusters for utrecht64, 8 clusters for utrecht128, 4 clusters for zuidholl64, 4 clusters for overijssel64
[s] : 0-49 for each of the 50 customer decision scenarios
[d] : 0-1 for each decision in a customer decision scenario

"""

# Define the list of list_names
list_names = [utrecht_32_route_based_dfs, utrecht_64_route_based_dfs, utrecht_128_route_based_dfs,
              zuidholl_64_route_based_dfs, overijssel_64_route_based_dfs]

depots = [depot_utrecht_df, depot_utrecht_df, depot_utrecht_df, depot_zuidholl_df, depot_overijssel_df]


# Process each element in list_names
CVRP_SKIP_results = []      # List to store distances for each element in list_names
CVRP_SKIP_dfs = []          # List to store dataframes per scenario for each element in list_names
CVRP_SKIP_dfs_split = []    # List to store split dataframes per scenario, split by the customer decision for each element in list_names

for index, dataframes in enumerate(list_names):
    
    # Create dfs for each final route of 8 customers
    route_based_with_scenarios = []
    for i in range(len(dataframes)):
        df_per_dataset = []
        for j in range(len(dataframes[i])):
            df_per_cluster = []
            for s in range(len(medium_set_scenarios)):
                df = copy.deepcopy(dataframes[i][j])
                df['decision'] = medium_set_scenarios[s]
                df_per_cluster.append(df)
            df_per_dataset.append(df_per_cluster)
        route_based_with_scenarios.append(df_per_dataset)
    CVRP_SKIP_dfs.append(route_based_with_scenarios)

    # Split each of the dataframes into two dataframes: one for each decision value
    route_based_with_scenarios_split = []
    for i in range(len(route_based_with_scenarios)):
        df_per_dataset = []
        for j in range(len(route_based_with_scenarios[i])):
            df_per_cluster = []
            for s in range(len(route_based_with_scenarios[i][j])):
                df = copy.deepcopy(route_based_with_scenarios[i][j][s])
                df_decision_1 = df[df['decision'] == 1]
                df_decision_2 = df[df['decision'] == 2]
                # add depot utrecht to each dataframe
                depot_df = depots[index]
                df_decision_1 = pd.concat([depot_df, df_decision_1])
                df_decision_2 = pd.concat([depot_df, df_decision_2])
                # insert 0 in "route_position" column for depot
                df_decision_1.loc[0, 'route_position'] = 0
                df_decision_2.loc[0, 'route_position'] = 0

                # Sort the DataFrame by "route_position"
                df_decision_1 = df_decision_1.sort_values(by='route_position')
                df_decision_2 = df_decision_2.sort_values(by='route_position')

                # Create "final_route_order" column
                df_decision_1['final_route_order'] = range(len(df_decision_1))
                df_decision_2['final_route_order'] = range(len(df_decision_2))
                df_per_cluster.append([df_decision_1, df_decision_2])
            df_per_dataset.append(df_per_cluster)
        route_based_with_scenarios_split.append(df_per_dataset)
    CVRP_SKIP_dfs_split.append(route_based_with_scenarios_split)
    
    # Calculate the total distance for each scenario and store the value in a list
    CVRP_SKIP_distances = []
    for i in range(len(route_based_with_scenarios_split)):
        df_per_dataset = []
        for j in range(len(route_based_with_scenarios_split[i])):
            df_per_cluster = []
            for s in range(len(route_based_with_scenarios_split[i][j])):
                total_distances_per_decision = []
                for d in range(len(route_based_with_scenarios_split[i][j][s])):
                    df = route_based_with_scenarios_split[i][j][s][d]
                    distances = skip_approach_distances(df)
                    total_distance = sum(distances)
                    total_distances_per_decision.append(total_distance)
                df_per_cluster.append(total_distances_per_decision)
            df_per_dataset.append(df_per_cluster)
        CVRP_SKIP_distances.append(df_per_dataset)
    
    CVRP_SKIP_results.append(CVRP_SKIP_distances)



# -----------------------------------------------------------------------------------------------------------------
# export the results to pickle

with open(output_path + 'CVRP_SKIP_results.pickle', 'wb') as file:
    pickle.dump(
        [CVRP_SKIP_results, CVRP_SKIP_dfs, CVRP_SKIP_dfs_split], file)
    

# -----------------------------------------------------------------------------------------------------------------
########################                            KMTSP-SKIP                             ######################## 
# -----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# load the data from pickle

with open(output_path + 'cluster_based_dfs.pickle', 'rb') as file:
    [utrecht_cluster_dataframes32_copy_KMTSP, utrecht_cluster_dataframes64_copy_KMTSP, utrecht_cluster_dataframes128_copy_KMTSP, 
                 zuidholl_cluster_dataframes64_copy_KMTSP, overijssel_cluster_dataframes64_copy_KMTSP] = pickle.load(file)


# -----------------------------------------------------------------------------------------------------------------

# Define the list of list_names
list_names = [utrecht_cluster_dataframes32_copy_KMTSP, utrecht_cluster_dataframes64_copy_KMTSP, utrecht_cluster_dataframes128_copy_KMTSP, 
                 zuidholl_cluster_dataframes64_copy_KMTSP, overijssel_cluster_dataframes64_copy_KMTSP]

depots = [depot_utrecht_df, depot_utrecht_df, depot_utrecht_df, depot_zuidholl_df, depot_overijssel_df]


# Process each element in list_names
KMTSP_SKIP_results = []      # List to store distances for each element in list_names
KMTSP_SKIP_dfs = []          # List to store dataframes per scenario for each element in list_names
KMTSP_SKIP_dfs_split = []    # List to store split dataframes per scenario, split by the customer decision for each element in list_names

for index, dataframes in enumerate(list_names):
    
    # Create dfs for each final route of 8 customers
    route_based_with_scenarios = []
    for i in range(len(dataframes)):
        df_per_dataset = []
        for j in range(len(dataframes[i])):
            df_per_cluster = []
            for s in range(len(medium_set_scenarios)):
                df = copy.deepcopy(dataframes[i][j])
                df['decision'] = medium_set_scenarios[s]
                df_per_cluster.append(df)
            df_per_dataset.append(df_per_cluster)
        route_based_with_scenarios.append(df_per_dataset)
    KMTSP_SKIP_dfs.append(route_based_with_scenarios)

    # Split each of the dataframes into two dataframes: one for each decision value
    route_based_with_scenarios_split = []
    for i in range(len(route_based_with_scenarios)):
        df_per_dataset = []
        for j in range(len(route_based_with_scenarios[i])):
            df_per_cluster = []
            for s in range(len(route_based_with_scenarios[i][j])):
                df = copy.deepcopy(route_based_with_scenarios[i][j][s])
                df_decision_1 = df[df['decision'] == 1]
                df_decision_2 = df[df['decision'] == 2]
                # add depot utrecht to each dataframe
                depot_df = depots[index]
                df_decision_1 = pd.concat([depot_df, df_decision_1])
                df_decision_2 = pd.concat([depot_df, df_decision_2])
                # insert 0 in "route_position" column for depot
                df_decision_1.loc[0, 'route_position'] = 0
                df_decision_2.loc[0, 'route_position'] = 0

                # Sort the DataFrame by "route_position"
                df_decision_1 = df_decision_1.sort_values(by='route_position')
                df_decision_2 = df_decision_2.sort_values(by='route_position')

                # Create "final_route_order" column
                df_decision_1['final_route_order'] = range(len(df_decision_1))
                df_decision_2['final_route_order'] = range(len(df_decision_2))
                df_per_cluster.append([df_decision_1, df_decision_2])
            df_per_dataset.append(df_per_cluster)
        route_based_with_scenarios_split.append(df_per_dataset)
    KMTSP_SKIP_dfs_split.append(route_based_with_scenarios_split)
    
    # Calculate the total distance for each scenario and store the value in a list
    KMTSP_SKIP_distances = []
    for i in range(len(route_based_with_scenarios_split)):
        df_per_dataset = []
        for j in range(len(route_based_with_scenarios_split[i])):
            df_per_cluster = []
            for s in range(len(route_based_with_scenarios_split[i][j])):
                total_distances_per_decision = []
                for d in range(len(route_based_with_scenarios_split[i][j][s])):
                    df = route_based_with_scenarios_split[i][j][s][d]
                    distances = skip_approach_distances(df)
                    total_distance = sum(distances)
                    total_distances_per_decision.append(total_distance)
                df_per_cluster.append(total_distances_per_decision)
            df_per_dataset.append(df_per_cluster)
        KMTSP_SKIP_distances.append(df_per_dataset)
    
    KMTSP_SKIP_results.append(KMTSP_SKIP_distances)



# -----------------------------------------------------------------------------------------------------------------
# export the results to pickle

with open(output_path + 'KMTSP_SKIP_results.pickle', 'wb') as file:
    pickle.dump(
        [KMTSP_SKIP_results, KMTSP_SKIP_dfs, KMTSP_SKIP_dfs_split], file)



# -----------------------------------------------------------------------------------------------------------------
########################                            CVRP-TSP                             ########################## 
# -----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# prerequisites for CVRP-TSP


scaling_factor = 100000

def scale_coordinates(coordinates, scale_factor):
    scaled_longitude = round(coordinates[0] * scale_factor, 0)
    scaled_latitude = round(coordinates[1] * scale_factor, 0)
    scaled_coordinates = (scaled_longitude, scaled_latitude)
    return scaled_coordinates


# -----------------------------------------------------------------------------------------------------------------
# take data from CVRP_SKIP_dfs_split and feed each of the datasets to vrp solver

with open(output_path + 'CVRP_SKIP_results.pickle', 'rb') as file:
     [CVRP_SKIP_results, CVRP_SKIP_dfs, CVRP_SKIP_dfs_split] = pickle.load(file)

# -----------------------------------------------------------------------------------------------------------------
# create the model for CVRP-TSP


CVRP_TSP_results = []  # List to store distances for each element in list_names
CVRP_TSP_routes = []   # List to store dataframes per scenario for each element in list_names

for index, dataframes in enumerate(CVRP_SKIP_dfs_split):
    results_per_dataframe = []  # Initialize distances for this iteration of list_names
    routes_per_dataframe = []   # Initialize routes for this iteration of list_names
    
    for i in range(len(dataframes)):
        results_per_dataset = []
        routes_per_dataset = []
        
        for j in range(len(dataframes[i])):
            results_per_cluster = []
            routes_per_cluster = []

            for s in range(len(dataframes[i][j])):
                results_per_scenario = []
                routes_per_scenario = []

                for d in range(len(dataframes[i][j][s])):
                    decision = dataframes[i][j][s][d]
                    all_coords = decision[['Longitude', 'Latitude']].values
                    demands = [0] + [1] * 8
                    scaled_coords = [scale_coordinates(coord, scaling_factor) for coord in all_coords]
                    m = Model()
                    m.add_vehicle_type(1, capacity=8)
                    depot = m.add_depot(x=scaled_coords[0][0], y=scaled_coords[0][1])
                    clients = [
                        m.add_client(x=scaled_coords[idx][0], y=scaled_coords[idx][1], delivery=demands[idx])
                        for idx in range(1, len(scaled_coords))
                    ]
                    locations = [depot] + clients
                    distances = []
                    for frm_idx, frm in enumerate(locations):
                        frm_lon, frm_lat = all_coords[frm_idx][0], all_coords[frm_idx][1]
                        distances_row = []
                        for to_idx, to in enumerate(locations):
                            to_lon, to_lat = all_coords[to_idx][0], all_coords[to_idx][1]
                            distance = haversine(frm_lon, frm_lat, to_lon, to_lat)
                            distances_row.append(distance)
                        distances.append(distances_row)

                    for frm_idx, frm in enumerate(locations):
                        for to_idx, to in enumerate(locations):
                            distance = distances[frm_idx][to_idx]
                            m.add_edge(frm, to, distance=distance)

                    res = m.solve(stop=MaxRuntime(1), collect_stats=True, display=True)
                    cost = res.cost()
                    route = str(res.best)

                    routes_per_scenario.append(route)
                    results_per_scenario.append(cost)

                routes_per_cluster.append(routes_per_scenario)
                results_per_cluster.append(results_per_scenario)

            routes_per_dataset.append(routes_per_cluster)
            results_per_dataset.append(results_per_cluster)

        routes_per_dataframe.append(routes_per_dataset)
        results_per_dataframe.append(results_per_dataset)

    CVRP_TSP_results.append(results_per_dataframe)
    CVRP_TSP_routes.append(routes_per_dataframe)



# -----------------------------------------------------------------------------------------------------------------
# export the results to pickle

with open(output_path + 'CVRP_TSP_results.pickle', 'wb') as file:
    pickle.dump(
        [CVRP_TSP_results, CVRP_TSP_routes], file)


# -----------------------------------------------------------------------------------------------------------------
########################                            KM-TSP                                 ######################## 
# -----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# prerequisites for CVRP-TSP


scaling_factor = 100000

def scale_coordinates(coordinates, scale_factor):
    scaled_longitude = round(coordinates[0] * scale_factor, 0)
    scaled_latitude = round(coordinates[1] * scale_factor, 0)
    scaled_coordinates = (scaled_longitude, scaled_latitude)
    return scaled_coordinates


# -----------------------------------------------------------------------------------------------------------------
# take data from KMTSP_SKIP_dfs_split and feed each of the datasets to vrp solver

with open(output_path + 'KMTSP_SKIP_results.pickle', 'rb') as file:
     [KMTSP_SKIP_results, KMTSP_SKIP_dfs, KMTSP_SKIP_dfs_split] = pickle.load(file)

# -----------------------------------------------------------------------------------------------------------------
# create the model for CVRP-TSP


KMTSP_TSP_results = []  # List to store distances for each element in list_names
KMTSP_TSP_routes = []   # List to store dataframes per scenario for each element in list_names

for index, dataframes in enumerate(KMTSP_SKIP_dfs_split):
    results_per_dataframe = []  # Initialize distances for this iteration of list_names
    routes_per_dataframe = []   # Initialize routes for this iteration of list_names
    
    for i in range(len(dataframes)):
        results_per_dataset = []
        routes_per_dataset = []
        
        for j in range(len(dataframes[i])):
            results_per_cluster = []
            routes_per_cluster = []

            for s in range(len(dataframes[i][j])):
                results_per_scenario = []
                routes_per_scenario = []

                for d in range(len(dataframes[i][j][s])):
                    decision = dataframes[i][j][s][d]
                    all_coords = decision[['Longitude', 'Latitude']].values
                    demands = [0] + [1] * 8
                    scaled_coords = [scale_coordinates(coord, scaling_factor) for coord in all_coords]
                    m = Model()
                    m.add_vehicle_type(1, capacity=8)
                    depot = m.add_depot(x=scaled_coords[0][0], y=scaled_coords[0][1])
                    clients = [
                        m.add_client(x=scaled_coords[idx][0], y=scaled_coords[idx][1], delivery=demands[idx])
                        for idx in range(1, len(scaled_coords))
                    ]
                    locations = [depot] + clients
                    distances = []
                    for frm_idx, frm in enumerate(locations):
                        frm_lon, frm_lat = all_coords[frm_idx][0], all_coords[frm_idx][1]
                        distances_row = []
                        for to_idx, to in enumerate(locations):
                            to_lon, to_lat = all_coords[to_idx][0], all_coords[to_idx][1]
                            distance = haversine(frm_lon, frm_lat, to_lon, to_lat)
                            distances_row.append(distance)
                        distances.append(distances_row)

                    for frm_idx, frm in enumerate(locations):
                        for to_idx, to in enumerate(locations):
                            distance = distances[frm_idx][to_idx]
                            m.add_edge(frm, to, distance=distance)

                    res = m.solve(stop=MaxRuntime(1), collect_stats=True, display=True)
                    cost = res.cost()
                    route = str(res.best)

                    routes_per_scenario.append(route)
                    results_per_scenario.append(cost)

                routes_per_cluster.append(routes_per_scenario)
                results_per_cluster.append(results_per_scenario)

            routes_per_dataset.append(routes_per_cluster)
            results_per_dataset.append(results_per_cluster)

        routes_per_dataframe.append(routes_per_dataset)
        results_per_dataframe.append(results_per_dataset)

    KMTSP_TSP_results.append(results_per_dataframe)
    KMTSP_TSP_routes.append(routes_per_dataframe)


# -----------------------------------------------------------------------------------------------------------------
# export the results to pickle

with open(output_path + 'KMTSP_TSP_results.pickle', 'wb') as file:
    pickle.dump(
        [KMTSP_TSP_results, KMTSP_TSP_routes], file)
    

# -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------   END OF STAGE 2    -------------------------------------------------------