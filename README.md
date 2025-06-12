# Microservicio de Autenticación

Este es un microservicio de autenticación construido con Flask que maneja el registro, inicio de sesión y gestión de usuarios.

## Configuración del Entorno de Desarrollo

Sigue estos pasos para preparar tu entorno de desarrollo de manera sencilla y ordenada:

### 1. Instalar `virtualenv`

```bash
pip3 install virtualenv
```

### 2. Crear un entorno virtual

```bash
virtualenv venv
```

### 3. Activar el entorno virtual

- **En Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
- **En Unix o macOS:**
    ```bash
    source venv/bin/activate
    ```

### 4. Instalar las dependencias del proyecto

```bash
pip install -r requirements.txt
```

## Configuración de la Base de Datos

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto con el siguiente contenido:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/tu_base_de_datos
FLASK_JWT_SECRET_KEY=tu-clave-secreta-aqui
FLASK_APP=main.py
FLASK_ENV=development
PORT=5000
```

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
├── main.py              # Punto de entrada de la aplicación
├── auth.py             # Rutas de autenticación
├── users.py            # Rutas de usuarios
├── models.py           # Modelos de base de datos
├── extensions.py       # Extensiones de Flask
├── jwt_handlers.py     # Manejadores de JWT
├── migrations.py       # Script de migraciones
└── requirements.txt    # Dependencias del proyecto
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