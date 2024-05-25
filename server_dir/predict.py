import os
import wave

import sys
sys.path.append('../recipe/local')

from xvector_utils import XvectorClassifier, load_xvectors
import pandas as pd

def predict(dir_name, model_name):
    file_name = dir_name + "/myfile.wav"
    new_file_name = dir_name + "/converted.wav"
    duration_seconds = 0.0
    os.system("ffmpeg -y -i " + file_name + " -vn -ac 1 -ar 16000 " + new_file_name)
    with open(dir_name + "/data.scp", "w") as f:
        f.write("converted " + os.path.abspath(new_file_name) + "\n")
    with wave.open(new_file_name) as mywav:
        duration_seconds = mywav.getnframes() / mywav.getframerate()
    with open(dir_name + "/data.stm", "w") as f:
        f.write("converted 0 unknown 0.0 " + str(duration_seconds) + " <unknown> _\n")
    os.system("python3 ../recipe/local/xvector_utils.py make-xvectors " + dir_name + "/data.scp " + dir_name + "/data.stm " + dir_name + "/xvector.ark")
    #os.system("python3 ../recipe/local/xvector_utils.py predict " + dir_name + "/xvector.ark ../recipe/model/xvector-classifier.joblib")
    clf = XvectorClassifier.load("../recipe/model/" + model_name)
    xvectors, _ = load_xvectors(None, dir_name + "/xvector.ark")
    proba = pd.DataFrame(clf.predict_proba(xvectors), columns=clf.class_names)
    out = {}
    for col_name, col in proba.items():
        out.update({col_name : col.mean()})
    return out


    
