# Py-Scraper
[![Banner](https://i.ibb.co/prMHs9C/py-scraper.png)](https://i.ibb.co/prMHs9C/py-scraper.png)

---

## Overview

`py-scraper` is a scholar project designed to scrape e-commerce sites in search of offers. With the vastness and complexity of online shopping platforms, this tool aims to make it simpler for users to find the best deals without going through the tedious process of visiting multiple websites.

---

## Features

- **Multiple E-commerce Support**: Easily search across multiple e-commerce platforms with a single query.
- **Real-time Results**: Get the latest offers as they appear on the platforms.

---

## Installation and Usage

*Here, you can provide instructions on how to install and use your tool. For example:*

1. Clone the repository:
   
   ```bash
   git clone https://github.com/your-username/py-scraper.git
   cd py-scraper
   ```
2. Setup Docker Networks
   
    ```docker network create backend```

    ```docker network create flaskapp```

3. Run the application using Docker Compose
   
    ```docker-compose up```

_Note: If you're running Docker for the first time, it might take a while as Docker downloads the required images._

## Supported E-commerce Platforms

1. Mercado Libre Mexico
2. Walmart Mexico
   
...and more coming soon!

## API DOCUMENTATION
### Endpoint: `/search`

**Description:** This endpoint allows you to search for Lenovo tablets within a specified price range across two domains: "meli" and "wm."

**Request:**

- Method: POST
- URL: http://localhost:5000/search
- Headers:
  - Content-Type: application/json
- Body (JSON):

```json
{
  "prompt": "Lenovo Tablet",
  "domains": ["meli", "wm"],
  "price_range": [0, 3000]
}
```
**Response:**

- Content-Type: application/json


**Response Example**
```json
[
    {
        "image": "https://http2.mlstatic.com/D_NQ_NP_602028-MLA44170637858_112020-V.webp",
        "link": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-e7-tb-7104f-7-8gb-negra-y-1gb-de-memoria-ram/p/MLM13635241?pdp_filters=category:MLM82070#searchVariation=MLM13635241&position=4&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5",
        "price": 1690,
        "product": "Tablet Lenovo Tab E7 TB-7104F 7\" 8GB negra y 1GB de memoria RAM",
        "source": "meli"
    },
    {
        "image": "https://http2.mlstatic.com/D_NQ_NP_895449-MLA52471823672_112022-V.webp",
        "link": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-m7-3rd-gen-tb-7306f-7-32gb-iron-gray-y-2gb-de-memoria-ram/p/MLM19858651?pdp_filters=category:MLM82070#searchVariation=MLM19858651&position=12&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5",
        "price": 1715,
        "product": "Tablet Lenovo Tab M7 3rd Gen TB-7306F 7\" 32GB iron gray y 2GB de memoria RAM",
        "source": "meli"
    },
    {
        "image": "https://http2.mlstatic.com/D_NQ_NP_788683-MLA47931054574_102021-V.webp",
        "link": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-m10-hd-2nd-gen-tb-x306f-101-32gb-iron-gray-y-2gb-de-memoria-ram/p/MLM18334221?pdp_filters=category:MLM82070#searchVariation=MLM18334221&position=13&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5",
        "price": 2434,
        "product": "Tablet Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM",
        "source": "meli"
    },
    //more results here
]
```
### Endpoint: `/product/specs`

**Description:** This endpoint allows you to retrieve product specifications and pricing information for given product URLs from different e-commerce domains.

**Request:**

- Method: GET
- URL: http://localhost:5000/product/specs
- Headers:
  - Content-Type: application/json
- Body (JSON):

```json
[
	{
		"ecommerce": "wm",
		"url": "https://www.walmart.com.mx/ip/tablets/tablet-lenovo-m10-4g-64g/00019637857793?from=/search"
	},
	{
		"ecommerce": "meli",
		"url": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-m10-hd-2nd-gen-tb-x306f-101-32gb-iron-gray-y-2gb-de-memoria-ram/p/MLM18334221?pdp_filters=category:MLM82070#searchVariation=MLM18334221&position=13&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5"
	}
]
```
**Response:**

- Content-Type: application/json

**Response Data Example:**
```json
[
	{
		"prices": {
			"actual_price": "$3,499.00",
			"original_price": "costaba $4,999.00"
		},
		"specs": {
			"ALTO": "0.85",
			"ANCHO": "23.98",
			"GRAFICOS": "Integrated ARM Mali-G52 3EE 2-Core™",
			"LEYENDAS_PROTECCION_ ADV": "No exponer el producto al fuego ó agua",
			"MEM_OPTANE": "No",
			"CONTENIDO": "1 Tableta, 1 Cable corriente y 1 manual de usuario",
			"FONDO": "15.86",
			"PESO": "0.46",
			"CAPACIDAD MEMORIA RAM": "4 GB",
			"Bluetooth": "Sí",
			"Garantía": "Sólo aplica para productos vendidos por Walmart/Bodega Aurrera: 1 año directo con el proveedor. Consulta las condiciones de garantía de otros vendedores en la sección correspondiente.",
			"Color Principal": "Storm Grey",
			"REACONDICIONADO": "No",
			"Gen_Procesador": "GEN 3a",
			"PUERTOS": "1 USB-C 2.0, 1 Micro SD, 1 Plug, 1 Jack 3.5",
			"EAN_BA": "196378577937",
			"CAMARA": "5 MP",
			"RESOLUCION": "1920 x 1200",
			"Unidad Lectora de Discos": "No",
			"DURACION_DE_BATERIA": "8 h",
			"PANEL": "LED",
			"BATERIA": "Ion de Litio",
			"SISTEMAOPERATIVO": "Android",
			"MODELO": "ZAAE0034MX",
			"Wi-Fi": "Sí",
			"Camara_Secundaria": "8 MP",
			"Pantalla_Tactil": "Sí",
			"Memoria_Interna": "64 GB",
			"Memoria_Expandible": "128 GB",
			"TAMAÑO_DE_PANTALLA": "10.1 Pulgadas",
			"País": "China",
			"Alimentación_de_corriente": "Continua",
			"Gama Color": "Gris"
		},
		"store": "Walmart",
		"title": "Tablet Lenovo M10 4G 64G",
		"url": "https://www.walmart.com.mx/ip/tablets/tablet-lenovo-m10-4g-64g/00019637857793?from=/search"
	},
	{
		"prices": {
			"actual_price": "2,434",
			"original_price": null
		},
		"specs": [
			{
				"spec_group_1": {
					"": null,
					"Color": "5",
					"Con control parental": null,
					"Con red móvil": "No",
					"Conectividad": "",
					"Es Dual SIM": null,
					"Lectores de tarjetas SIM": null,
					"Modelo alfanumérico": "Sí",
					"Opiniones": "No",
					"Precio": "Wi-Fi, Wi-Fi Direct, Bluetooth, USB micro-C, Wi-Fi Display, Pogo pin, OTG",
					"Tablet  Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM(Este producto)": "(807)",
					"Tablet  Samsung Galaxy Tab A A7 Lite SM-T220 8.7\" 32GB gris y 3GB de memoria RAMVer producto": "TB-X306F",
					"Tablet  Xiaomi Redmi Pad 10.61\" 128GB graphite gray y 4GB de memoria RAMVer producto": "Iron gray",
					"Tablet Lenovo Tab M10 3ra Gen 10.1'' 3gb Ram 32gb Android 11 Color Storm greyVer producto": "2434 pesos con 78 centavos$2,434.78",
					"Versión de Bluetooth": null
				}
			}
		],
		"store": "Mercado Libre",
		"title": "Tablet Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM",
"url": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-m10-hd-2nd-gen-tb-x306f-101-32gb-iron-gray-y-2gb-de-memoria-ram/p/MLM18334221?pdp_filters=category:MLM82070#searchVariation=MLM18334221&position=13&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5"
	}
]

```
### Endpoint: `/products/compare`

**Description:** This endpoint allows you to compare product specifications and pricing information between two different products.

**Request:**

- Method: POST
- URL: http://localhost:5000/products/compare
- Headers:
  - Content-Type: application/json
- Body (JSON):

```json
[
	{
		"prices": {
			"actual_price": "$3,499.00",
			"original_price": "costaba $4,999.00"
		},
		"specs": "{\"ALTO\": \"0.85\", \"ANCHO\": \"23.98\", \"GRAFICOS\": \"Integrated ARM Mali-G52 3EE 2-Core™\", \"LEYENDAS_PROTECCION_ ADV\": \"No exponer el producto al fuego ó agua\", \"MEM_OPTANE\": \"No\", \"CONTENIDO\": \"1 Tableta, 1 Cable corriente y 1 manual de usuario\", \"FONDO\": \"15.86\", \"PESO\": \"0.46\", \"CAPACIDAD MEMORIA RAM\": \"4 GB\", \"Bluetooth\": \"Sí\", \"Garantía\": \"Sólo aplica para productos vendidos por Walmart/Bodega Aurrera: 1 año directo con el proveedor. Consulta las condiciones de garantía de otros vendedores en la sección correspondiente.\", \"Color Principal\": \"Storm Grey\", \"REACONDICIONADO\": \"No\", \"Gen_Procesador\": \"GEN 3a\", \"PUERTOS\": \"1 USB-C 2.0, 1 Micro SD, 1 Plug, 1 Jack 3.5\", \"EAN_BA\": \"196378577937\", \"CAMARA\": \"5 MP\", \"RESOLUCION\": \"1920 x 1200\", \"Unidad Lectora de Discos\": \"No\", \"DURACION_DE_BATERIA\": \"8 h\", \"PANEL\": \"LED\", \"BATERIA\": \"Ion de Litio\", \"SISTEMAOPERATIVO\": \"Android\", \"MODELO\": \"ZAAE0034MX\", \"Wi-Fi\": \"Sí\", \"Camara_Secundaria\": \"8 MP\", \"Pantalla_Tactil\": \"Sí\", \"Memoria_Interna\": \"64 GB\", \"Memoria_Expandible\": \"128 GB\", \"TAMAÑO_DE_PANTALLA\": \"10.1 Pulgadas\", \"País\": \"China\", \"Alimentación_de_corriente\": \"Continua\", \"Gama Color\": \"Gris\"}",
		"store": "Walmart",
		"title": "Tablet Lenovo M10 4G 64G",
		"url": "https://www.walmart.com.mx/ip/tablets/tablet-lenovo-m10-4g-64g/00019637857793?from=/search"
	},
	{
		"prices": {
			"actual_price": "2,434",
			"original_price": null
		},
		"specs": [
			{
				"spec_group_1": {
					"": null,
					"Color": "5",
					"Con control parental": null,
					"Con red móvil": "No",
					"Conectividad": "",
					"Es Dual SIM": null,
					"Lectores de tarjetas SIM": null,
					"Modelo alfanumérico": "Sí",
					"Opiniones": "No",
					"Precio": "Wi-Fi, Wi-Fi Direct, Bluetooth, USB micro-C, Wi-Fi Display, Pogo pin, OTG",
					"Tablet  Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM(Este producto)": "(807)",
					"Tablet  Samsung Galaxy Tab A A7 Lite SM-T220 8.7\" 32GB gris y 3GB de memoria RAMVer producto": "TB-X306F",
					"Tablet  Xiaomi Redmi Pad 10.61\" 128GB graphite gray y 4GB de memoria RAMVer producto": "Iron gray",
					"Tablet Lenovo Tab M10 3ra Gen 10.1'\'''\'' 3gb Ram 32gb Android 11 Color Storm greyVer producto": "2434 pesos con 78 centavos$2,434.78",
					"Versión de Bluetooth": null
				}
			}
		],
		"store": "Mercado Libre",
		"title": "Tablet Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM",
		"url": "https://www.mercadolibre.com.mx/tablet-lenovo-tab-m10-hd-2nd-gen-tb-x306f-101-32gb-iron-gray-y-2gb-de-memoria-ram/p/MLM18334221?pdp_filters=category:MLM82070#searchVariation=MLM18334221&position=13&search_layout=stack&type=product&tracking_id=bb88560c-8604-466a-9951-dd739923fdc5"
	}
]
```
**Response:**

- Content-Type: application/json
**Response Data Example:**
```json
{
	"compare": "La Tablet Lenovo M10 4G 64G disponible en Walmart tiene un precio actual de $3,499.00, con un descuento notable de $1,500.00 sobre el precio original. Cuenta con una pantalla de 10.1 pulgadas y una resolución de 1920 x 1200. Viene con 4GB de memoria RAM y 64GB de almacenamiento interno, expandible hasta 128GB. Además, cuenta con una cámara principal de 5MP y una cámara secundaria de 8MP. La batería tiene una duración de hasta 8 horas. También incluye conectividad Wi-Fi y Bluetooth. Por otro lado, la Tablet Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM, disponible en Mercado Libre, tiene un precio de $2,434.78. Esta tablet cuenta con una pantalla de 10.1 pulgadas, 32GB de almacenamiento interno y 2GB de memoria RAM. Además, tiene conectividad Wi-Fi, Bluetooth y USB. La mejor opción en términos de precio y características sería la Tablet Lenovo Tab M10 HD 2nd Gen TB-X306F 10.1\" 32GB iron gray y 2GB de memoria RAM disponible en Mercado Libre, ya que ofrece un precio más económico y características similares a la Tablet Lenovo M10 4G 64G de Walmart.",
	"product": null
}
```

Currently the product comparison does not provides the product object that is selected as the best option


## Contributions
While this is a scholar project, contributions and feedback are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License.

## Do you like this project?

Let's drink a coffe together!

<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="devmanu" data-color="#FFDD00" data-emoji="☕"  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>
