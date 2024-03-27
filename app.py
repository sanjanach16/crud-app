from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient(host='test_mongodb', port=27017,
                     username='root', password='pass', authSource="admin")
db = client.mytododb
students_collection = db.students


@app.route('/')
def index_redirect():
    return redirect(url_for('add_student_form'))


@app.route('/index.html')
def add_student_form():
    return render_template('index.html')


@app.route('/homepage')
def homepage():
    students = students_collection.find()
    return render_template('homepage.html', students=students)


@app.route('/add_student', methods=['POST'])
def add_student():
    if request.method == 'POST':
        student_data = {
            'name': request.form['name'],
            'roll_number': request.form['roll_number'],
            'grade': request.form['grade']
        }
        students_collection.insert_one(student_data)
    return redirect(url_for('index_redirect'))


@app.route('/edit_student/<student_id>', methods=['POST'])
def edit_student(student_id):
    if request.method == 'POST':
        try:
            students_collection.update_one({'_id': ObjectId(student_id)}, {'$set': {
                'name': request.json['name'],
                'roll_number': request.json['roll_number'],
                'grade': request.json['grade']
            }})
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/delete_student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        students_collection.delete_one({'_id': ObjectId(student_id)})
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
