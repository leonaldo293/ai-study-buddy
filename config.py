import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Configurações do Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')
    
    # Configurações do MySQL (XAMPP padrão)
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'flashcard_db')
    MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
    
    # Configurações do Hugging Face - Modelo mais adequado para geração de perguntas
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY', 'sua_chave_api_huggingface')
    HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'google/t5-v1_1-large')