from frameworks.openai import compare_products

promts={
    'compare': "Compara objetivamente estos productos y entregame la mejor opcion segun su precio y caracteristicas en un parrafo e indica la tienda en donde se encuentra"
    }

def use_openai(products):
    compare = compare_products(products, promts["compare"])
    data={
        'compare':compare
    }
    return data
