import csv
import json

csv_file_path = '/Users/svkane/Desktop/Uni/archive/movies.csv'
json_file_path = '/Users/svkane/Desktop/Uni/archive/movies.json'

data = []

with open(csv_file_path, encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # Optional: Clean or transform data here
        data.append(row)

with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("CSV file has been converted to JSON.")
