import numpy as np
import csv
import glob
from tqdm import tqdm


def doit():
    base_dir = "../ml_preds_csv/"
    target_dir = "../ml_pred_csv_scaled/"
    files = glob.glob(base_dir + "*.csv")

    for csvfile in tqdm(files):
        grid = []
        grid_temp = [None]*82
        for i in range(82):
            grid.append(grid_temp.copy())

        with open(csvfile, 'r') as csv_file:
            reader = csv.reader(csv_file)
            first_row = True
            for row in reader:
                if first_row:
                    first_row = False
                    continue

                r = int(row[0])
                c = int(row[1])

                if grid[int(r / 100)][int(c / 100)] is None or grid[int(r / 100)][int(c / 100)]['val'] < int(row[2]):
                    d = dict()
                    d['i'] = r
                    d['j'] = c
                    d['val'] = int(row[2])
                    d['lat'] = row[3]
                    d['lng'] = row[4]
                    grid[int(r / 100)][int(c / 100)] = d

        fname = csvfile.split(sep='/')[-1]
        f = open(target_dir + fname, 'w')
        csv_writer = csv.writer(f)
        csv_writer.writerow(["i", "j", "val", "Latitude", "Longitude"])
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                # print(grid[r][c])
                if grid[r][c] is not None and grid[r][c]['val'] >= 75:
                    csv_writer.writerow([
                        str(grid[r][c]['i']),
                        str(grid[r][c]['j']),
                        str(grid[r][c]['val']),
                        grid[r][c]['lat'],
                        grid[r][c]['lng']
                    ])

        f.close()


if __name__ == '__main__':
    doit()