"""

testing pandas


a lot better idea!



"""


import pandas as pd

import csv


class Main:

    output_filename = "pandas_process_output.4000000.csv"

    def script1(self):

        # self.country_gdp = pd.read_csv ("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv", header=4) # GDP
        # print (self.country_gdp)

        # self.country_population = pd.read_csv("API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv", header=4) # population
        # print(self.country_population)

        self.csv_writer = csv.writer(
            open(self.output_filename, 'w', newline='', encoding='utf-8'))
        self.csv_writer.writerow(['name', 'longitude', 'latitude', 'population',
                                  'country_name', 'country_gdp', 'country_population'])

        rebuild_world_cities = pd.DataFrame()

        self.world_cities = pd.read_csv(
            "geonames-all-cities-with-a-population-1000.csv", delimiter=";")  # world cities
        # print(self.world_cities)

        ttl = 1000000000000000

        for index, row in self.world_cities.iterrows():
            # print(row['Name'], row[0])

            name = row['Name']

            population = row['Population']

            coordinates = row['Coordinates']

            # print("{} pop:{} coor:{}".format(name,population,coordinates))

            # print(coordinates)

            coor_split = coordinates.split(',')

            longitude = float(coor_split[0])
            latitude = float(coor_split[1])

            if population > 4000000:
                self.csv_writer.writerow(
                    [name, longitude, latitude, population, 'country_name', 'country_gdp', 'country_population'])

            new_row = {
                "name": name,
                "longitude": longitude,
                "latitude": latitude,
                "population":  population

            }

            rebuild_world_cities = rebuild_world_cities.append(new_row, ignore_index=True)

            ttl -= 1
            if ttl <= 0:

                break

        print("rebuild_world_cities: ", rebuild_world_cities)

    def __init__(self):

        self.script1()


Main()
