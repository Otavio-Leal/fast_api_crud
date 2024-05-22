from fastapi import FastAPI
from src.routes.user import app as user_app

app = FastAPI()

# Inclua as rotas do arquivo user.py
app.mount("/user", user_app)
