CREATE TABLE IF NOT EXISTS historico_livros (
    id SERIAL PRIMARY KEY,
    genero_solicitado VARCHAR(50),
    data_consulta TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);