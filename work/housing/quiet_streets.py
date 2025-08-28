import os
import osmnx as ox
import requests
from bs4 import BeautifulSoup 

def open_street_maps_find_one_way_streets(_place_name, silent=False):

    if not silent:
        _place_name = 'Long Beach, CA, USA'

        # Download the street network for the place
        G = ox.graph_from_place(_place_name, network_type='drive')

        one_way_streets = []

        # Iterate through edges and print one-way streets
        for u, v, k, data in G.edges(keys=True, data=True):
            if data.get('oneway'):
                street_name = data.get('name', 'Unnamed street')
                # print(type(street_name))
                if isinstance(street_name, list):
                    for name in street_name:
                        one_way_streets.append(name)
                else:
                    one_way_streets.append(street_name)

        unique_one_way_streets = sorted(set(one_way_streets))

        # for street in unique_one_way_streets:
        #     print(street)

        # Write the list to a file in the current script directory
        output_path = os.path.join(os.path.dirname(__file__), 'one_way_streets.txt')
        with open(output_path, 'w') as f:
            for street in unique_one_way_streets:
                f.write(f"{street}\n")

def zillow_search_html(_url, test=False):

    text = None

    if not test:
        # TODO:  Get this working
        # text = response.text
        pass
    else:
        print("Reading from local file...")
        input_path = os.path.join(os.path.dirname(__file__), 'Rental Listings in Long Beach CA - 114 Rentals _ Zillow.html')
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

    soup = BeautifulSoup(text, features="html.parser")

    # Zillow specific:
    # 
    # Find the </address> tag, then the next div with the desired attribute
    # address is in line 4068, where we want 1516 E. 2nd Street 
    # the parent of that tag is a </style> tag
    # inspecting the page gives us the following structure
    # <html>
    #   <head> stuff0 </head> 
    #   <body class="responsive-search-page nav-full-width"> stuff1 </body class>        (</address> is here)
    #   <iframe> stuff2 </iframe>
    # </html>
    # 
    # within the </body class"responsive-search-page nav-full-width"> <body> tags the sub structure is 
    # <upper upper level tags>   these describe the search result page
    #    <ul class>             ... and finally many layers down    container = soup.find('body', class_='responsive-search-page nav-full-width') we have ALL the listing cards
    #       <dl class>          this is the individual listing where </address> is located a few levels down
    
    # container = soup.find('body', class_=['responsive-search-page'])
    container = soup.find('head')
    print(container.prettify())

    return

def main():
    place_name = 'Long Beach, CA, USA'
    zillow_search_url = 'https://www.zillow.com/long-beach-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-118.26751773364256%2C%22east%22%3A-118.04470126635741%2C%22south%22%3A33.68558471156971%2C%22north%22%3A33.89045561170285%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A46298%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22sqft%22%3A%7B%22min%22%3A750%7D%2C%2255plus%22%3A%7B%22value%22%3A%22e%22%7D%2C%22doz%22%3A%7B%22value%22%3A%227%22%7D%2C%22mp%22%3A%7B%22min%22%3A1600%2C%22max%22%3A3000%7D%2C%22price%22%3A%7B%22min%22%3A318207%2C%22max%22%3A596639%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22Long%20Beach%20CA%22%7D'

    open_street_maps_find_one_way_streets(place_name, silent=True)
    zillow_search_html(zillow_search_url, test=True)


main()