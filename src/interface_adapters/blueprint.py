from flask import Blueprint, request, jsonify
from usecases.search_products import search_in_multiple_domains
from usecases.use_browser import use_browser
from usecases.use_openai import use_openai

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

@main_blueprint.route('/product/specs', methods=['GET'])
def access_link():
    payload = request.json
    data=use_browser(payload)
    return jsonify(data)

@main_blueprint.route('/products/compare', methods=['POST'])
def compare_products():
    payload = request.json
    data = use_openai(payload)
    return jsonify(data)