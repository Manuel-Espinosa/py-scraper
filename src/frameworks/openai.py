import openai
import logging
import os
import json
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

def compare_products(products, question):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    products_str = [json.dumps(product) for product in products]
    products_str = ', '.join(products_str)
    prompt = f"Productos: {products_str} Accion: {question}"
    logging.info(f"promt: {prompt}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that compares products."},
            {"role": "user", "content": prompt}
        ],
    )

    answer = response['choices'][0]['message']['content'].strip()
    logging.info(f"answer: {answer}")

    return answer
