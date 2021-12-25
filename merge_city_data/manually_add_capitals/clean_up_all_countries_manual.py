"""


currently takes the coordinates column and splits it

"""
import csv


class Main():


    def __init__(self):

        input_filename = "all_countries_gdp_and_manual_capitals.ucsv"
        output_filename = "all_countries_gdp_and_manual_capitals.clean.ucsv"

        writer = csv.DictWriter(
            open("all_countries_gdp_and_manual_capitals.clean.ucsv", 'w', encoding='utf-8', newline=''),
            fieldnames=[
                'longitude',
                'latitude',


            ],

        )
        writer.writeheader()





        ttl = 10000000000000
        for raw in csv.DictReader(open(input_filename, encoding='utf-8'), delimiter=','):
            ttl -= 1
            if ttl < 0:
                break


            print(raw)

            coor = raw['capital_coor']

            coor = coor.split(',')
            longitude = ""
            latitude = ""


            if len(coor) == 2:
                longitude = coor[0]
                latitude = coor[1]

            print(coor)


            writer.writerow({
                'longitude' : longitude,
                'latitude' : latitude,
                })







Main()