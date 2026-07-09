import os

# 1. Conteúdo do Frontend (HTML + Bootstrap 5)
html_code = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BiblioIA - Agente de Livros</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #fcfbf9; font-family: 'Segoe UI', sans-serif; }
        .hero { background: linear-gradient(135deg, #2c3e50 0%, #0f2027 100%); color: white; padding: 40px 0; border-bottom: 4px solid #deff9a; }
        .card { border: none; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); }
    </style>
</head>
<body>
    <div class="hero text-center mb-5">
        <h1 class="display-4 fw-bold">📚 BiblioIA</h1>
        <p class="lead">Seu Agente Inteligente de Atendimento e Recomendação Literária</p>
    </div>
    <div class="container">
        <div class="row">
            <div class="col-md-5 mb-4">
                <div class="card p-4">
                    <h3 class="text-secondary mb-4">Suas Preferências</h3>
                    <form id="bookForm">
                        <div class="mb-3">
                            <label class="form-label">Gênero favorito</label>
                            <select class="form-select" id="genero">
                                <option value="ficcao">Ficção Científica</option>
                                <option value="misterio">Mistério e Suspense</option>
                                <option value="desenvolvimento">Desenvolvimento Pessoal</option>
                            </select>
                        </div>
                        <button type="submit" class="btn btn-dark w-100 py-2">Consultar IA ✨</button>
                    </form>
                </div>
            </div>
            <div class="col-md-7">
                <div class="card p-4" style="min-height: 250px;">
                    <h3 class="text-secondary">Sugestão do Agente</h3>
                    <div id="result" class="mt-3 text-muted">
                        Preencha o formulário para ativar o agente literário...
                    </div>
                </div>
            </div>
        </div>
    </div>
    <script src="js/script.js"></script>
</body>
</html>'''

# 2. Conteúdo do Front-end JavaScript (Assíncrono)
js_code = '''document.getElementById('bookForm').addEventListener('submit', async (e) => {
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
});'''

# 3. Conteúdo do Back-end (Flask API preparado para o Render)
backend_code = '''import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/recommend-books', methods=['POST'])
def recommend():
    data = request.json or {}
    genero = data.get('genero', 'ficcao')
    
    if genero == 'ficcao':
        cat = "Ficção Científica & Universos Expandidos"
    elif genero == 'misterio':
        cat = "Mistério & Suspense Psicológico"
    else:
        cat = "Desenvolvimento Pessoal & Alta Performance"
        
    return jsonify({
        "categoria": cat,
        "status": "Sucesso"
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
'''

# 4. Conteúdo do Banco de Dados para o Neon.tech
sql_code = '''CREATE TABLE IF NOT EXISTS historico_livros (
    id SERIAL PRIMARY KEY,
    genero_solicitado VARCHAR(50),
    data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);'''

# Executando a automação de diretórios
print("Iniciando a criação das pastas estruturadas...")
os.makedirs("biblioia-projeto/frontend/js", exist_ok=True)
os.makedirs("biblioia-projeto/backend", exist_ok=True)
os.makedirs("biblioia-projeto/database", exist_ok=True)

print("Escrevendo os códigos base...")
with open("biblioia-projeto/frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html_code)
with open("biblioia-projeto/frontend/js/script.js", "w", encoding="utf-8") as f:
    f.write(js_code)
with open("biblioia-projeto/backend/app.py", "w", encoding="utf-8") as f:
    f.write(backend_code)
with open("biblioia-projeto/backend/requirements.txt", "w", encoding="utf-8") as f:
    f.write("Flask==3.0.2\nFlask-CORS==4.0.0\n")
with open("biblioia-projeto/database/schema.sql", "w", encoding="utf-8") as f:
    f.write(sql_code)

print("\n===================================================\n")
print("  PROJETO 'biblioia-projeto' CRIADO COM SUCESSO! ")
print("===================================================\n")
print("Para rodar o backend localmente:")
print("1. cd biblioia-projeto/backend")
print("2. pip install -r requirements.txt")
print("3. python app.py")
print("\nAbra o arquivo frontend/index.html em seu navegador.")