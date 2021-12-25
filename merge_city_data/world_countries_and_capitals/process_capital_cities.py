"""
"""
import csv




class Main:



	def script1(self):

		filename1 = "PROCESS_ALL_DATA_SCRIPT_V3.OUTPUT.SORTED_POPULATION.csv"
		filename2 = "capital_cities_from_github.csv"


		out_filename = "process_all_world_capitals.gen.csv"

		writer = csv.DictWriter(
            open(out_filename, 'w', encoding='utf-8', newline=''),
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




		cities = {}

		for raw in csv.DictReader(open(filename1, encoding='utf-8')):
			# print(raw)

			name = raw['name']

			cities[name] = raw




		for raw in csv.DictReader(open(filename2, encoding='utf-8')):
			# print(raw)

			capital = raw['capital']
			country = raw['country']

			if capital in cities:

				# print("FOUND CAP!")
				pass

			else:
				print("missing capital \"{}\" for \"{}\"".format(capital, country))
       


	def __init__(self):

		print("run scripts...")

		self.script1()


Main()
