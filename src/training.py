
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.ensemble import GradientBoostingRegressor
from xgboost import XGBRegressor


class Training:
    def __init__(self,x_train,x_test,y_train,y_test):
        self.x_train=x_train
        self.x_test=x_test
        self.y_train=y_train
        self.y_test=y_test
        self.y_pred=None
        self.mse=None
        self.rmse=None
        self.mae=None
        self.r2_score=None
        self.models=None
    def model_train(self):


            xgb= XGBRegressor(colsample_bytree= 0.8, gamma= 0, learning_rate= 0.05,
                  max_depth= 3, n_estimators= 100, reg_alpha=0.1, 
                  reg_lambda = 1, subsample= 0.8)
            self.y_pred=xgb.fit(self.x_train,self.y_train).predict(self.x_test)

            mse = mean_squared_error(self.y_test, self.y_pred)
            r2 = r2_score(self.y_test, self.y_pred)
            mae=mean_absolute_error(self.y_test,self.y_pred)