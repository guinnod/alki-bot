import requests


def get_colors_from_api(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        colors = response.json()  # Assuming the API returns a JSON array of colors
        print(colors)
        return colors
    except requests.RequestException as e:
        print(f"Error fetching colors from API: {e}")
        return []
