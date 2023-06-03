from fastapi import FastAPI
from app import subapps

app = FastAPI(title="FastAPI App")


app.mount("/client", subapps.client_app)
app.mount("/api", subapps.web_app)
app.mount("/internal", subapps.internal_app)
