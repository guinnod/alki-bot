import requests


def get_colors(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        colors = response.json()
        return colors
    except requests.RequestException as e:
        return []


def get_sizes(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        sizes = response.json()
        return sizes
    except requests.RequestException as e:
        return []


def get_order_number(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        order_number = response.json()
        return order_number
    except requests.RequestException as e:
        return None


def get_order_status(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        order_status = response.json()
        return order_status
    except requests.RequestException as e:
        return None
