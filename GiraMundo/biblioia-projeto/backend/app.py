import os
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
