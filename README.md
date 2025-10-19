
# Micrositio Django de Dashboards + Notebooks

Proyecto mínimo listo para:
- Mostrar dashboards públicos
- Restringir dashboards privados a usuarios del grupo **Privados**
- Enlazar el `.ipynb` correspondiente (descarga)
- Cargar datos desde `data/dashboards.csv`
- Crear 3 usuarios preconfigurados desde `.env` (contraseñas ENCRIPTADAS con `set_password`)

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Pasos
```bash
# 1) Instalar dependencias
pip install -r requirements.txt

# 2) Migraciones
python manage.py migrate

# 3) Cargar usuarios, grupo y dashboards desde .env y CSV
python manage.py bootstrap

# 4) Levantar servidor
python manage.py runserver
```

Usuarios (definidos en `.env`):
- admin / Admin123* (superusuario)
- analista_privado / Privado123* (miembro del grupo Privados, ve privados)
- usuario_publico / Publico123* (solo públicos)

> Los notebooks buscados se ubican en `notebooks/<Área>/<Nombre>.ipynb`. Ya hay placeholders creados.

## Estructura
```
dashsite/         # Proyecto Django
dashboards/       # App
data/dashboards.csv
notebooks/Área/Nombre.ipynb
templates/
.env
```

## Notas
- Para producción, ajusta `ALLOWED_HOSTS` y `DEBUG=False` en `.env`.
- El iframe de Power BI usa la URL del CSV; algunos entornos requieren permitir orígenes.
