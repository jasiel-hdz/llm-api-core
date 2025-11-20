# Estructura del Proyecto LLM API Core

## Descripción General
Proyecto FastAPI escalable para un servicio de LLM (Large Language Model) con arquitectura modular y separación de responsabilidades.

## Estructura de Directorios

```
llm-api-core/
├── app.py                 # Punto de entrada principal de FastAPI
├── config.py              # Configuración de la aplicación (Settings con Pydantic)
├── database.py            # Configuración de SQLAlchemy y conexión a PostgreSQL
├── dependencies.py        # Dependencias compartidas (get_db, get_current_user, JWT)
├── requirements.txt       # Dependencias de Python
├── Dockerfile             # Configuración de Docker
├── docker-compose.yml     # Orquestación de contenedores
├── local.yml              # Configuración local (probablemente Ansible)
├── .dockerignore          # Archivos excluidos del build de Docker
│
├── core/                  # Módulos principales de la aplicación (estructura esperada)
│   ├── user/              # Módulo de usuarios
│   │   ├── models.py      # Modelos SQLAlchemy de User
│   │   ├── routes.py      # Rutas de API para usuarios
│   │   ├── schema.py      # Schemas Pydantic para validación
│   │   └── bearer.py      # JWTBearer para autenticación
│   │
│   └── post/              # Módulo de posts
│       ├── models.py      # Modelos SQLAlchemy de Post
│       ├── routes.py      # Rutas de API para posts
│       ├── schema.py      # Schemas Pydantic
│       └── dependency.py  # Dependencias específicas del módulo
│
└── test/                  # Módulos de prueba/desarrollo
    └── llm/               # Módulo LLM en desarrollo
        ├── __init__.py
        ├── models.py      # Modelo Message (tabla "posts")
        ├── routes.py      # Rutas POST para LLM
        ├── schema.py      # Schema Message (Pydantic)
        └── dependency.py  # Dependencias específicas del módulo LLM
```

## Arquitectura y Patrones

### Patrón de Organización
- **Modular**: Cada funcionalidad está en su propio módulo dentro de `core/`
- **Separación de capas**: Models (DB), Schemas (validación), Routes (API), Dependencies (lógica compartida)
- **Dependency Injection**: Uso extensivo de `Depends()` de FastAPI

### Componentes Principales

#### 1. `app.py`
- Inicializa la aplicación FastAPI
- Registra routers de módulos (`user_router`, `post_router`)
- Crea tablas de base de datos al iniciar

#### 2. `config.py`
- Usa `pydantic_settings` para gestión de configuración
- Soporta múltiples entornos (dev/prod) mediante `APP_ENV`
- Carga variables desde `.env` o `.env.prod`
- Usa `@lru_cache` para singleton de Settings

#### 3. `database.py`
- Configuración de SQLAlchemy
- Crea engine de PostgreSQL usando credenciales de Settings
- Define `sessionLocal` para sesiones de DB
- `Base` para modelos declarativos

#### 4. `dependencies.py`
- `get_db()`: Dependency para obtener sesión de DB (context manager)
- `get_current_user()`: Dependency para autenticación JWT
- Valida tokens usando `JWTBearer` y `SECRET_KEY`

### Módulo LLM (test/llm/)

#### Modelo (`models.py`)
```python
class Message(Base):
    __tablename__ = "posts"
    - id: UUID (primary key)
    - title: String
    - content: String
    - author_id: UUID (FK a users.id)
    - author: relationship con User
```

#### Schema (`schema.py`)
```python
class Message(BaseModel):
    - message: str
```

#### Routes (`routes.py`)
- Endpoint: `POST /post`
- Recibe: `Message` (schema)
- Dependencias: `get_db`, `get_current_user`
- Crea post en DB y retorna datos

#### Dependency (`dependency.py`)
- `get_post_for_user()`: Valida que el post pertenezca al usuario autenticado

## Stack Tecnológico

- **Framework**: FastAPI 0.121.2
- **Base de Datos**: PostgreSQL (psycopg2-binary 2.9.6)
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Autenticación**: JWT (JSON Web Tokens)
- **Contenedores**: Docker + Docker Compose
- **Python**: 3.10

## Flujo de Datos

1. **Request** → FastAPI recibe petición HTTP
2. **Autenticación** → `JWTBearer` valida token
3. **Usuario** → `get_current_user` obtiene usuario de DB
4. **Validación** → Pydantic schema valida datos de entrada
5. **Base de Datos** → `get_db` proporciona sesión SQLAlchemy
6. **Lógica de Negocio** → Route handler procesa request
7. **Response** → Retorna JSON con datos

## Convenciones de Código

- **Routers**: Cada módulo tiene su router (`*_router`)
- **Prefijos**: Routers se registran con prefijos (`/user`, `/post`)
- **Tags**: Cada router tiene tags para documentación Swagger
- **Dependencies**: Lógica compartida en `dependencies.py`, específica en `dependency.py` del módulo
- **Models**: Nombres en singular (User, Post, Message)
- **Schemas**: Nombres descriptivos (CreateUpdatePost, Message)

## Estado Actual

- ✅ Estructura base configurada
- ✅ Sistema de autenticación JWT
- ✅ Configuración multi-entorno
- ✅ Módulo LLM en desarrollo (`test/llm/`)
- ⚠️ Referencias a `core/user` y `core/post` en código pero directorios no presentes
- ⚠️ Algunas importaciones pueden necesitar ajustes

## Próximos Pasos Sugeridos

1. Migrar módulo `test/llm/` a `core/llm/` cuando esté listo
2. Crear estructura completa de `core/user/` y `core/post/` si se necesitan
3. Agregar migraciones de DB (Alembic)
4. Implementar logging estructurado
5. Agregar tests unitarios e integración
6. Documentación API con OpenAPI/Swagger mejorada



