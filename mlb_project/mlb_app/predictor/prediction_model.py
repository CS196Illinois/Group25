from django.conf import settings
import os
import pickle

import numpy as np
from sklearn.linear_model import LogisticRegression

def predict_game(delta_ERA, delta_RBI, delta_SLG, delta_AVG):
    # Creates path to models
    path = os.path.join(settings.MODELS, 'models.p')
 
    # Loads logistic regression model from pickle file
    with open(path, 'rb') as pickled:
       data = pickle.load(pickled)
    logreg = data['regression']

    # Stores the team stats in a numpy array and predicts the outcome of the game
    team_stats = np.array([delta_ERA, delta_RBI, delta_SLG, delta_AVG]).reshape(1, 4)
    prediction = logreg.predict(team_stats)

    return prediction