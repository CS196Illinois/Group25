from django.conf import settings
import os
import pickle

import numpy as np
from sklearn.linear_model import LogisticRegression

##call the API to get stats for both teams needed to predict game
#def get_data(home_team_name, away_team_name):
#   code to get stats from API
#   return predict_game(stats)

def predict_game(home_delta_ERA, home_delta_RBI, home_delta_SLG, home_delta_AVG,
                away_delta_ERA, away_delta_RBI, away_delta_SLG, away_delta_AVG):
    # Creates path to models
    path = os.path.join(settings.MODELS, 'models.p')
 
    # Loads logistic regression model from pickle file
    with open(path, 'rb') as pickled:
       data = pickle.load(pickled)
    logreg = data['regression']
    
    diff_ERA = home_delta_ERA - away_delta_ERA
    diff_RBI = home_delta_RBI - away_delta_RBI
    diff_SLG = home_delta_SLG - away_delta_SLG
    diff_AVG = home_delta_AVG - away_delta_AVG

    # Stores the team stats in a numpy array and predicts the outcome of the game
    team_stats = np.array([diff_ERA, diff_RBI, diff_SLG, diff_AVG]).reshape(1, 4)
    prediction = logreg.predict(team_stats)

    return prediction
