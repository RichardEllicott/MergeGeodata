"""


testing a pythons csv to dict



seems to be as fast as manual, way faster than pandas



this is the 3rd version.

first version: completly manual, higher order functions in manual csv loop ... about 50% faster than this version but horrible to write as it doesn't save the csv in memory
second version: pandas takes ages, good syntax but far too slow

this version: using the DictReader is a great compromise, nearly as fast as first version, way easier



"""


import csv

import warnings


def open_file_from_row(filename, row=0):
    """
    open from a row reference, like some csv files come with their headers starting on later lines
    """

    file = open(filename, encoding='utf-8')
    for i in range(row): # skip rows
        next(file)

    return file


def print_warning(msg):

    print("WARNING: {}".format(msg))





class Main():


    cities_filename = "geonames-all-cities-with-a-population-1000.csv"







    max_records = 1000000000 # only set low to debug

    min_population = 1000000



    override_country_for_city = {}

    country_name_corrections = {}

    output_filename = "PROCESS_ALL_DATA_SCRIPT_V3.OUTPUT.csv"



    output_filename2 = "PROCESS_ALL_DATA_SCRIPT_V3.OUTPUT.SORTED.csv"



    def script1_load_corrections(self):


        for raw in csv.DictReader(open("PROCESS_ALL_DATA_SCRIPT_V3_override_country_for_city.csv", encoding='utf-8')):
            self.override_country_for_city[raw['city']] = raw['country']


        for raw in csv.DictReader(open("country_name_corrections.csv", encoding='utf-8')):
            self.country_name_corrections[raw['from']] = raw['to']


        # print("override_country_for_city:",self.override_country_for_city,"\n")        
        # print("country_name_corrections:",self.country_name_corrections,"\n")



    def handle_world_bank_csv(self, filename, reason = "population"):
        """
        set up for the world bank data where we need to find the last valid value by going back through the columns
        """

        return_data = {}

        for raw in csv.DictReader(open_file_from_row(filename,row=4)): # world bank population

            country_name = raw['Country Name']

            if country_name in self.country_name_corrections:
                country_name = self.country_name_corrections[country_name]


            population = None


            start_col = 2020

            for i in range(30):

                col = str(start_col-i)

                this_val = raw[col]

                try:
                    this_val = float(this_val) # WARNING, float avoids bug, i choose float, the GDP needs a FLOAT, the population is actually an INT

                    if i > 0:
                        print_warning("last valid {} for {} is from {} ({})".format(reason,country_name,col,this_val))
                        pass
                    population = this_val

                    break
                except:
                    pass

            if population == None:
                print_warning("no valid {} found for \"{}\" ignoring this entry".format(reason,country_name))
            else:


                return_data[country_name] = population

        # print("population_data:")
        # print(return_data)

        return return_data


   


        pass


    def script2_load_world_bank_data(self):



        self.population_data = self.handle_world_bank_csv("API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv", "population")

        self.gdp_data = self.handle_world_bank_csv("API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv", "gdp")





    def script3_load_cities(self):

        valid_city_count = 0


        writer = csv.DictWriter(
            open(self.output_filename, 'w', encoding='utf-8',newline=''),
            fieldnames = ['name', 'longitude', 'latitude', 'population', 'significance'],

        )
        writer.writeheader()


        reader = csv.DictReader(
            open(self.cities_filename, encoding='utf-8'),
            delimiter=';'
        )

        i = 0
        for raw in reader:
            # print(raw)

            name = raw['Name']
            population = int(raw['Population'])


            coor = raw['Coordinates'].split(',')

            longitude = float(coor[0])

            latitude = float(coor[1])

            country_population = None 
            country_gdp = None


            country_gpd_per_capita = None

            city_significance = 0.0


            country_name = raw['Country name EN']

            if country_name in self.country_name_corrections:

                # print("correcting \"{}\" to \"{}\"".format(country_name, self.country_name_corrections[country_name]))
                country_name = self.country_name_corrections[country_name]



            timezone = raw['Timezone']



            if population >= self.min_population: # only bother to report these errors and process further if over population theshold
                


                if country_name in self.population_data:

                    country_population = self.population_data[country_name]

                else:
                    print_warning("no country_population found for city \"{}\"  ({})".format(name,country_name) )
                    pass


                if country_name in self.gdp_data:

                    country_gdp = self.gdp_data[country_name]

                else:
                    print_warning("no country_gdp found for city \"{}\"  ({})".format(name,country_name) )
                    pass


                if country_population and country_gdp:

                    country_gpd_per_capita = country_gdp / country_population

                    significance = country_gpd_per_capita * population / 1000000000.0

                    if significance > 1:

                        print("{} is significance with {:.0f}".format(name,significance))

                        valid_city_count += 1


                        writer.writerow({
                            'name' : name,
                            'longitude' : longitude,
                            'latitude' : longitude,
                            'population' : longitude,
                            'significance' : round(significance),
                            })



                    pass
                else:
                    # print("HSHSHSHS ..")
                    pass



            # print("{} {} {} {} ".format(name,longitude, latitude, population ))

            i += 1
            if i >= self.max_records:
                break



        print("valid_city_count:",valid_city_count)


    def script3_sort_data(self):


        reader = csv.DictReader(open(self.output_filename, encoding='utf-8'))


        for raw in reader:
            print(raw)

            name = raw['name']


            
            


    def __init__(self):

        # self.script1_load_corrections() # loads my correction csv
        # self.script2_load_world_bank_data() 
        # self.script3_load_cities() # REQUIRES PREVIOUS DATA, SAVES A FILE  takes about 4 seconds


        

        self.script3_sort_data()


        


Main()








