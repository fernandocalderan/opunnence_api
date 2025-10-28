-- Crear tabla 'users' para Opunnence API
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Insertar datos de ejemplo opcionales
INSERT INTO users (name, email)
VALUES
    ('Fernando Aringhieri Calderan', 'fernando@opunnence.com'),
    ('Lilian Aguiar', 'lilian@opunnence.com')
ON CONFLICT (email) DO NOTHING;

-- Verificar contenido
SELECT * FROM users;
