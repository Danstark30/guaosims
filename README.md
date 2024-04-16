# UAO SIMS

Laboratorio de bioinstrumentación del grupo de ingeniería biomédica de la Universidad Autónoma de Occidente


## Correr localmente

Clonar el proyecto

```bash
  git@github.com:bimbau/bimbau_admin.git
```

### Opción Docker :whale2:

Construir imágen de Docker

```bash
  sudo docker build -t uaosims-local .
```

Correr imágen
```bash
  sudo docker run -dp 8000:8000 uaosims-local
```
### Opción Python 3.* :snake:

Instalar dependencias de python
```bash
  pip install -r requirements.txt
```

Recopilar archivos estáticos
```bash
  python manage.py collectstatic --clear --noinput
```

Correr proyecto
```bash
  python manage.py runserver
```
