import math
from tqdm import tqdm
import numpy as np
import glob
import csv
import cv2


def all_in_one():
    print("Data loading and Management")
    ml_road_dir = "../ml_preds_csv/"

    base_file_name = "3001120103"

    # 82** = 656
    grid = np.zeros((656, 656), dtype=np.uint8)

    level_a = {'0': (0, 0), '1': (0, 328), '2': (328, 0), '3': (328, 328)}
    level_b = {'0': (0, 0), '1': (0, 164), '2': (164, 0), '3': (164, 164)}
    level_c = {'0': (0, 0), '1': (0, 82), '2': (82, 0), '3': (82, 82)}
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

                        i = c_i + int(d_i / 100)
                        j = c_j + int(d_j / 100)

                        grid[i][j] = max(np.uint8(row[2]), grid[i][j])

    grid[grid <= 75] = 0
    cv2.namedWindow("Scaled Image", cv2.WINDOW_NORMAL)
    cv2.imshow("Scaled Image", grid)
    cv2.waitKey(0)


if __name__ == '__main__':
    all_in_one()