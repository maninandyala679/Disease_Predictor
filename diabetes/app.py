from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load models
diabetes_model = pickle.load(open('saved_models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('saved_models/heart_disease_model.sav', 'rb'))
parkinsons_model = pickle.load(open('saved_models/parkinsons_model.sav', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes_prediction():
    result = None
    if request.method == 'POST':
        try:
            inputs = [float(request.form[key]) for key in [
                'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
                'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
            ]]
            prediction = diabetes_model.predict([inputs])[0]
            result = 'The person is diabetic' if prediction == 1 else 'The person is not diabetic'
        except ValueError:
            result = "Invalid input. Please enter numeric values."

    diabetes_fields = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]
    
    return render_template('diabetes.html', result=result, fields=diabetes_fields)

@app.route('/predict', methods=['POST'])
def predict_diabetes():
    try:
        data = request.get_json()
        features = [float(value) for value in data.values()]
        prediction = diabetes_model.predict([features])[0]
        return jsonify({"result": "Yes" if prediction == 1 else "No"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/heart_disease', methods=['GET', 'POST'])
def heart_disease_prediction():
    result = None
    if request.method == 'POST':
        try:
            inputs = [float(request.form[key]) for key in [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]]
            prediction = heart_disease_model.predict([inputs])[0]
            result = 'The person has heart disease' if prediction == 1 else 'The person does not have heart disease'
        except ValueError:
            result = "Invalid input. Please enter numeric values."

    heart_disease_fields = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    return render_template('heart_disease.html', result=result, fields=heart_disease_fields)

@app.route('/predict_heart', methods=['POST'])
def predict_heart():
    try:
        data = request.get_json()
        features = [float(value) for value in data.values()]
        prediction = heart_disease_model.predict([features])[0]
        return jsonify({"result": "Yes" if prediction == 1 else "No"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/parkinsons', methods=['GET', 'POST'])
def parkinsons_prediction():
    result = None
    if request.method == 'POST':
        try:
            # Fetching the inputs based on the updated field names
            inputs = [float(request.form[key]) for key in [
                'mdvp_fo', 'mdvp_fhi', 'mdvp_flo', 'mdvp_jitter',
                'mdvp_jitter_abs', 'mdvp_rap', 'mdvp_ppq', 'jitter_ddp',
                'mdvp_shimmer', 'mdvp_shimmer_db', 'shimmer_apq3',
                'shimmer_apq5', 'mdvp_apq', 'shimmer_dda', 'nhr', 'hnr',
                'rpde', 'dfa', 'spread1', 'spread2', 'd2', 'ppe'
            ]]
            prediction = parkinsons_model.predict([inputs])[0]
            result = "The person has Parkinson's disease" if prediction == 1 else "The person does not have Parkinson's disease"
        except ValueError:
            result = "Invalid input. Please enter numeric values."

    parkinsons_fields = [
        'mdvp_fo', 'mdvp_fhi', 'mdvp_flo', 'mdvp_jitter',
        'mdvp_jitter_abs', 'mdvp_rap', 'mdvp_ppq', 'jitter_ddp',
        'mdvp_shimmer', 'mdvp_shimmer_db', 'shimmer_apq3',
        'shimmer_apq5', 'mdvp_apq', 'shimmer_dda', 'nhr', 'hnr',
        'rpde', 'dfa', 'spread1', 'spread2', 'd2', 'ppe'
    ]
    
    return render_template('parkinsons.html', result=result, fields=parkinsons_fields)

@app.route('/predict_parkinsons', methods=['POST'])
def predict_parkinsons():
    try:
        data = request.get_json()
        features = [float(value) for value in data.values()]
        prediction = parkinsons_model.predict([features])[0]
        return jsonify({"result": "Yes" if prediction == 1 else "No"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
