# COMO CORRER POR SI MUERO

## 1. Crear .venv

```
python -m venv .venv
```

## 2. Activar venv

Windows:
```
.\.venv\Scripts\activate
```

macOS:
```
source .venv/bin/activate
```

## 3. Instalar requerimientos

```
pip install -r requirements.txt
```

## 4. Cambiar Valores en `database.py` para usar tu MySQL

## 5. Crear `parkup_edge` en tu MySQL

## 6. Correr `configuration.py`

```
python configuration.py
```

## 7. Correr servidor (SOLO VA A FUNCIONAR ASÍ)

```
uvicorn main:app --host 0.0.0.0 --port 8000
```
