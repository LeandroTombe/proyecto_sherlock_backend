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

---


### 5. iniciar el servidor

```bash
python main.py
```

¡Listo! Ahora puedes comenzar a trabajar en tu proyecto dentro de un entorno aislado.