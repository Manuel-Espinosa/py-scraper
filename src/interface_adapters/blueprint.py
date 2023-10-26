from flask import Blueprint, request, jsonify
from usecases.search_products import search_in_multiple_domains

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    return "Hello, Web Scraper!"

@main_blueprint.route('/search', methods=['POST'])
def search():
    data = request.json
    prompt = data['prompt']
    domains_keywords = data['domains']
    price_range = data['price_range']
    products = search_in_multiple_domains(prompt, domains_keywords, price_range)
    return jsonify(products)