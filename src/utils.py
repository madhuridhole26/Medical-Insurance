import config
import pickle
import json

import pandas as pd
import numpy as np
from src.database import get_data_collection

class MedicalInsurance():
    def __init__(self):
        pass

    def load_model(self):
        """
            This method is used to load the model
        """
        with open(config.ML_MODEL_PATH, 'rb') as f:
            self.model = pickle.load(f)
        return ""
    
    def load_column_data(self):
        """
            This method is used to load the column data
        """
        with open(config.INPUT_COLUMN_DATA, 'r') as f:
            self.input_columns = json.load(f)

        return self.input_columns
    
    def create_test_df(self):
        """
            This method is used to create a test dataframe
        """
        self.load_model()
        self.load_column_data()

        test_array = np.zeros((1,self.model.n_features_in_))
        test_array[0,0] = self.data['age']
        test_array[0,1] = self.input_columns['gender'][self.data['gender']]
        test_array[0,2] = self.data['bmi']
        test_array[0,3] = self.data['children']
        test_array[0,4] = self.input_columns['smoker'][self.data['smoker']]

        region = f"region_{self.data['region']}"

        region_index = np.where(self.model.feature_names_in_ == region)[0]
        test_array[0,region_index] = 1
        self.test_df = pd.DataFrame(test_array, columns=self.model.feature_names_in_)

    def predict_charges(self, user_input_data):
        self.data = dict(user_input_data)
        self.data['age'] = int(self.data['age'])
        self.data['bmi'] = float(self.data['bmi'])
        self.data['children'] = int(self.data['children'])
        self.create_test_df()

        self.prediction = np.around(self.model.predict(self.test_df),4)
        print("Predicted Charges are:", self.prediction)
        self.save_data_in_db()
        return self.prediction

    def save_data_in_db(self):
        input_data = self.data
        input_data.update({"Prediction" : self.prediction[0]})
        data_collection = get_data_collection()

        data_collection.insert_one(input_data)