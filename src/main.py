"""
Este archivo contiene una aplicación FastAPI que ejecuta un spider de Scrapy.
author: Miguel Herize
mail: migherize@gmail.com
"""

import os
import subprocess
from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI(
    title="API de Turismo Madrid",
    version="1.0",
    description="Esta API proporciona información turística de la ciudad de Madrid.",
)

client = MongoClient("mongodb://admin:password@mongodb:27017/")
db = client["RutasMadrid"]


@app.get("/")
def home_page():
    """Página de inicio de la aplicación."""
    return {"page": "home"}


@app.get("/spider-crawl")
def crawler():
    """
    Ejecuta un spider de Scrapy en el directorio del proyecto.

    Returns:
        dict: Un diccionario con el mensaje de éxito al ejecutar el spider.

    Raises:
        subprocess.CalledProcessError: Si el proceso del spider no se pudo ejecutar correctamente.
    """
    project_path = os.path.join(os.getcwd(), "turismo_madrid")
    spider_args = ["scrapy", "crawl", "turismo_madrid_spider"]

    current_dir = os.getcwd()

    os.chdir(project_path)

    subprocess.run(spider_args, check=True)

    os.chdir(current_dir)
    return {"message": "Spider ejecutado exitosamente"}


@app.get("/Get-RutasMadrid")
def get_all():
    """Obtiene todas las rutas de Madrid almacenadas en MongoDB.

    Returns:
        list: Una lista de diccionarios que contienen la información de todas las rutas de Madrid en MongoDB.

    Raises:
        HTTPException: Si no se pudieron obtener las rutas de MongoDB.
    """
    list_result = []
    resultados = db["router"].find()
    for resultado in resultados:
        if "list_stage_ids" in resultado:
            lista_id_etapas = resultado["list_stage_ids"]
            etapas = db["stages"].find({"_id": {"$in": lista_id_etapas}})
            resultado["list_stage_ids"] = [etapa for etapa in etapas]
            for resultado2 in resultado["list_stage_ids"]:
                if "info_itinerarios" in resultado2:
                    lista_id_itinerarys = resultado2["info_itinerarios"]
                    itinerarys = db["itinerary"].find(
                        {"_id": {"$in": lista_id_itinerarys}}
                    )
                    resultado2["info_itinerarios"] = [
                        itinerary for itinerary in itinerarys
                    ]
                    continue

                else:
                    continue
        else:
            continue

        list_result.append(resultado)

    print(len(list_result))

    def change_type(data: dict):
        aux_data = data.copy()
        for key, value in aux_data.items():
            if isinstance(value, dict):
                aux_data[key] = change_type(value)
                continue
            aux_data[key] = str(value)
        return aux_data

    for index, d in enumerate(list_result):
        list_result[index] = change_type(d)

    return list_result
