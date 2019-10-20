import pandas as pd
import math
from tqdm import tqdm
import glob
import csv


def doit():
    base_dir = "../ml_pred_csv_scaled/"
    files = glob.glob(base_dir + "*.csv")

    geocoords = []
    print("reading road files")
    for csvfile in tqdm(files):
        with open(csvfile, 'r') as csv_file:
            reader = csv.reader(csv_file)
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                    continue
            geocoords.append((row[3], row[4]))

    outfile = open("../results/results_part_1-a.csv", 'w')
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(["Latitude", "Longitude", "Distance(lat/lng)", "Distance(m)"])

    popden_path = "../tz_popdens_sample.csv"
    with open(popden_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_row = True
        for row in tqdm(reader):
            if first_row:
                first_row = False
                continue

            poplat = float(row[1])*100000
            poplng = float(row[2])*100000
            min_dist = math.inf
            closest_lat = 0
            closest_lng = 0
            for coord in geocoords:
                lat = float(coord[0])*100000
                lng = float(coord[1])*100000
                if math.sqrt((lat-poplat)**2 + (lng-poplng)**2) < min_dist:
                    min_dist = math.sqrt((lat-poplat)**2 + (lng-poplng)**2)
                    closest_lat = coord[0]
                    closest_lng = coord[1]
            # print(min_dist)
            csv_writer.writerow([
                row[1],
                row[2],
                str(min_dist/100000),
                str(min_dist)
            ])
    outfile.close()


if __name__ == "__main__":
    doit()
