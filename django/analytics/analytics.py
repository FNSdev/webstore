from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

MODEL = linear_model.LinearRegression()
POLY = PolynomialFeatures(degree=3)


# TODO model needs to be saved, when there is more than 1 uwsgi process
def train_profit(x, y):
    x = POLY.fit_transform(x)
    MODEL.fit(x, y)


def predict_profit(x):
    x = POLY.fit_transform([x])
    return MODEL.predict(x)[0]


def get_coefficients():
    return MODEL.coef_
