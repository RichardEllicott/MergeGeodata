"""


tried to find the cities by name


ended up with london canada for the UK!!!



"""
import csv


class Main:

    def script1(self):

        use_alt_names = False

        print("running script1...")

        
        self.geonames_all_cities = {}
        self.geonames_all_cities_alt_names = {}


        ttl = 10000000000000
        for raw in csv.DictReader(open("geonames-all-cities-with-a-population-1000.csv", encoding='utf-8'), delimiter=';'):
            ttl -= 1
            if ttl < 0:
                break

            # print(raw)

            name = raw['Name']

            alt_names = raw['Alternate Names']

            alt_names_list = alt_names.split(',')

            # print(alt_names)

            # print("alt names size: ", len(alt_names_list))


            if use_alt_names:
                for alt_name in alt_names_list:
                    self.geonames_all_cities_alt_names[alt_name] = raw
  

            self.geonames_all_cities[name] = raw

            

    def script2(self):

        print("running script2...")

        ttl = 100000000000
        self.found_capitals = {}
        self.missing_capitals = {}

        self.total_capitals = 0
        for raw in csv.DictReader(open("capital_cities_from_github.csv", encoding='utf-8')):
            ttl -= 1
            if ttl < 0:
                break

            print(raw)

            country = raw['country']
            capital = raw['capital']

            correct_capital = {
                'Washington, D.C.' : 'Washington D.C.',
                'Tskhinvali' : 'tskhinvali',
                'St. Pierre' : 'St Pierre',
                'Episkopi Cantonment' : 'Episkopi',
                'Sri Jayawardenapura Kotte' : 'Sri Jayawardenapura',
            }

            if capital in correct_capital:
                capital = correct_capital[capital]


            if capital in self.geonames_all_cities:
                # print("found capital!")
                # self.found_capitals += 1

                self.found_capitals[country] = self.geonames_all_cities[capital]

            elif capital in self.geonames_all_cities_alt_names:

                self.found_capitals[country] = self.geonames_all_cities_alt_names[capital]


            else:
                print("missing capital: {}".format(capital))
                self.missing_capitals[country] = capital

            

        print("found {} capitals".format(len(self.found_capitals)) )

        print("missing capitals: {}".format(len(self.missing_capitals)))

        for capital in self.missing_capitals:

            print("missing capital: {} ({})".format(capital, self.missing_capitals[capital]))





    def script3(self):

        print("running script3...")






        writer = csv.DictWriter(
            open("capitals_with_locations.gen.csv", 'w', encoding='utf-8', newline=''),
            fieldnames=[
                'country',
                'capital',
                'longitude',
                'latitude',

            ],

        )
        writer.writeheader()


        ttl = 10000000000000
        for raw in self.found_capitals:
            ttl -= 1
            if ttl < 0:
                break


            record = self.found_capitals[raw]

            # print(record)

            country = raw

            capital = record['Name']

            coor = record['Coordinates'].split(',')

            if capital == "London":

                print("London Coordinates ", coor)


            writer.writerow(
                {
                'country' : country,
                'capital' : capital,
                'longitude' : coor[0],
                'latitude' : coor[1],

                })
                



            # print(record)


        pass
    


    def __init__(self):

        self.script1()
        self.script2()
        self.script3()


Main()
