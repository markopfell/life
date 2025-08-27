import osmnx as ox

place_name = 'Long Beach, CA, USA'

# Download the street network for the place
G = ox.graph_from_place(place_name, network_type='drive')

one_way_streets = []

# Iterate through edges and print one-way streets
for u, v, k, data in G.edges(keys=True, data=True):
    if data.get('oneway'):
        street_name = data.get('name', 'Unnamed street')
        print(type(street_name))
        if isinstance(street_name, list):
            for name in street_name:
                one_way_streets.append(name)
        else:
            one_way_streets.append(street_name)

unique_one_way_streets = sorted(set(one_way_streets))

for street in unique_one_way_streets:
    print(street)

# Write the list to a file in the current script directory
import os
output_path = os.path.join(os.path.dirname(__file__), 'one_way_streets.txt')
with open(output_path, 'w') as f:
    for street in unique_one_way_streets:
        f.write(f"{street}\n")

