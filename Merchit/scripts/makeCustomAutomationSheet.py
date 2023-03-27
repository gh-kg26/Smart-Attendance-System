import re

def extract_values(input_string):
    # Define regular expressions to match the desired values
    size_regex = r'Choose Size:\s*(\w+)'
    color_regex = r'COLOUR:\s*(\w+)'
    preview_regex = r'_customily-preview:\s*(\S+)'
    production_regex = r'_customily-production-url:\s*(\S+)'

    # Extract the values using regular expressions
    size_match = re.search(size_regex, input_string)
    color_match = re.search(color_regex, input_string)
    preview_match = re.search(preview_regex, input_string)
    production_match = re.search(production_regex, input_string)

    # Create a list of the extracted values
    extracted_values = []
    if size_match:
        extracted_values.append(size_match.group(1))
    if color_match:
        extracted_values.append(color_match.group(1))
    if preview_match:
        extracted_values.append(preview_match.group(1))
    if production_match:
        extracted_values.append(production_match.group(1))
        
    # Print the extracted values
    print(extracted_values) 
    return extracted_values


input_string = '''Choose Size: Small
CHOOSE HOODIE COLOUR: BLACK
ADD PERSONALIZED CENTER TEXT: NO TEXT
_customily-thumb-id: _thumb-id-1675764452301
_customily-preview: https://cdn.customily.com/shopify/assetFiles/previews/merchit-official-merch.myshopify.com/ce896a79-6051-43f8-8f1c-bf3a84d9ee68.jpeg
_customily-thumb: https://cdn.customily.com/shopify/assetFiles/thumbs/merchit-official-merch.myshopify.com/ce896a79-6051-43f8-8f1c-bf3a84d9ee68.jpeg
_customily-customization-url: https://merchit.in/products/copy-of-customize-your-own-hoodie?variant=44757407334646&currency=INR&utm_medium=product_sync&utm_source=google&utm_content=sag_organic&utm_campaign=sag_organic&customizationId=9f0471ca-4f2b-4112-ad10-4d88b9f9f596
_customily-production-url: https://cdn.customily.com/ExportFile/merchit-official-merch/6318bfeb-304b-49a1-ac94-531ffa20bef1.png
_customily-personalization-id: _customily-id-3bdba2fa-39fd-487b-8ae3-a1ecece9c0fd
_Upload Image: https://cdn.customily.com/js-lib-temp-images/f3915aa5-e45f-4305-9446-be1e9093edc8/1-5d419368-7ba5-46ae-95b8-3ddf4725da24.png'''
extract_values(input_string)




    
    
     
