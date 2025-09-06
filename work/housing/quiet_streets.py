import os
import osmnx as ox
import requests
from bs4 import BeautifulSoup 
import pandas
import copy

def open_street_maps_find_one_lane_streets(_place_name, _test=False, _output_to_file=False):

    unique_one_lane_streets = None
    
    one_lane_streets_file_name = '_one_lane_streets.txt'

    if _test:
        print("Downloading street network...")
        # _place_name = 'Long Beach, CA, USA'
        
        
        place_name_parts = _place_name.split(',')

        if ' ' in place_name_parts[0]:
            city_parts = place_name_parts[0].split(' ')
            place_name_parts[0] = '_'.join(city_parts)

        # print(place_name_parts)

        for i, place_name_part in enumerate(place_name_parts):
            place_name_part = place_name_part.strip().lower()
            place_name_parts[i] = place_name_part

        one_lane_streets_file_name = '_'.join(place_name_parts) + one_lane_streets_file_name


        # Download the street network for the place
        G = ox.graph_from_place(_place_name, network_type='drive')

        one_lane_streets = []

        # Iterate through edges and print one-lane streets
        for u, v, k, data in G.edges(keys=True, data=True):
            if data.get('onelane'):
                street_name = data.get('name', 'Unnamed street')
                # print(type(street_name))
                if isinstance(street_name, list):
                    for name in street_name:
                        one_lane_streets.append(name)
                else:
                    one_lane_streets.append(street_name)
                    print('onelane street: ', street_name)

        unique_one_lane_streets = sorted(set(one_lane_streets))
        # print(f"Found {len(unique_one_lane_streets)} unique one-lane streets in {place_name}.")

        for street in unique_one_lane_streets:
            print(street)

        print('\n_output_to_file:', _output_to_file)
        print('\n')


        if _output_to_file:
            # Write the list to a file in the current script directory
            print("Writing one-lane streets")
            output_path = os.path.join(os.path.dirname(__file__), one_lane_streets_file_name)
            with open(output_path, 'w') as f:
                for street in unique_one_lane_streets:
                    f.write(f"{street}\n")
    else:
        print('Skipping one-lane street extraction...')

    # for street in unique_one_lane_streets:
    #     print(street)

    return unique_one_lane_streets

def zillow_search_html(_city, _url, _test=False, _silent=True):

    text = None

    if not _test:
        # TODO:  Get this working
        # text = response.text
        pass
    else:
        print("Reading from local Zillow html file...")
        input_path = os.path.join(os.path.dirname(__file__), 'Rental Listings in Long Beach CA - 106 Rentals _ Zillow.html')
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
    #       <dl class>          this is the individual listing
    #           ...
    #               </address> is located a few levels down
    
    containers = soup.find_all('address')

    if _silent:
        for container in containers:
            print(container.prettify())
        print('\n')

    if _silent:
        for container in containers:
            # print(type(container)) # Should be <class 'bs4.element.Tag'>
            print(str(container.contents))
        print('\n')

    complex_addresses = []        

    for container in containers:
        # print(type(container)) # Should be <class 'bs4.element.Tag'>
        try:
            complex_addresses.append(str(container.contents[0]))
        except IndexError:
            pass

    if _silent:
        for i, complex_address in enumerate(complex_addresses):
            # print(complex_address)
            # Example: ['1516 E. 2nd Street', ' 1516 E 2nd St APT 2', ' Long Beach', ' CA 90802']
            # print('\t', complex_address.split(','))

            if i == 0:
                print(complex_address.split(','))

        print('\n')

    addresses = []
    for complex_address in complex_addresses:
        address_components = complex_address.split(',')
        

        address_index = 0
        for i, component in enumerate(address_components):
            if _city in component:
                address_index = i - 1

        if '|' in address_components[address_index]:
            address_components[address_index] = address_components[address_index].split('|')[1].strip()
        else:
            addresses.append(address_components[address_index])

    


    if _silent:
        # print(addresses[0]) # 1516 E 2nd St APT 2
        print ('\n')
        for i, address in enumerate(addresses):
            print(address)
            # print(address.split(' ')[1:])
            # if i == 0:
            #     print(address.split(' ')[1:]) # ['1516', 'E', '2nd', 'St', 'APT', '2']
        print('\n')


    print('Number of Zillow rental listing cards: {}'.format(len(containers)))
    print("Finished processing addresses.")

    return addresses

def street_abbreviations(_street_abbreviations_file, _test=False, _silent=False):

    _street_abbreviations_df = pandas.read_csv(_street_abbreviations_file)

    if _test and _silent:
        print('Processing street abbreviations:')
        _street_abbreviations_df


    return _street_abbreviations_df

def uncompressed_street_names(addresses, _street_abbreviations_df, _test, _silent):
    # TODO: Implement uncompression logic

    uncompressed_streets = []

    for _abbreviated_address in addresses:
        if _test and _silent:
            # print('Open Street maps quiet street uncompressed name:\n')
            # print('East 2nd Street\n')
            # _abbreviated_address = '1516 E 2nd St APT 2'

            # search_value = 'St'

            number = _abbreviated_address.split(' ')[0]

            street_name_end_index = 0

            for i, part in enumerate(_abbreviated_address.split(' ')):
                if part == 'APT' or '#' in part:
                    street_name_end_index = i - 1

            abbreviated_street_name_a = (_abbreviated_address.split(' '))[1:street_name_end_index + 1]
            print('Parsed abbreviated street name from abbreviated address:')
            print(abbreviated_street_name_a)

            uncompressed_street_name = copy.deepcopy(abbreviated_street_name_a)

            for i, part in enumerate(abbreviated_street_name_a):

                for idx, row in _street_abbreviations_df.iterrows():
                    for col in _street_abbreviations_df.columns:
                        if pandas.notnull(row[col]) and str(row[col]).lower() == str(part).lower():
                            # print(row[0])
                            uncompressed_street_name[i] = row[0]

            print('Uncompressed street name:')
            print('\t',' '.join(uncompressed_street_name))

            print('Uncompressed main address:')
            print(' '.join([number] + uncompressed_street_name))

            uncompressed_streets.append(' '.join([number] + uncompressed_street_name))

    return uncompressed_streets

def rentals_on_one_lane_streets(_addresses, _one_lane_streets, _test, _silent):
    if _test and _silent:
        print('\n\nFinding rentals potentially on one-lane streets:\n')

        for address in _addresses:

            street_name = address.split(' ')[2:]  # Get everything after the address number
            street_name = ' '.join(street_name)   

            # print(street_name)     

            for _one_lane_street in _one_lane_streets:
                if street_name == _one_lane_street:
                    print(f'Found rental on potentially a one-lane street: {address}')

                    # https://www.google.com/maps/place/926+Locust+Ave,+Long+Beach,+CA+90813/
                    parts = '+'.join(address.split(' ') + ['Long', 'Beach', 'CA'])
                    # print(parts)

                    search_query = ''.join(['https://www.google.com/maps/place/', parts])
                    print(search_query)
                    print('\n')
    return

def main():

    city = 'Long Beach'
    state = 'CA'
    country = 'USA'

    place_name = str(city + ', ' + state + ', ' + country)

    place_name = 'Long Beach, CA, USA'
    zillow_search_url = 'https://www.zillow.com/long-beach-ca/rentals/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-118.26751773364256%2C%22east%22%3A-118.04470126635741%2C%22south%22%3A33.68558471156971%2C%22north%22%3A33.89045561170285%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A46298%2C%22regionType%22%3A6%7D%5D%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22sqft%22%3A%7B%22min%22%3A750%7D%2C%2255plus%22%3A%7B%22value%22%3A%22e%22%7D%2C%22doz%22%3A%7B%22value%22%3A%227%22%7D%2C%22mp%22%3A%7B%22min%22%3A1600%2C%22max%22%3A3000%7D%2C%22price%22%3A%7B%22min%22%3A318207%2C%22max%22%3A596639%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%2C%22usersSearchTerm%22%3A%22Long%20Beach%20CA%22%7D'

    street_abbreviations_file = 'street_name_abbreviations_us.csv'

    street_abbreviations_df = street_abbreviations(street_abbreviations_file, True, True)
    one_lane_streets = open_street_maps_find_one_lane_streets(place_name, True, True)
    abbreviated_rental_addresses = zillow_search_html(city, zillow_search_url, True, True)
    addresses = uncompressed_street_names(abbreviated_rental_addresses, street_abbreviations_df, True, True)
    rentals_on_one_lane_streets(addresses, one_lane_streets, True, True)

    return


main()


