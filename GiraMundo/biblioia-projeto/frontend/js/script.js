document.getElementById('bookForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const genero = document.getElementById('genero').value;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<div class="spinner-border text-dark" role="status"></div><p class="mt-2">Consultando a inteligência literária...</p>';
    
    try {
        const response = await fetch('http://localhost:5000/api/v1/recommend-books', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ genero })
        });
        const data = await response.json();
        resultDiv.innerHTML = `<h4>💡 Categoria Sugerida: <span class="text-primary">${data.categoria}</span></h4>
                               <p class="mt-3 text-success">✓ Resposta mockada recebida com sucesso do Back-end!</p>`;
    } catch(err) {
        resultDiv.innerHTML = '<span class="text-danger">Erro ao falar com o agente backend. Verifique se ele está ativo localmente na porta 5000.</span>';
    }
});