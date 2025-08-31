document.addEventListener('DOMContentLoaded', function() {
    const generateBtn = document.getElementById('generate-btn');
    const loadSavedBtn = document.getElementById('load-saved-btn');
    const studyNotes = document.getElementById('study-notes');
    const flashcardsContainer = document.getElementById('flashcards-container');
    const loader = document.getElementById('loader');
    const successMessage = document.getElementById('success-message');
    
    // Função para criar um flashcard
    function createFlashcard(question, answer, id = null) {
        const flashcard = document.createElement('div');
        flashcard.className = 'flashcard';
        if (id) flashcard.dataset.id = id;
        
        flashcard.innerHTML = `
            <div class="flashcard-inner">
                <div class="flashcard-front">
                    <div class="card-content">
                        <h3>Pergunta</h3>
                        <p>${question}</p>
                    </div>
                </div>
                <div class="flashcard-back">
                    <div class="card-content">
                        <h3>Resposta</h3>
                        <p>${answer}</p>
                    </div>
                </div>
            </div>
        `;
        
        flashcard.addEventListener('click', function() {
            this.classList.toggle('flipped');
        });
        
        return flashcard;
    }
    
    // Função para exibir flashcards
    function displayFlashcards(flashcards) {
        flashcardsContainer.innerHTML = '';
        
        if (flashcards.length === 0) {
            flashcardsContainer.innerHTML = '<div class="placeholder"><p>Nenhum flashcard encontrado.</p></div>';
            return;
        }
        
        flashcards.forEach(card => {
            const flashcardElement = createFlashcard(card.question, card.answer, card.id || null);
            flashcardsContainer.appendChild(flashcardElement);
        });
    }
    
    // Função para mostrar mensagem de erro
    function showError(message) {
        // Remover mensagens de erro existentes
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        const inputSection = document.querySelector('.input-section');
        inputSection.appendChild(errorDiv);
        
        setTimeout(() => {
            errorDiv.style.display = 'block';
        }, 10);
        
        // Esconder após 5 segundos
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
    
    // Gerar flashcards
    generateBtn.addEventListener('click', function() {
        const notes = studyNotes.value.trim();
        
        if (notes === '') {
            showError('Por favor, insira suas anotações de estudo.');
            return;
        }
        
        // Mostrar loader
        loader.style.display = 'block';
        
        // Fazer requisição para o backend
        fetch('/generate_flashcards', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: notes })
        })
        .then(response => response.json())
        .then(data => {
            // Esconder loader
            loader.style.display = 'none';
            
            if (data.error) {
                showError('Erro: ' + data.error);
                return;
            }
            
            // Mostrar mensagem de sucesso
            successMessage.style.display = 'block';
            
            // Exibir flashcards
            displayFlashcards(data);
            
            // Esconder mensagem de sucesso após 3 segundos
            setTimeout(function() {
                successMessage.style.display = 'none';
            }, 3000);
        })
        .catch(error => {
            console.error('Error:', error);
            loader.style.display = 'none';
            showError('Ocorreu um erro ao gerar os flashcards.');
        });
    });
    
    // Carregar flashcards salvos
    loadSavedBtn.addEventListener('click', function() {
        fetch('/get_flashcards')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError('Erro: ' + data.error);
                return;
            }
            
            // Exibir flashcards
            displayFlashcards(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Ocorreu um erro ao carregar os flashcards.');
        });
    });
    
    // Preencher com texto de exemplo para facilitar a demonstração
    studyNotes.value = "Fotossíntese é o processo pelo qual plantas, algas e algumas bactérias convertem luz solar, dióxido de carbono e água em glicose e oxigênio. Este processo ocorre nos cloroplastos e é vital para a vida na Terra, pois produz oxigênio e serve como base para a cadeia alimentar. A fotossíntese consiste em duas etapas principais: as reações dependentes de luz (que capturam energia luminosa) e o ciclo de Calvin (que fixa o carbono para produzir glicose).";
});