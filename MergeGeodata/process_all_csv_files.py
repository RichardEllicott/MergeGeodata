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



take the world data, format it to just 2020 GDP:




"""
import csv






class Main():

    country_name_correct = {
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


    def counties_gdp_data_predicate(self,i, row, keys):

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

            country_name = row[keys['Country name EN']]


            if country_name in self.country_name_correct: # correct country_name
                country_name = self.country_name_correct[country_name]

            

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




            if population > 1000000:
                # print("{}  {} {}  {}".format(name,country_name,population,gdp_link))

                self.cities_count += 1

                if gdp_link == None:
                    print("No GDP found for city \"{}\" looking for country  \"{}\"" .format(  name, country_name))
                


            # country_code = row[keys['Country Code']]
            # gdp_2020 = row[keys['2020']]

            # print("{}   {}  {}  {}".format(i,name,country_name,population))
            pass


    counties_gdp_data =  "API_NY.GDP.MKTP.CD_DS2_en_csv_v2_3358362.csv" # comma

    cities_pop_data_csv =  "geonames-all-cities-with-a-population-1000.csv" # semicolon


    def __init__(self):

        

        self.read_csv_file(self.counties_gdp_data,self.counties_gdp_data_predicate, 4, delimiter=',',max_records = 1000000)




    
        

        self.read_csv_file(self.cities_pop_data_csv,self.cities_pop_data_csv_predicate, 0, delimiter=';',max_records = 1000000)

        print("cities_count: ",self.cities_count)



Main()