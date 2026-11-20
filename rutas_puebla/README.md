# 🚌 Rutas Puebla — Gestión de Paradas de Transporte Público

Aplicación web interactiva y API REST desarrollada con **FastAPI**, **Redis Cloud** y **Leaflet.js** que permite administrar (crear, consultar, editar y eliminar) paradas de transporte público en la ciudad de Puebla y visualizarlas geográficamente en un mapa interactivo.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, FastAPI, Uvicorn
* **Base de Datos en Memoria / Cloud:** Redis Cloud (`redis-py`)
* **Validación de Esquemas:** Pydantic v2
* **Frontend & Mapas:** HTML5, CSS3, JavaScript (Vanilla Fetch API) y **Leaflet.js** (OpenStreetMap)

---

## 📂 Estructura del Proyecto

```text
rutas_puebla/
├── app/
│   ├── __init__.py       # Inicializador del paquete de aplicación
│   ├── database.py       # Conexión a Redis Cloud y prueba de estado (PING)
│   ├── main.py           # Configuración de FastAPI, CORS, estáticos y rutas raíz
│   ├── models.py         # Modelo Pydantic `Parada` con generación de ID y coordenadas
│   └── routes.py         # Endpoints REST CRUD (`/paradas`) sobre Redis
├── static/
│   ├── index.html        # Interfaz web principal (formulario, lista y mapa)
│   ├── app.js            # Lógica del cliente, peticiones Fetch y control de Leaflet
│   └── styles.css        # Estilos visuales de la interfaz
├── .env                  # Variables de entorno locales (no incluido en el repo)
├── requirements.txt      # Dependencias del proyecto
└── README.md             # Documentación del proyecto