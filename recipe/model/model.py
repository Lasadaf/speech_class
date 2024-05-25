from sklearn.calibration import CalibratedClassifierCV
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import \
    classification_report, \
    confusion_matrix, \
    roc_curve
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn.svm import LinearSVC

class XVLinearSVC:
    def __init__(self, class_names, model_params={}):
        self._model = CalibratedClassifierCV(Pipeline([('scaler', Normalizer(norm='l1')),('svc', LinearSVC(**model_params))]))
        self._class_names = class_names

    def train(self, X_train, y_train):
        self._model.fit(X_train, y_train)

    

