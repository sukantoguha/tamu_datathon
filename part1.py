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


def all_in_one():
    # data loading
    # data structures:
    # > structure1: grid = 2D matrix (656x656) represents scaled down data
    #               each element in grid is a dict:
    #               {latitude, longitude, [all latitude/longitude covered by the grid]}
    # > structure2: flattened
    print("Data loading and Management")
    ml_road_dir = "../ml_preds_csv/"

    base_file_name = "3001120103"

    # 82** = 656
    grid = []
    grid_temp = [None] * 656
    for i in range(656):
        grid.append(grid_temp.copy())

    level_a = {'0': (0, 0), '1': (0, 328), '2': (328, 0), '3': (328, 328)}
    level_b = {'0': (0, 0), '1': (0, 164), '2': (164, 0), '3': (164, 164)}
    level_c = {'0': (0, 0), '1': (0, 82),  '2': (82, 0),  '3': (82, 82)}
    for a in tqdm(level_a):
        a_i = level_a[a][0]
        a_j = level_a[a][1]
        for b in level_b:
            b_i = a_i + level_b[b][0]
            b_j = a_j + level_b[b][1]
            for c in level_c:
                c_i = b_i + level_c[c][0]
                c_j = b_j + level_c[c][1]

                # generate files names
                file_name = base_file_name + a + b + c + ".csv"
                file_path = ml_road_dir + file_name

                with open(file_path, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    first_row = True
                    for row in reader:
                        if first_row:
                            first_row = False
                            continue

                        d_i = int(row[0])
                        d_j = int(row[1])

                        i = c_i + int(d_i/100)
                        j = c_j + int(d_j/100)

                        if int(row[2]) >= 75:
                            if grid[i][j] is None or grid[i][j]['val'] < int(row[2]):
                                if grid[i][j] is None:
                                    grid[i][j] = dict()
                                    grid[i][j]['coords'] = []
                                    # print(i, j)
                                grid[i][j]['val'] = int(row[2])
                                grid[i][j]['latlng'] = (float(row[3]), float(row[4]))
                            grid[i][j]['coords'].append((float(row[3]), float(row[4])))

    print("Data Management done")

    output = []
    population_sum = 0
    popden_path = "../tz_popdens_sample.csv"
    with open(popden_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_row = True
        for row in tqdm(reader):
            if first_row:
                first_row = False
                continue

            poplat = float(row[1]) * 100000
            poplng = float(row[2]) * 100000
            min_dist = 999999
            min_i = 0
            min_j = 0

            # iterate through the data
            for i in range(len(grid)):
                for j in range(len(grid[0])):
                    if grid[i][j] is not None:
                        lat = grid[i][j]['latlng'][0] * 100000
                        lng = grid[i][j]['latlng'][1] * 100000
                        if math.sqrt((lat - poplat) ** 2 + (lng - poplng) ** 2) < min_dist:
                            min_dist = math.sqrt((lat - poplat) ** 2 + (lng - poplng) ** 2)
                            min_i = i
                            min_j = j

            # dist = min_dist

            kernel = [-1, 0, 1]
            for i in kernel:
                for j in kernel:
                    r = min_i + i
                    c = min_j + j

                    if 0 <= r < len(grid) and 0 <= c < len(grid) and grid[r][c] is not None:
                        for coord in grid[r][c]['coords']:
                            lat = coord[0] * 100000
                            lng = coord[1] * 100000
                            min_dist = min(math.sqrt((lat - poplat) ** 2 + (lng - poplng) ** 2), min_dist)

            if min_dist <= 100:
                population_sum += float(row[0])

            output.append([float(row[1]), float(row[2]), min_dist / 100000, min_dist])

    print("writing results")
    outfile = open("../results/results_part_1-a.csv", 'w')
    csv_writer = csv.writer(outfile)
    csv_writer.writerow(["Latitude", "Longitude", "Distance(lat/lng)", "Distance(m)"])
    for row in output:
        csv_writer.writerow([str(row[0]), str(row[1]), str(row[2]), str(row[3])])

    outfile.close()

    print("Population having roads within 100m is: ", population_sum)


if __name__ == "__main__":
    all_in_one()
