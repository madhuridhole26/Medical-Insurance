from flask import Flask, jsonify, request,request,render_template,url_for,redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  
import config
from src.utils import MedicalInsurance
import datetime

medical_insurance_object = MedicalInsurance()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = "secret"  # Change this to a random secret key in production

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = "flask_session_secret"   # Set the expiration time for the access token

jwt = JWTManager(app)

STATIC_USERS = [
    {
        "username": "admin",
        "email_id": "admin@example.com",
        "password": "admin123",
        "dob": "1990-01-01",
        "contact_number": "0000000000"
    }
]

def find_static_user(user_name=None, email_id=None, password=None):
    for user in STATIC_USERS:
        if password is not None and user["password"] != password:
            continue
        if user_name and user["username"] == user_name:
            return user
        if email_id and user["email_id"] == email_id:
            return user
    return None

@app.route('/')
def home():
    return redirect(url_for('login_page'))

@app.route('/register', methods=['GET'])
@app.route('/register_page', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET'])
@app.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/forgot-password', methods=['GET'])
@app.route('/forget_password_page', methods=['GET'])
def forgot_password():
    return render_template('forgot_password.html')

@app.route('/prediction_page' )
def prediction_page():
    token = request.args.get('token')
    return render_template('prediction.html', token=token)

@app.route('/register', methods=['POST'])
def register_user():
    return jsonify({"status": "fail", "message": "Registration is disabled. Use the static login credentials."})

@app.route('/login', methods=['POST'])
def login():
    user_data = request.form
    user_name = user_data.get('user_name')
    email_id = user_data.get('email_id')
    password = user_data.get('password')

    response = find_static_user(user_name=user_name, email_id=email_id, password=password)
    if response:
        identity = user_name if user_name else email_id
        access_token = create_access_token(
            identity=identity,
            expires_delta=datetime.timedelta(minutes=60)
        )
        return jsonify({"status": "success", "message": "Login successful", "access_token": access_token})
    else:
        return jsonify({"status": "fail", "message": "Invalid username/email or password"})

@app.route('/forgot-password', methods=['POST'])
def forgot_password_post():
    user_data = request.form
    user_name = user_data.get('user_name')
    dob = user_data.get('dob')

    response = find_static_user(user_name=user_name, email_id=None, password=None)
    if response and response.get('dob') == dob:
        return jsonify({"status": "fail", "message": "Password reset is disabled for static credentials."})
    else:
        return jsonify({"status": "fail", "message": "Invalid username or date of birth"})

@app.route('/gender_options', methods=['GET'])
@jwt_required()
def gender_options():
    col_data= medical_insurance_object.load_column_data()
    gender_values = list(col_data['gender'].keys())
    return jsonify(gender_values)

@app.route('/smoker_options', methods=['GET'])
@jwt_required()
def smoker_options():
    col_data= medical_insurance_object.load_column_data()
    smoker_values = list(col_data['smoker'].keys())
    return jsonify(smoker_values)

@app.route('/region_options', methods=['GET'])
@jwt_required()
def region_options():
    col_data= medical_insurance_object.load_column_data()
    region_values = [feature.replace("region_", "") for feature in col_data['colName'] if feature.startswith("region_")]
    return jsonify(region_values)

@app.route('/predict', methods=['POST'])
@jwt_required()

def predict():
    user_input_data = request.form
    prediction_result = medical_insurance_object.predict_charges(user_input_data)
    return jsonify({"status": "success", "Predicted Charges": prediction_result[0]})

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=True)