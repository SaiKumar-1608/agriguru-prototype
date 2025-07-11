import shap
import xgboost
import numpy as np
import matplotlib.pyplot as plt

X = np.random.rand(100, 2)
y = (X[:, 0] + X[:, 1] > 1).astype(int)
model = xgboost.XGBClassifier().fit(X, y)

explainer = shap.Explainer(model)
shap_values = explainer(X[:5])
shap.plots.waterfall(shap_values[0])
