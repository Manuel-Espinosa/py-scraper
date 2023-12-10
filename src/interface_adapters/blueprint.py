from quart import Blueprint, request, jsonify
from usecases.search_products import search_in_multiple_domains
from usecases.use_browser import use_browser
from usecases.use_openai import use_openai

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
async def index():
    return "Hello, Web Scraper!"

@main_blueprint.route('/health')
async def health_check():
    return "OK", 200

@main_blueprint.route('/search', methods=['POST'])
async def search():
    data = await request.get_json()
    prompt = data['prompt']
    domains_keywords = data['domains']
    price_range = data['price_range']
    products = await search_in_multiple_domains(prompt, domains_keywords, price_range)
    return jsonify(products)

@main_blueprint.route('/product/specs', methods=['POST'])
async def access_link():
    payload = await request.get_json()
    data = await use_browser(payload)
    return jsonify(data)

@main_blueprint.route('/products/compare', methods=['POST'])
async def compare_products():
    payload = await request.get_json()
    data = await use_openai(payload)
    return jsonify(data)
