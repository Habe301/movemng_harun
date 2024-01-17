from flask import Flask, render_template, redirect, url_for, jsonify, request, send_from_directory, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__, static_folder='docs')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secret key for security
db = SQLAlchemy(app)


# Datenbankmigration
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(500), nullable=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean, default=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    start = db.Column(db.String(80), nullable=False)

with app.app_context(): 
    db.create_all()
        

# Beispielroute für Startseite
@app.route("/")
def startpage():
    return render_template('index.html')




tasks = [
    {"id": 1, "title": "Altes Mietverhältnis kündigen", "category": "before", "completed": False},
    {"id": 2, "title": "Freien Tag bei Arbeitgeber beantragen", "category": "before", "completed": False},
    {"id": 3, "title": "Inventarliste erstellen", "category": "before", "completed": False},
    {"id": 4, "title": "Packen", "category": "before", "completed": False},
    {"id": 5, "title": "Umzugsauto reservieren", "category": "before", "completed": False},
    {"id": 6, "title": "Umzugsgut aussortieren", "category": "before", "completed": False},
    {"id": 7, "title": "Umzugsunternehmen oder Freunde kontaktieren", "category": "before", "completed": False},
    {"id": 8, "title": "Verpackungsmaterial besorgen (Karton, Luftpolsterfolie)", "category": "before", "completed": False},
    {"id": 9, "title": "Versicherungen überprüfen (Hausratsversicherung)", "category": "before", "completed": False},
    {"id": 10, "title": "Haustiere an einem ruhigen Ort rüberbringen", "category": "during", "completed": False},
    {"id": 11, "title": "Kommunikation mit Umzugsunternehmen", "category": "during", "completed": False},
    {"id": 12, "title": "Letzte Runde, schauen ob was fehlt", "category": "during", "completed": False},
    {"id": 13, "title": "Schlüsselübergabe", "category": "during", "completed": False},
    {"id": 14, "title": "Schranktüren und Schubladen mit Klebeband verschliessen", "category": "during", "completed": False},
    {"id": 15, "title": "Schrauben- und Nagellöcher zuspachteln", "category": "during", "completed": False},
    {"id": 16, "title": "Zugang zur neuen Wohnung sicherstellen", "category": "during", "completed": False},
    {"id": 17, "title": "Einrichtung der Möbel planen", "category": "after", "completed": False},
    {"id": 18, "title": "Nachsendeauftrag überprüfen", "category": "after", "completed": False},
    {"id": 19, "title": "Neue Adressen aktualisieren", "category": "after", "completed": False},
    {"id": 20, "title": "Sicherheitssysteme prüfen (Rauchmelder)", "category": "after", "completed": False},
    {"id": 21, "title": "Wohnungseinweihung planen", "category": "after", "completed": False},
    {"id": 22, "title": "Wohnungsinspektion (Ausschau halten nach Mängel)", "category": "after", "completed": False},
    {"id": 23, "title": "Arbeitgeber", "category": "adresschange", "completed": False},
    {"id": 24, "title": "Banken", "category": "adresschange", "completed": False},
    {"id": 25, "title": "Freunde und Familie", "category": "adresschange", "completed": False},
    {"id": 26, "title": "Gemeinde", "category": "adresschange", "completed": False},
    {"id": 27, "title": "Hausarzt", "category": "adresschange", "completed": False},
    {"id": 28, "title": "Krankenkassen", "category": "adresschange", "completed": False},
    {"id": 29, "title": "Laufende Abbonements und Mitgliedschaften", "category": "adresschange", "completed": False},
    {"id": 30, "title": "Post (Nachsendeauftrag)", "category": "adresschange", "completed": False},
    {"id": 31, "title": "Schule/Kindergarten (bei Kindern)", "category": "adresschange", "completed": False},
    {"id": 32, "title": "Strassenverkehrsamt", "category": "adresschange", "completed": False},
    {"id": 33, "title": "Telefon- und Internetanbieter", "category": "adresschange", "completed": False},
    {"id": 34, "title": "Vereine", "category": "adresschange", "completed": False},
    {"id": 35, "title": "Versicherungen", "category": "adresschange", "completed": False},
    {"id": 36, "title": "Backofen", "category": "clean", "completed": False},
    {"id": 37, "title": "Badezimmer", "category": "clean", "completed": False},
    {"id": 38, "title": "Böden", "category": "clean", "completed": False},
    {"id": 39, "title": "Dampfabzug", "category": "clean", "completed": False},
    {"id": 40, "title": "Kühlschrank", "category": "clean", "completed": False},
    {"id": 41, "title": "Rollläden", "category": "clean", "completed": False},
    {"id": 42, "title": "Spülmaschine", "category": "clean", "completed": False},
    {"id": 43, "title": "Waschbecken", "category": "clean", "completed": False},
    {"id": 44, "title": "Waschmaschine", "category": "clean", "completed": False},
]
 
with app.app_context():
    db.create_all()
    Task.query.delete()  # Delete all tasks
    for task in tasks:
        new_task = Task(id=task["id"], title=task["title"], category=task["category"], completed=task["completed"])
        db.session.add(new_task)
    db.session.commit()

# Code für Kalender
events = [
        { "id": 1, "title": 'my event', "start": '2024-01-17' },
        { "id": 2, "title": 'my event 2', "start": '2024-01-18' },
        { "id": 3, "title": 'my event 3', "start": '2024-01-19' },
    ]

@app.route('/calendar_view')
def calendar():
    return render_template('calendar.html')

@app.route('/events')
def events():
    events = Event.query.all()
    return jsonify([{'id': event.id, 'title': event.title, 'start': event.start} for event in events])

@app.route('/add_event', methods=['POST'])
def add_event():
    event_data = request.get_json()
    event = Event(title=event_data['title'], start=event_data['start'])
    db.session.add(event)
    db.session.commit()
    return jsonify({'id': event.id, 'title': event.title, 'start': event.start}), 201




# Code für Taskliste
@app.route('/handle_data', methods=['POST'])
def handle_data():
    tasks = request.form.getlist('task')
    for task in tasks:
        print(task)
    return 'Tasks received'

@app.route("/tasks")
def show_tasks():
    tasks = Task.query.all()
    print(tasks)
    return render_template("liste.html", tasks=tasks)

@app.route('/update_task', methods=['POST'])
def update_task():
    task_update = request.get_json()
    task = Task.query.get(task_update['id'])
    if task:
        task.completed = task_update['completed']
        db.session.commit()
        return jsonify(task_update), 200
    return jsonify({'error': 'Task not found'}), 404



#Code für Docs
@app.route('/documents')
def documents():
    return render_template("docs.html")

@app.route('/documents/<path:filename>')
def download_file(filename):
    return send_from_directory('documents', filename)



if __name__ == "__main__":
    app.run(debug=True)



