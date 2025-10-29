# 🚀 Opunnence API v2

Backend base para **Opunnence**, con:
- FastAPI
- PostgreSQL
- SQLAlchemy
- Deploy automático en Render
- Dominio personalizado: api.opunnence.com

---

## 🧩 Estructura

```
opunnence_api/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       └── users.py
│
├── requirements.txt
├── .env.example
├── render.yaml
└── README.md
```

---

## ▶️ Ejecución local

```bash
python -m venv venv
source venv/bin/activate  # o venv\Scripts\activate (Windows)
pip install -r requirements.txt
cp .env.example .env
# Opcional: crea un archivo `.env.local` (se ignora en git) y define ahí tu `DATABASE_URL`.
# Si mantienes el valor de ejemplo, la app usará SQLite local (`opunnence.db`) para desarrollo.
# Para usar un PostgreSQL local (por ejemplo Docker), define en tu entorno:
#   DATABASE_URL=postgresql://usuario:password@localhost:5432/tu_db
# o añade esa línea en `.env.local` únicamente en tu máquina.
uvicorn app.main:app --reload
```

🚀 Deploy en Render

Sube el proyecto a GitHub.

En Render:

- Crea un servicio PostgreSQL.
- Crea un Web Service y selecciona este repo.
- Añade la variable DATABASE_URL con el valor del PostgreSQL.
- Agrega el dominio: api.opunnence.com → Render generará automáticamente SSL.

---

## 🧠 Endpoints

| Método | Ruta      | Descripción     |
|--------|-----------|-----------------|
| GET    | /         | Home            |
| GET    | /health   | Estado          |
| POST   | /users    | Crear usuario   |
| GET    | /users    | Listar usuarios |

Ejemplo de uso:

```bash
curl -X POST https://api.opunnence.com/users \
-H "Content-Type: application/json" \
-d '{"name": "Fernando", "email": "fernando@opunnence.com"}'
```

✅ Devuelve el usuario creado.

---

## ✅ Despliegue final (Resumen rápido)

| Etapa | Acción                       | Resultado                          |
|-------|------------------------------|------------------------------------|
| 1️⃣    | Crear repo en GitHub          | `opunnence_api`                    |
| 2️⃣    | Crear Web Service (Render)   | `https://opunnence-api.onrender.com` |
| 3️⃣    | Crear DB PostgreSQL (Render) | `DATABASE_URL` disponible          |
| 4️⃣    | Añadir Custom Domain         | `api.opunnence.com`                |
| 5️⃣    | Esperar verificación SSL     | API 100% operativa ✅              |

---

¿Quieres que te genere también el **script SQL inicial** para crear la tabla `users` automáticamente (útil si prefieres manejar la DB manualmente o probarla localmente)?
