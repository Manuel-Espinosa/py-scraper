from frameworks.openai import compare_products
from utils.get_product_in_compare import extract_product_from_compare_text

promts={
    'compare': "Compara objetivamente estos productos y entregame la mejor opcion segun su precio y caracteristicas en un parrafo e indica la tienda en donde se encuentra"
    }

def use_openai(products):
    compare = compare_products(products, promts["compare"])
    product = extract_product_from_compare_text(compare, products)
    data={
        'compare':compare,
        'product': product
    }
    return data
