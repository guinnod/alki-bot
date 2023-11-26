import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")


def get_request(api_url):
    try:
        response = requests.get(f"{BACKEND_URL}{api_url}")
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(e)
        return None


def get_colors(product_id):
    data = get_request(f"?id={product_id}")
    if data:
        return {'colors': ['Red', 'White', 'Green'], 'price': 2390}
    return None


def get_sizes(product_id, color):
    data = get_request(f"?id={product_id}&color={color}")
    if data:
        return {'sizes': ['XS', 'S', 'M', 'L', 'XXL']}
    return None


def get_order_number(product_id, color, size, address, contacts):
    data = get_request(f"?id={product_id}&color={color}")
    if data:
        return {'order_id': '999'}
    return None


def get_order_status(order_id):
    data = get_request(f"?order_id={order_id}")
    if data:
        return f"Ваш заказ № {order_id} в ожидании оплаты. \nПродукт № product_id, размер: size, цвет: color,\nадрес доставки: address"
    return None
