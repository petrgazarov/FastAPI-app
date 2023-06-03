from fastapi import FastAPI
from app import subapps

app = FastAPI(title="Glaza API")


# cdn.glaza.io for script file
app.mount("/client", subapps.client_app)  # app.glaza.io/client
app.mount("/api", subapps.web_app)  # app.glaza.io/api
app.mount("/internal", subapps.internal_app)  # app.glaza.io/internal
