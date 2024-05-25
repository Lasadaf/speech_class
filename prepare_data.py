import os
import wave
import csv

ru_directory = os.path.abspath("./audio/Russian/ru/") + "/"
conv_audio_dir = os.path.abspath("./audio/converted/") + "/"

scp_file = open("./input/data.scp", "w")
stm_file = open("./input/data.stm", "w")

ru_csv = open(ru_directory + "ru_full.csv", "r")

reader = csv.DictReader(ru_csv)
for row in reader:
    if not (row["gender"] == "male" or row["gender"] == "female"):
        continue
    print("Doing " + row["path"])
    scp_file.write(row["name"] + " " + conv_audio_dir + row["name"].split(".")[0] + ".wav\n")
    if not os.path.isfile(conv_audio_dir + row["name"].split(".")[0] + ".wav"):
        os.system("ffmpeg -y -i " + ru_directory + row["path"] + " -vn -ac 1 -ar 16000 " + conv_audio_dir + row["name"].split(".")[0] + ".wav")
    else:
        print("File " + conv_audio_dir + row["name"].split(".")[0] + ".wav already exists, skipping...")
    with wave.open(conv_audio_dir + row["name"].split(".")[0] + ".wav") as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
        stm_file.write(row["name"] + " 0 " + row["speaker"] + " 0.00 " + str(duration_seconds) + " <" + row["gender"] + "> _\n")

ru_csv.close()

scp_file.close()
stm_file.close()