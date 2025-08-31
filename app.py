from flask import Flask, render_template, request, jsonify
from database import Database
from huggingface_api import generate_questions
import json

app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializar banco de dados
db = Database(app.config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_flashcards', methods=['POST'])
def generate_flashcards():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texto não fornecido'}), 400
        
        # Gerar perguntas usando Hugging Face
        questions_answers = generate_questions(text)
        
        # Salvar no banco de dados
        for qa in questions_answers:
            db.insert_flashcard(qa['question'], qa['answer'])
        
        return jsonify(questions_answers)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_flashcards', methods=['GET'])
def get_flashcards():
    try:
        flashcards = db.get_flashcards()
        return jsonify(flashcards)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)