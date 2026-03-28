# VetPremium — Backend API

API REST construida con **FastAPI + PostgreSQL + SQLAlchemy**. Gestiona mascotas, dueños, citas, historial médico, hospitalización, inventario, facturación y más.

---

## Tecnologías

| Tech | Versión |
|---|---|
| Python | 3.10 |
| FastAPI | 0.110 |
| SQLAlchemy | 2.0 |
| PostgreSQL | 16 |
| Alembic | 1.13 |
| Uvicorn | 0.27 |

---

## Requisitos previos

- [Docker](https://www.docker.com/products/docker-desktop) y Docker Compose **— opción recomendada**
- O bien: Python 3.10+ y PostgreSQL instalados localmente

---

## Instalación con Docker (recomendado)

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd veterinary-medicine-back

# 2. Levantar la base de datos y el servidor
docker compose up -d

# 3. Listo — API disponible en:
#    http://localhost:8000
#    http://localhost:8000/docs  (Swagger UI)
```

Para bajar los contenedores:

```bash
docker compose down
```

Para bajar y eliminar los datos de la base de datos:

```bash
docker compose down -v
```

---

## Instalación local (sin Docker)

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd veterinary-medicine-back

# 2. Crear entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
#    Crea un archivo .env en la raíz con:
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/veterinaria
SECRET_KEY=tu_clave_secreta

# 5. Correr migraciones
alembic upgrade head

# 6. Iniciar el servidor
uvicorn main:app --reload
```

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `DATABASE_URL` | Conexión a PostgreSQL | `postgresql://postgres:28demarzo@localhost:5432/veterinaria` |
| `SECRET_KEY` | Clave para firmar JWT | `supersecretkey` |

---

## Endpoints principales

| Módulo | Prefijo |
|---|---|
| Usuarios / Auth | `/users` |
| Mascotas | `/pets` |
| Dueños | `/owners` |
| Citas | `/appointments` |
| Historial médico | `/medical-records` |
| Prescripciones | `/prescriptions` |
| Vacunas | `/vaccines` |
| Hospitalización | `/hospital` |
| Inventario | `/inventory` |
| Facturación | `/billing` |
| Roles y permisos | `/roles` |
| Estadísticas | `/stats` |
| Búsqueda | `/search` |

Documentación interactiva completa en **`/docs`** (Swagger) o **`/redoc`**.

---

## Estructura del proyecto

```
veterinary-medicine-back/
├── main.py                         # Entrada de la aplicación
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env                            # Variables de entorno (no subir a git)
├── alembic/                        # Configuración de migraciones
├── migrations/                     # Migraciones de base de datos
└── app/
    ├── domain/
    │   ├── entities/               # Modelos de dominio (Pet, User, etc.)
    │   └── ports/                  # Interfaces de repositorios
    ├── application/
    │   └── services/               # Casos de uso / lógica de negocio
    └── infrastructure/
        └── adapters/
            ├── api/                # Rutas FastAPI + schemas Pydantic
            └── db/                 # Modelos SQLAlchemy + repositorios
```

---

## Autenticación

La API usa **JWT Bearer tokens**.

1. Hacer POST a `/users/login` con `username` y `password`
2. Guardar el `access_token` recibido
3. Incluirlo en cada request: `Authorization: Bearer <token>`

Los tokens expiran en **24 horas**.

---

## Archivos subidos

Las fotos de mascotas y adjuntos médicos se guardan en la carpeta `uploads/` y se sirven estáticamente en `/uploads/<archivo>`.

