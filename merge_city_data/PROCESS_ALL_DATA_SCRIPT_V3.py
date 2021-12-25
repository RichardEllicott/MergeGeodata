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
    for i in range(row):  # skip rows
        next(file)

    return file


def print_warning(msg):

    print("WARNING: {}".format(msg))


class Main():

    cities_filename = "geonames-all-cities-with-a-population-1000.csv"

    max_records = 1000000000  # only set low to debug

    min_population = 10000

    min_significance = 0

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

    def handle_world_bank_csv(self, filename, reason="population"):
        """
        set up for the world bank data where we need to find the last valid value by going back through the columns
        """

        return_data = {}

        # world bank population
        for raw in csv.DictReader(open_file_from_row(filename, row=4)):

            country_name = raw['Country Name']

            if country_name in self.country_name_corrections:
                country_name = self.country_name_corrections[country_name]

            population = None

            start_col = 2020

            for i in range(30):

                col = str(start_col - i)

                this_val = raw[col]

                try:
                    # WARNING, float avoids bug, i choose float, the GDP needs a FLOAT, the population is actually an INT
                    this_val = float(this_val)

                    if i > 0:
                        print_warning("last valid {} for {} is from {} ({})".format(
                            reason, country_name, col, this_val))
                        pass
                    population = this_val

                    break
                except:
                    pass

            if population == None:
                print_warning("no valid {} found for \"{}\" ignoring this entry".format(
                    reason, country_name))
            else:

                return_data[country_name] = population

        # print("population_data:")
        # print(return_data)

        return return_data

        pass

    def script2_load_world_bank_data(self):

        self.population_data = self.handle_world_bank_csv(
            "API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv", "population")

        self.gdp_data = self.handle_world_bank_csv(
            "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv", "gdp")


        for raw in csv.DictReader(open("mydata_missing_gdp.csv", encoding='utf-8')): # load my corrections file
            # print(raw)
            self.population_data[raw['country']] = float(raw['population'])
            self.gdp_data[raw['country']] = float(raw['gdp'])





    def script3_load_cities(self):

        self.featured_countries = set() # null ref dict to track featured countries

        self.valid_city_count = 0

        writer = csv.DictWriter(
            open(self.output_filename, 'w', encoding='utf-8', newline=''),
            fieldnames=[
                'name',
                'country_name',
                # 'geoname_id',
                'longitude',
                'latitude',
                # 'elevation',
                'population',
                'significance'
            ],

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

            elevation = raw['Elevation']

            geoname_id = raw['Geoname ID']

            coor = raw['Coordinates'].split(',')

            longitude = float(coor[0])

            latitude = float(coor[1])

            country_population = None
            country_gdp = None

            country_gpd_per_capita = None

            country_name = raw['Country name EN']

            if country_name in self.country_name_corrections:

                # print("correcting \"{}\" to \"{}\"".format(country_name, self.country_name_corrections[country_name]))
                country_name = self.country_name_corrections[country_name]

            # only bother to report these errors and process further if over population theshold
            if population >= self.min_population:

                if country_name in self.population_data:

                    country_population = self.population_data[country_name]

                else:
                    print_warning(
                        "no country_population found for city \"{}\"  ({})".format(name, country_name))
                    pass

                if country_name in self.gdp_data:

                    country_gdp = self.gdp_data[country_name]

                else:
                    print_warning(
                        "no country_gdp found for city \"{}\"  ({})".format(name, country_name))
                    pass

                if country_population and country_gdp:

                    country_gpd_per_capita = country_gdp / country_population

                    significance = country_gpd_per_capita * population

                    if significance > 1:

                        # print("{} is significance with {:.0f}".format(name, significance))

                        self.valid_city_count += 1

                        self.featured_countries.add(country_name)

                        writer.writerow({
                            'name': name,
                            'country_name': country_name,
                            # 'geoname_id' : geoname_id,
                            'longitude': longitude,
                            'latitude': latitude,
                            # 'elevation': elevation,
                            'population': population,
                            'significance': round(significance),
                        })

                    pass
                else:
                    # print("HSHSHSHS ..")
                    pass

            # print("{} {} {} {} ".format(name,longitude, latitude, population ))

            i += 1
            if i >= self.max_records:
                break



    def script4_analyse_countries(self):


        output_filename6 = "output_countries_of_world.gen.csv"
        output_filename7 = "output_countries_of_world.gen2.csv"


        # EXTRA CHECK STUFF:
        print("valid_city_count:", self.valid_city_count)

        print("featured_countries: ", self.featured_countries)

        print("featured_countries count: ", len(self.featured_countries))


        writer = csv.DictWriter(
            open(output_filename6, 'w', encoding='utf-8', newline=''),
            fieldnames=[
                'country',
                'population',
                'gdp',
            ],

        )
        writer.writeheader()


        records = []

        for country in self.featured_countries:

            gdp = None 
            population = None

            if country in self.gdp_data:
                gdp = self.gdp_data[country]
            else:
                print("NO gdp FOR %s" % [country])

            if country in self.population_data:
                population = self.population_data[country]
            else:
                print("NO population FOR %s" % [country])


            records.append({
                'country': country,
                'population': population,
                'gdp': gdp,
             
            })



        def my_sort(e):
            return float(e["gdp"])
        records.sort(key=my_sort, reverse=True)


        for record in records:
            writer.writerow(record)









    def sort_csv_file(self, filename, output_filename, column_name):

        reader = csv.DictReader(open(filename, encoding='utf-8'))
        list_of_dicts = list(reader)

        writer = csv.DictWriter(
            open(self.output_filename2, 'w', encoding='utf-8', newline=''),
            fieldnames=list_of_dicts[0].keys())
        writer.writeheader()

        def my_sort(e):

            return float(e[column_name])

        list_of_dicts.sort(key=my_sort, reverse=True)

        for raw in list_of_dicts:

            writer.writerow(raw)

        pass

    def __init__(self):

        self.script1_load_corrections()  # loads my correction csv
        self.script2_load_world_bank_data()
        
        self.script3_load_cities() # REQUIRES PREVIOUS DATA, SAVES A FILE  takes about 4 seconds


        # self.sort_csv_file(self.output_filename,self.output_filename2, 'significance')
        self.sort_csv_file(self.output_filename,self.output_filename2, 'population')



        self.script4_analyse_countries()




        


Main()
