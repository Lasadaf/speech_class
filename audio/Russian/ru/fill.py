import csv
import pandas as pd
csvfile_out = open("./ru.csv", "w")
csvwriter = csv.DictWriter(csvfile_out, fieldnames=["path", "name", "speaker", "gender", "class"])
csvwriter.writeheader()
ds = pd.read_csv("./other.csv", sep='\t', low_memory=False, skiprows=0)
for index, row in ds.iterrows():
    csvwriter.writerow({"path" : "./clips/" + row["path"], "name" : row["path"], "speaker" : row["client_id"], "gender" : row["gender"], "class" : "russian"})
ds = pd.read_csv("./validated.csv", sep='\t', low_memory=False, skiprows=0)
for index, row in ds.iterrows():
    csvwriter.writerow({"path" : "./clips/" + row["path"], "name" : row["path"], "speaker" : row["client_id"], "gender" : row["gender"], "class" : "russian"})
ds = pd.read_csv("./invalidated.csv", sep='\t', low_memory=False, skiprows=0)
for index, row in ds.iterrows():
    csvwriter.writerow({"path" : "./clips/" + row["path"], "name" : row["path"], "speaker" : row["client_id"], "gender" : row["gender"], "class" : "russian"})
csvfile_out.close()

 
 
 
