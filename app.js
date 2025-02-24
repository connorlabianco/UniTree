from flask import Flask, render_template, jsonify
from flask import Flask, request, jsonify

app = Flask(__name__)

#EXAMPLE DATA 
class_data = [
    {"name": "CS 156", "units": 4, "time": "MWF 10-11am"},
    {"name": "CS 170", "units": 4, "time": "TTh 2-3:30pm"}
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/classes')
def get_classes():
    return jsonify(class_data)

# Example storage for the classes
user_classes = []

@app.route('/api/saveClasses', methods=['POST'])
def save_classes():
    data = request.get_json()
    classes = data.get('classes', [])
    
    # Save the classes (you can store them in a database instead of a list)
    user_classes.extend(classes)
    
    return jsonify({'message': 'Classes saved successfully!', 'classes': user_classes}), 200

if __name__ == '__main__':
    app.run(debug=False, port=5000)  
