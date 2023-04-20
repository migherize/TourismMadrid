"""
funciones utils para la araña
author: Miguel Herize
mail: migherize@gmail.com
"""
import re


def extractor_info_with_regex(data: str, regex: str) -> str or None:
    """
    Función que busca una coincidencia con un patrón de expresión regular en una cadena de texto "data" utilizando el patrón "regex".

    Args:
        data (str): Cadena de texto en la que se realizará la búsqueda.
        regex (str): Patrón de expresión regular que se utilizará para la búsqueda.

    Returns:
        str or None: Si se encuentra una coincidencia, devuelve el primer grupo de captura (los elementos capturados
        entre paréntesis) como una cadena de texto. Si no se encuentra ninguna coincidencia, devuelve "None".
    """
    aux_data, aux_regex = data, regex

    url_main_image = re.search(rf"{aux_regex}", aux_data.strip())
    if url_main_image:
        return url_main_image.group(1)
    return None
