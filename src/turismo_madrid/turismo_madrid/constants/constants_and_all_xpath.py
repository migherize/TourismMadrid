
path_output = ''
output_folder_name = 'raw_data'
output_filename_name = 'turismo_madrid.csv'
output_filename_refine_name = 'turismo_madrid_refine.csv'


xpath_url_routes = '//a[contains(@class, "enlace-ruta")]'
xpath_info_first_table = './div/div'

xpath_href = './@href' 
xpath_style = './@style'
xpath_header_2 = './/h2/text()'
xpath_paragraph = './/p/text()'

xpath_image = './/img/@src'

xpath_routs = "//div[contains(@class, 'datos-etapa')]//span//text()"
xpath_second_info = '//div[@class="item_fields"]/div'


field_name = [
    'page_first',
    'second_first'
]