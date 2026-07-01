import os
FLASK_HOST="0.0.0.0"
FLASK_PORT=8000

MONGODB_URI = 'mongodb://localhost:27017/'
MONGO_URL = MONGODB_URI

db_name='test_db'
MONGO_DB_NAME = db_name

users_collection_name = 'collection_users'
MONGO_USERS_COLLECTION = users_collection_name

data_collection_name = 'collection_data'
MONGO_DATA_COLLECTION = data_collection_name

INPUT_DATA_PATH = os.path.join(os.getcwd(), "data", "medical_insurance.csv")
ML_MODEL_PATH = os.path.join(os.getcwd(),"artifacts","linear_reg_med_ins.pkl")

STD_SCALER_FILE_PATH = os.path.join(os.getcwd(), "artifacts", "std_scaler_med_ins.pkl")

INPUT_COLUMN_DATA = os.path.join(os.getcwd(), "artifacts", "med_ins_column_data.json")