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




Not all data matches up perfectly. Taiwan seems missing in GDP. The owner of the west bank is unclear. As this data is being used for a videogame we make incorrect assumptions and corrections in this edge cases.
Taiwan becomes part of China
Palestine part of Israel
Other mistakes may exist with conflict regions.
etc

Our objective with this data was to figure the worlds most important cities. These would be used for an X-Com like game.






Thusly counties will have a psedo-alliance.
This reflects for instance how the west tends to stick together and agree with one another.
Russia, China and other communist type countries also tend to stick together






Searching for a world map:
https://upload.wikimedia.org/wikipedia/commons/4/4a/World_map_with_four_colours.svg




"""
import csv






class Main():
    """

    all processing included in this one once object, it is a little complicated however by using high order functions with the read_csv_file function we re-use code


    using this pattern avoids loading the entire files into memory which is not practical at these file size, instead we iterate the file performing actions


    """

    # some entries for countries are simply empty in the city data, especially Kosovo
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



        "Vushtrri" : "Kosovo",
        "Istok" : "Kosovo",
        "Podujeva" : "Kosovo",

        "Shtime" : "Kosovo",
        "Dragash" : "Kosovo",
        "Peć" : "Kosovo",

        "Vitina" : "Kosovo",

        "Orahovac" : "Kosovo",


        "Obiliq" : "Kosovo",

        "Leposaviq" : "Kosovo",

        "Kosovo Polje" : "Kosovo",
        "Zvečan" : "Kosovo",
        "Llazicë" : "Kosovo",







        "Dzaoudzi" : "France",
        "Koungou" : "France",


    }


    # these names will override existing names, simplifying them for example like to "South Korea" just "Congo" etc.... preffering common names over official
    # in some cases we have no GDP for Taiwan for example, this data being for a videogame will assume Taiwan is in China

    # All matches on the left, will be replaced by the value on the right.... many islands etc simplified to their main owner, like France for instance
    country_name_correct = {


        "St. Lucia" : "Saint Lucia",

        "Jersey" : "Channel Islands",

        "Guernsey" : "Channel Islands",


        "St. Vincent and the Grenadines" : "Saint Vincent and the Grenadines",



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


            latitude = Coordinates[1]
            longitude = Coordinates[0]





            country_name = row[keys['Country name EN']]


            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]



            if name in self.override_country_for_city: # certain cities need correcting on owner
                country_name = self.override_country_for_city[name]

            

            country_code = row[keys['Country Code']]

            population = row[keys['Population']]
            population = int(population)

            country_gdp = None


            try:
                country_gdp = self.country_name_to_gdp[country_name]

            except:
                pass


            country_population = None
            try:
                country_population = self.country_name_to_pop[country_name]
            except:
                pass





            if population >= self.min_population:

                self.cities_count += 1

                if country_population == None:
                    print("no country population found for country {} , {}".format(name, country_name))
                if country_gdp == None:
                    print("no country gdp found for country {} , {}".format(name, country_gdp))



                if self.csv_writer:

                    self.csv_writer.writerow([name, longitude, latitude, population, country_name, country_gdp])
                    pass
                


            # country_code = row[keys['Country Code']]
            # gdp_2020 = row[keys['2020']]

            # print("{}   {}  {}  {}".format(i,name,country_name,population))
            pass




    country_name_to_pop = {}

    def countries_pop_data_csv_predicate(self, i , row, keys):


        if len(row) > 1:


            country_name = row[keys['Country Name']]


            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]


            country_population = row[keys['2020']]

            try:
                country_population = int(country_population)
            except:

                print("error getting population of:", country_name)
                country_population = 0

            


            self.country_name_to_pop[country_name] = country_population


            # print("{}  {} ".format(country_name,country_population))


    """
    

    """


    min_population = 50000



    cities_pop_data_csv =  "geonames-all-cities-with-a-population-1000.csv" # semicolonb

    countries_gdp_data =  "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv" # comma
    countries_pop_data = "API_SP.POP.TOTL_DS2_en_csv_v2_3358390.csv"


    output_filename = "MERGED_CITY_DATA.output.csv"


    csv_writer = None


    def __init__(self):

        print("RUNNING SCRIPT...")

        print("scan countries pop data...")


        # GET country_name_to_gdp dict
        self.read_csv_file(self.countries_pop_data,self.countries_pop_data_csv_predicate, 4, delimiter=',',max_records = 1000000)

        print("scan countries gdp data...")

        # GET country_name_to_gdp
        self.read_csv_file(self.countries_gdp_data,self.countries_gdp_data_predicate, 4, delimiter=',',max_records = 1000000)



        print("scan cities pop data...")


        # UNCOMMENT TO WRITE CSV
        self.csv_writer = csv.writer(open(self.output_filename, 'w', newline='',encoding='utf-8'))
        self.csv_writer.writerow(['name', 'longitude', 'latitude', 'population', 'country_name', 'country_gdp'])

        self.read_csv_file(self.cities_pop_data_csv,self.cities_pop_data_csv_predicate, 0, delimiter=';',max_records = 1000000)
        print("cities_count: ",self.cities_count)



        








Main()