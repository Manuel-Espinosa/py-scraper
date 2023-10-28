from frameworks.selenium import browser

def use_browser(payload):
    products_details = []
    for product in payload:
        detail =  browser(product["ecommerce"],product["url"])
        products_details.append(detail)

    return products_details