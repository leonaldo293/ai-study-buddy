import requests
import time
import re
from config import Config

def generate_questions(text):
    """
    Gera perguntas com base no texto usando a API do Hugging Face
    Usando um modelo mais adequado para geração de perguntas
    """
    try:
        # URL da API do Hugging Face
        api_url = f"https://api-inference.huggingface.co/models/{Config.HUGGINGFACE_MODEL}"
        
        # Headers com a chave API
        headers = {
            "Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Prompt mais específico para geração de perguntas
        prompt = f"""
        Com base no seguinte texto, gere 5 perguntas e respostas relevantes para flashcards de estudo.
        Formate cada pergunta e resposta no padrão: 
        PERGUNTA: [texto da pergunta]
        RESPOSTA: [texto da resposta]
        
        Texto:
        {text[:2000]}  # Limitar o tamanho do texto para evitar problemas
        """
        
        # Preparar o payload
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 800,
                "temperature": 0.9,
                "top_p": 0.9,
                "num_return_sequences": 1,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        # Fazer a requisição
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Verificar se a resposta é válida
        if response.status_code == 200:
            result = response.json()
            generated_text = result[0]['generated_text']
            
            # Processar o texto gerado para extrair perguntas e respostas
            questions_answers = parse_generated_text(generated_text)
            
            # Se não obteve perguntas suficientes, usar fallback
            if len(questions_answers) < 3:
                questions_answers.extend(get_fallback_questions(text))
                
            return questions_answers[:5]  # Retornar no máximo 5 perguntas
            
        elif response.status_code == 503:
            # Modelo está carregando, tentar novamente após um tempo
            print("Modelo está carregando, tentando novamente em 20 segundos...")
            time.sleep(20)
            return generate_questions(text)  # Tentar novamente
        else:
            print(f"Erro na API: {response.status_code}, {response.text}")
            return get_fallback_questions(text)
            
    except Exception as e:
        print(f"Erro ao gerar perguntas: {e}")
        return get_fallback_questions(text)

def parse_generated_text(text):
    """
    Processa o texto gerado pela IA para extrair perguntas e respostas
    usando expressões regulares para maior robustez
    """
    questions_answers = []
    
    # Padrões para encontrar perguntas e respostas
    patterns = [
        r"PERGUNTA:\s*(.*?)\s*RESPOSTA:\s*(.*?)(?=PERGUNTA:|$)",
        r"QUESTION:\s*(.*?)\s*ANSWER:\s*(.*?)(?=QUESTION:|$)",
        r"P:\s*(.*?)\s*R:\s*(.*?)(?=P:|$)",
        r"Q:\s*(.*?)\s*A:\s*(.*?)(?=Q:|$)"
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)
        for match in matches:
            if len(match) == 2:
                question = match[0].strip()
                answer = match[1].strip()
                
                # Remover possíveis números ou marcadores no início
                question = re.sub(r'^\d+[\.\)]\s*', '', question)
                answer = re.sub(r'^\d+[\.\)]\s*', '', answer)
                
                if question and answer and len(question) > 10 and len(answer) > 5:
                    questions_answers.append({
                        "question": question,
                        "answer": answer
                    })
    
    return questions_answers

def get_fallback_questions(text):
    """
    Gera perguntas fallback caso a API não funcione
    Baseado em heurísticas simples de extração de informações do texto
    """
    questions = []
    
    # Dividir o texto em frases
    sentences = re.split(r'[.!?]', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    # Criar perguntas com base nas frases mais longas
    for i, sentence in enumerate(sentences[:5]):
        if sentence:
            # Extrair conceitos importantes (palavras com letra maiúscula)
            concepts = re.findall(r'\b[A-Z][a-z]+\b', sentence)
            
            if concepts:
                question = f"O que é {concepts[0]}?"
                answer = sentence
            else:
                # Se não encontrar conceitos, criar pergunta genérica
                words = sentence.split()
                if len(words) > 5:
                    question = f"Explique: '{' '.join(words[:5])}...'"
                    answer = sentence
            
            questions.append({
                "question": question,
                "answer": answer
            })
    
    return questions