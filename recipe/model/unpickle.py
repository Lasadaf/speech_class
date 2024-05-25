import pickle

f = open('xvector-classifier.pkl', 'rb')
data = pickle.load(f)

f.close()
f = open('unpickled.txt', "w")
f.write(str(data))
f.close()