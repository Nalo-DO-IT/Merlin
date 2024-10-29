from flask import Blueprint, request, jsonify

sort_products_endpoint = Blueprint('sort_products_endpoint', __name__)

@sort_products_endpoint.route('/sort-products', methods=['POST'])
def sort_products():
    data = request.get_json()

    # Validación del payload vacío
    if not data:
        return jsonify({"error": "Payload vacío"}), 400

    sales_weight = data.get("salesWeight")
    stock_weight = data.get("stockWeight")

    # Verifica que productSales y productStock estén presentes
    product_sales = data.get("productSales")
    product_stock = data.get("productStock")

    if product_sales is None or product_stock is None:
        return jsonify({"error": "productSales y productStock son requeridos"}), 400

    # Crea diccionarios para ventas y stock
    product_sales_dict = {prod["productId"]: prod["sales"] for prod in product_sales}
    product_stock_dict = {prod["productId"]: prod["stock"] for prod in product_stock}

    # Verifica que los productos estén en ambas listas
    if not product_sales_dict.keys() & product_stock_dict.keys():
        return jsonify({"error": "No hay productos comunes en productSales y productStock"}), 400

    scores = {}
    for product_id in product_sales_dict.keys() & product_stock_dict.keys():
        sales_score = product_sales_dict[product_id] * sales_weight
        stock_score = product_stock_dict[product_id] * stock_weight
        scores[product_id] = sales_score + stock_score

    sorted_products = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    
    return jsonify(sorted_products)
