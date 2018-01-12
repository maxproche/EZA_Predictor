import pandas as pd
import statsmodels.api as sm

class Predictor:

    def train(self, data):
        #Get the lsit of dependent variables from the data set
        X = data[ ["Open", "High", "Low", "Volume"] ]
        #Get independent variable from the data set
        y = data["Close"]
        #give X a constant term, representing y-intercept
        X = sm.add_constant(X)
        #get the results of Ordinary Least Squares Test
        results = sm.OLS(y, X).fit()
        #make an exception if the user puts time t = 1
        constantValue = 0.0
        if self.time > 1:
            constantValue = results.params.const
        #create dictionary of coefficients
        self.coefficients = {"Constant": constantValue, "Open": results.params.Open, "High": results.params.High, "Low": results.params.Low, "Volume": results.params.Volume }


    def test(self, data):
        #Get the features (dependent vars) & their data from our test day, t
        features = { "Open": data.Open, "High": data.High, "Low": data.Low, "Volume": data.Volume }
        #get the closing price for day t
        close = data.Close
        #start prediction at our y-intercept
        prediction = self.coefficients["Constant"]
        #for each key in dictionary
        for key in features:
            #add the product of that feature's weight * feature's value on day t
            prediction += self.coefficients[key] * features[key]

        #ratio of prediction to actual cost
        ratio = float(prediction / close)
        #I chose test outcome to be a list of strings for convenience
        testOutcome = ["Time t: " + str(self.time), "Predicted Close: " + str(prediction), "Actual Close: " + str(close), "Ratio: " + str(ratio) ]
        return testOutcome

    def getPredictionForDay(self, time):
        """
        if less than 5 do something different maybe
        """
        #create instance variable containing time
        self.time = time
        t = time
        #the data we use will range from row 0 through row t
        data = pd.read_csv("EZA_Daily.csv", nrows = t + 1)

        #training data will be the data from day 0 through day t-1
        trainData = data[0:t]
        #we will test how well our model does on day t
        testData = data.ix[t]
        #train the model on our training data
        self.train(trainData)
        #get the results of our trained model on the test data a.k.a. data from day t
        testOutcome = self.test(testData)
        return testOutcome
