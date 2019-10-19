import csv
import glob
from tqdm import tqdm

base_dir = "../ml_preds_csv/"
files = glob.glob(base_dir + "*.csv")

# print(files)

f1 = open("roi.csv", 'w')
csv_writer = csv.writer(f1)
csv_writer.writerow(["Latitude", "Longitude"])

for f in tqdm(files):
    with open(f, 'r') as csv_file:
        reader = csv.reader(csv_file)
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue

            if int(row[2]) >= 75:
                csv_writer.writerow([row[3], row[4]])

f1.close()

                            
