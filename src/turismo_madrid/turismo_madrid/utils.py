import re


def extractor_info_with_regex(data: str, regex:str) -> str or None:

    aux_data, aux_regex = data, regex
    
    url_main_image = re.search(fr"{aux_regex}", aux_data.strip())
    if url_main_image:
        return url_main_image.group(1)
    return None
