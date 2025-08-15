# Microservicio de Autenticación

Este es un microservicio de autenticación construido con Flask que maneja el registro, inicio de sesión y gestión de usuarios.

## Configuración del Entorno de Desarrollo

### Opción 1: Usar Docker (Recomendada)

```bash
# Clonar el repositorio
git clone <tu-repositorio>
cd authMicro

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus valores reales

# Ejecutar con Docker
docker-compose up --build
```

### Opción 2: Entorno local

#### 1. Instalar `virtualenv`
```bash
pip3 install virtualenv
```

#### 2. Crear un entorno virtual
```bash
virtualenv venv
```

#### 3. Activar el entorno virtual
- **En Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
- **En Unix o macOS:**
    ```bash
    source venv/bin/activate
    ```

#### 4. Instalar las dependencias del proyecto
```bash
pip install -r requirements.txt
```

## Configuración de la Base de Datos

### Variables de Entorno

#### Configuración inicial
1. **Copiar el archivo de ejemplo:**
```bash
cp .env.example .env
```

2. **Editar `.env` con tus valores reales:**
```bash
# Configuración de Flask
FLASK_APP=main.py
FLASK_ENV=development
FLASK_DEBUG=1

# Clave secreta para JWT (¡CAMBIA ESTA CLAVE!)
FLASK_JWT_SECRET_KEY=mi_clave_secreta_super_segura_123456789

# Base de datos local
DATABASE_URL=postgresql://postgres:tu_password@localhost:5432/auth_db_local

# Puerto de la aplicación
PORT=5000
```

#### ⚠️ IMPORTANTE
- **NO subir `.env` a GitHub** (ya está en `.gitignore`)
- **SÍ subir `.env.example`** para que otros desarrolladores sepan qué configurar
- Cambia `FLASK_JWT_SECRET_KEY` por una clave única y segura

### Migraciones de Base de Datos
El proyecto utiliza Flask-Migrate para manejar las migraciones de la base de datos. Los comandos principales son:

1. **Inicializar la base de datos** (solo la primera vez):
```bash
flask db init
```

2. **Crear una nueva migración** (cuando hagas cambios en los modelos):
```bash
flask db migrate -m "descripción del cambio"
```

3. **Aplicar las migraciones pendientes**:
```bash
flask db upgrade
```

4. **O ejecutar el script de migraciones automático**:
```bash
python migrations.py
```

## Endpoints Disponibles

### Autenticación
- `POST /auth/register` - Registro de nuevos usuarios
- `POST /auth/login` - Inicio de sesión
- `DELETE /auth/logout` - Cierre de sesión
- `GET /auth/refresh` - Renovar token de acceso
- `GET /auth/whoami` - Obtener información del usuario actual

### Usuarios
- `GET /users/all` - Listar todos los usuarios (requiere autenticación)

## Características de Seguridad

- Autenticación basada en JWT (JSON Web Tokens)
- Lista negra de tokens para logout seguro
- Contraseñas hasheadas
- Protección contra tokens expirados
- Manejo de sesiones con refresh tokens

## Estructura del Proyecto

```
.
├── main.py                 # Punto de entrada de la aplicación
├── .env.example           # Variables de entorno de ejemplo
├── .env                   # Variables de entorno reales (NO subir a GitHub)
├── docker-compose.yml     # Configuración de Docker
├── Dockerfile             # Imagen de Docker
├── requirements.txt       # Dependencias del proyecto
├── src/
│   ├── api/              # Rutas de la API
│   ├── config/           # Configuración y extensiones
│   ├── models/           # Modelos de base de datos
│   ├── repositories/     # Capa de acceso a datos
│   └── services/         # Lógica de negocio
├── migrations/            # Migraciones de base de datos
├── nginx/                 # Configuración de Nginx
└── tests/                 # Tests unitarios
```

## Ejecutar el Servidor

```bash
python main.py
```

El servidor se iniciará en `http://localhost:5000`

## Health Check

Para verificar el estado del servicio:
```bash
curl http://localhost:5000/health
```

## Notas Adicionales

- El servicio está configurado como un microservicio y puede ser containerizado con Docker
- Las migraciones de base de datos son automáticas y seguras
- Los tokens JWT tienen una expiración de 1 hora
- Se implementa una lista negra de tokens para manejar el logout de forma segura