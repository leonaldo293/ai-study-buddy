import mysql.connector
from mysql.connector import Error
import time

class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.connect()
        self.create_table()

    def connect(self):
        max_retries = 5
        retry_delay = 2  # segundos
        
        for attempt in range(max_retries):
            try:
                self.connection = mysql.connector.connect(
                    host=self.config['MYSQL_HOST'],
                    user=self.config['MYSQL_USER'],
                    password=self.config['MYSQL_PASSWORD'],
                    database=self.config['MYSQL_DB'],
                    port=self.config['MYSQL_PORT']
                )
                if self.connection.is_connected():
                    print("Conexão ao MySQL estabelecida com sucesso")
                    return
            except Error as e:
                print(f"Tentativa {attempt + 1}/{max_retries}: Erro ao conectar ao MySQL: {e}")
                if attempt < max_retries - 1:
                    print(f"Tentando novamente em {retry_delay} segundos...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Aumentar o delay exponencialmente
                else:
                    print("Não foi possível conectar ao MySQL após várias tentativas")
                    raise

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS flashcards (
            id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(create_table_query)
            self.connection.commit()
            print("Tabela 'flashcards' criada ou já existe")
        except Error as e:
            print(f"Erro ao criar tabela: {e}")

    def insert_flashcard(self, question, answer):
        insert_query = "INSERT INTO flashcards (question, answer) VALUES (%s, %s)"
        try:
            cursor = self.connection.cursor()
            cursor.execute(insert_query, (question, answer))
            self.connection.commit()
            print("Flashcard inserido com sucesso")
            return cursor.lastrowid
        except Error as e:
            print(f"Erro ao inserir flashcard: {e}")
            return None

    def get_flashcards(self):
        select_query = "SELECT id, question, answer FROM flashcards ORDER BY created_at DESC"
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(select_query)
            flashcards = cursor.fetchall()
            return flashcards
        except Error as e:
            print(f"Erro ao buscar flashcards: {e}")
            return []