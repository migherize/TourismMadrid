from pymongo import MongoClient

MONGO_URL = "mongodb"

client = MongoClient("localhost", port=27019, username="admin", password="password")

db = client["prueba"]

col = db["personas"]

print(
    col.insert_one(
        {
            "route_name": "Nombre de la ruta",
            "title": "Titulo de la pagina de ruta",
            "distance": "70.7km",
            "time": "106h",
            "stages": 5,
            "description": "La descripcion de la ruta",
            "image": "url_imagen_ruta",
            "map_kmz": "url_map_kmz",
            "map_gpx": "url_map_gpx",
            "list_stages": [
                {
                    "state_name": "Alcalá de Henares",
                    "route_number": "RUTA 1",
                    "details": "Detalle de la ruta",
                    "itinerary": [
                        {
                            "route_relation": "RUTA 1 > ITINERARIO 1",
                            "itinerary_distance": "2.2Km",
                            "intinerary_name": "Alcalá Imprescindible paso a paso",
                            "itinerary_description": "La descripcion general del itinerario",
                            "places": [
                                {
                                    "place_name": "1. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "2. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "3. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                            ],
                        },
                        {
                            "route_relation": "RUTA 2 > ITINERARIO 2",
                            "itinerary_distance": "2.2Km",
                            "intinerary_name": "Alcalá Imprescindible paso a paso",
                            "itinerary_description": "La descripcion general del itinerario",
                            "places": [
                                {
                                    "place_name": "1. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "2. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "3. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                            ],
                        },
                    ],
                },
                {
                    "state_name": "Alcalá de Henares",
                    "route_number": "RUTA 1",
                    "details": "Detalle de la ruta",
                    "itinerary": [
                        {
                            "route_relation": "RUTA 1 > ITINERARIO 1",
                            "itinerary_distance": "2.2Km",
                            "intinerary_name": "Alcalá Imprescindible paso a paso",
                            "itinerary_description": "La descripcion general del itinerario",
                            "places": [
                                {
                                    "place_name": "1. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "2. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "3. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                            ],
                        },
                        {
                            "route_relation": "RUTA 2 > ITINERARIO 2",
                            "itinerary_distance": "2.2Km",
                            "intinerary_name": "Alcalá Imprescindible paso a paso",
                            "itinerary_description": "La descripcion general del itinerario",
                            "places": [
                                {
                                    "place_name": "1. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "2. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                                {
                                    "place_name": "3. Iglesia de Santa María la Mayor y Capilla de las Santas Formas",
                                    "place_description": "Descripcion del lugar",
                                    "place_img": "url_de_la_imagen_del_lugar",
                                    "more_info": "link_more_info",
                                },
                            ],
                        },
                    ],
                },
            ],
        }
    )
)
