"""
Este archivo contiene una aplicación FastAPI que ejecuta un spider de Scrapy.
author: Miguel Herize
mail: migherize@gmail.com
"""

import os
import subprocess
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home_page():
    """Página de inicio de la aplicación."""
    return {"page": "home"}


@app.get("/spider-crawl")
def crawler():
    """
    Ejecuta un spider de Scrapy en el directorio del proyecto.
    """
    project_path = os.path.join(os.getcwd(), "turismo_madrid")
    spider_args = ["scrapy", "crawl", "turismo_madrid_spider"]

    os.chdir(project_path)

    subprocess.run(spider_args, check=True)
    os.chdir(os.getcwd())
    return {"message": "Spider ejecutado exitosamente"}


@app.get("/Get-RutasMadrid")
def get_all():
    return {"message": "Spider ejecutado exitosamente"}
