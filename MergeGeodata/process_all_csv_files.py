"""



Cities Population:
https://public.opendatasoft.com/explore/dataset/geonames-all-cities-with-a-population-1000/export/?disjunctive.cou_name_en&sort=name

filename: geonames-all-cities-with-a-population-1000.csv
filesize: 25'937 KB
liscense: Attribution 4.0 International (CC BY 4.0)




GDP (countries):
https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

filename: API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv
size: 256 KB




Population (countries):
https://data.worldbank.org/indicator/SP.POP.TOTL?view=chart


filename: API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv
size: 179 KB




"""
import csv






class Main():

    # some entries for countries are simply empty for the smaller settlements
    override_country_for_city = {

        "Pristina" : "Kosovo",

        "Mitrovica" : "Kosovo",

        "Mitrovicë" : "Kosovo",

        "Prizren" : "Kosovo",



        "Willemstad" : "Curacao",



        "Gjilan" : "Kosovo",


        "Gjakovë" : "Kosovo",

        "Glogovac" : "Kosovo",

        "Ferizaj" : "Kosovo",


        "Mamoudzou" : "Mozambique", # NOT TRUE?


        "Suva Reka" : "Kosovo",

        "Deçan" : "Kosovo",

    }


    # these names will override existing names, simplifying them for example like to "South Korea" just "Congo" etc.... preffering common names over official
    # in some cases we have no GDP for Taiwan for example, this data being for a videogame will assume Taiwan is in China
    country_name_correct = {


        "Guadeloupe" : "France",
        "French Guiana" : "France",
        "Martinique" : "France",
        "Mayotte" : "France",


        "Lao PDR" : "Laos",


        "Egypt, Arab Rep.": "Egypt",

        "Iran, Islamic Rep. of" : "Iran",


        "Iran, Islamic Rep." : "Iran",


        "Korea, Rep." : "South Korea",
        "Korea, Republic of" : "South Korea",


        "Viet Nam" : "Vietnam",


        "Hong Kong, China" : "China",


        "Tanzania, United Republic of" : "Tanzania",

        "Congo, Democratic Republic of the" : "Congo",
        "Congo, Dem. Rep." : "Congo",


        "Korea, Dem. People's Rep." : "North Korea",
        "Korea, Dem. People's Rep. of" : "North Korea",


        "Venezuela, Bolivarian Rep. of" : "Venezuela",

        "Venezuela, RB" : "Venezuela",


        "Taiwan, China" : "China", # sorry Taiwan!



        "Cote d'Ivoire" : "Côte d'Ivoire", # Ivory Coast


        "Yemen, Rep." : "Yemen",

        

        "Sudan, The Republic of" : "Sudan",



        "Libyan Arab Jamahiriya" : "Libya",


        "Macau, China" : "China",

        "Moldova, Republic of" : "Moldova",


        "Kyrgyz Republic" : "Kyrgyzstan",


        "West Bank and Gaza Strip" : "Israel", # Palestine has made peace so it has the same gdp!

        "Slovak Republic" : "Slovakia",

        "South Sudan, The Republic of" : "South Sudan",



        

        "Macedonia, The former Yugoslav Rep. of" : "North Macedonia",



        "Gambia, The" : "Gambia",


        "Bahamas, The" : "Bahamas",


        "Eswatini" : "Swaziland",



        "Western Sahara" : "Morocco",


        "Réunion" : "France",


        "Cabo Verde" : "Cape Verde",


        "Lao People's Dem. Rep." : "Laos",



        "Virgin Islands (US)" : "Virgin Islands",

        "Virgin Islands (U.S.)" : "Virgin Islands",

    }






    def read_csv_file(self,filename, predicate, header_row = 0, delimiter=',', quotechar='"',encoding='utf-8',max_records = 1000000):


        csv_reader = csv.reader(
            open(filename, 'r', encoding=encoding), delimiter=delimiter, quotechar=quotechar)


        i_max = max_records

        i = 0

        record_id = 0

        keys = {}

        for line in csv_reader:


            if i < header_row:
                pass
            elif i == header_row:

                i2 = 0
                for label in line:
                    keys[label] = i2


                    i2 += 1
                print("keys: ", keys)
            else:
                # print("ff")
                predicate(record_id,line, keys)
                record_id += 1

            

            i += 1
            if i > i_max:
                break



    country_code_to_gdp = {}
    country_name_to_gdp = {}


    def countries_gdp_data_predicate(self,i, row, keys):

        # print("gg")

        if len(row) > 1:


            country_name = row[keys['Country Name']]


            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]



            country_code = row[keys['Country Code']]
            gdp_2020 = row[keys['2020']]

            try:
                gdp_2020 = float(gdp_2020)
            except ValueError as e:
                # print("Variable x is not defined ",e)
                gdp_2020 = 0.0





            self.country_code_to_gdp[country_code] = gdp_2020

            self.country_name_to_gdp[country_name] = gdp_2020

            # print("{} {}  {}".format(country_name,country_code,gdp_2020))
            pass

    




    cities_count = 0


    def count_add(self):
        self.record_count22 += 1
        pass

    def cities_pop_data_csv_predicate(self,i, row, keys):

        # print("gg")

        if len(row) > 1:


            name = row[keys['Name']]

            
            Coordinates = row[keys['Coordinates']]
            Coordinates = Coordinates.split(',')

            # print(Coordinates)


            latitude = Coordinates[0]
            longitude = Coordinates[1]





            country_name = row[keys['Country name EN']]


            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]



            if name in self.override_country_for_city: # certain cities need correcting on owner
                country_name = self.override_country_for_city[name]

            

            country_code = row[keys['Country Code']]

            population = row[keys['Population']]
            population = int(population)

            gdp_link = None


            try:
                # gdp_link = self.country_code_to_gdp[country_code]
                gdp_link = self.country_name_to_gdp[country_name]

            except:

                # print("nod gdp found: ", country_name)

                pass




            if population >= self.min_population:
                # print("{}  {} {}  {}".format(name,country_name,population,gdp_link))

                self.cities_count += 1

                if gdp_link == None:
                    print("No GDP found for city \"{}\" looking for country  \"{}\"" .format(  name, country_name))


                if self.csv_writer:

                    self.csv_writer.writerow([name, longitude, latitude, population, country_name, gdp_link])
                    pass
                


            # country_code = row[keys['Country Code']]
            # gdp_2020 = row[keys['2020']]

            # print("{}   {}  {}  {}".format(i,name,country_name,population))
            pass




    country_name_to_gdp = {}

    def countries_pop_data_csv_predicate(self, i , row, keys):


        if len(row) > 1:


            country_name = row[keys['Country Name']]

            country_population = row[keys['2020']]

            try:
                country_population = int(country_population)
            except:

                print("error getting population of:", country_name)
                country_population = 0

            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]


            self.country_name_to_gdp[country_name] = country_population


            # print("{}  {} ".format(country_name,country_population))




    min_population = 50000



    cities_pop_data_csv =  "geonames-all-cities-with-a-population-1000.csv" # semicolonb

    countries_gdp_data =  "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv" # comma
    countries_pop_data = "API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv"


    output_filename = "MERGED_CITY_DATA.csv"



    csv_writer = None


    def __init__(self):

        # GET country_name_to_gdp dict
        self.read_csv_file(self.countries_pop_data,self.countries_pop_data_csv_predicate, 4, delimiter=',',max_records = 1000000)


        # GET country_name_to_gdp
        self.read_csv_file(self.countries_gdp_data,self.countries_gdp_data_predicate, 4, delimiter=',',max_records = 1000000)



        self.csv_writer = csv.writer(open(self.output_filename, 'w', newline='',encoding='utf-8'))

        self.csv_writer.writerow(['name', 'longitude', 'latitude', 'population', 'country_name', 'country_gdp'])

        self.read_csv_file(self.cities_pop_data_csv,self.cities_pop_data_csv_predicate, 0, delimiter=';',max_records = 1000000)

        print("cities_count: ",self.cities_count)



        








Main()