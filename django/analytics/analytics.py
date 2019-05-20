from analytics.models import DataSample
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

class Model():
    class __Model:
        def __init__(self):
            self.model = linear_model.LinearRegression()
            self.poly = PolynomialFeatures(degree=3)

        def train(self, x, y):
            x = self.poly.fit_transform(x)
            self.model.fit(x, y)

        def predict(self, x):
            x = self.poly.fit_transform([x])
            return self.model.predict(x)[0]

        def get_coefficients(self):
            return self.model.coef_

    instance = None

    def __new__(cls): 
        if not Model.instance:
            Model.instance = Model.__Model()
        return Model.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)