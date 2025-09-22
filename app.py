from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DB = 'notes.db'

# Initialize database
def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        conn.execute('CREATE TABLE notes (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)')
        conn.close()

init_db()

@app.route('/')
def home():
    return "Cloud Notes API is running! Use /add, /list, /delete/<id> endpoints."

@app.route('/add', methods=['POST'])
def add_note():
    data = request.json
    content = data.get('content') if data else None
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note added successfully!'})

@app.route('/list', methods=['GET'])
def list_notes():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('SELECT * FROM notes')
    notes = [{'id': row[0], 'content': row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify(notes)

@app.route('/delete/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute('DELETE FROM notes WHERE id=?', (note_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Note deleted successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
