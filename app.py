from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

@app.route('/')

def home():
    joke = get_random_chuck_norris_joke()
    color = get_random_color()
    return render_template_string(html_template, joke=joke, color=color)

def get_random_color():
    lambda_url = os.environ.get('RANDOM_COLOR_LAMBDA_URL')
    if not lambda_url:
        return "#000000" # Default to black if the URL is not set
    try:
        response = requests.get(lambda_url)
        if response.status_code == 200:
            color_data = response.json()
            return color_data.get('color', "#000000") # Return the color value or default to black
        else:
            print(f"Failed to retrieve color. Status code: {response.status_code}")
            return "#000000" # Default to black on error
    except Exception as e:
        print(f"An error occurred while fetching color: {e}")
        return "#000000" # Default to black on exception

def get_random_chuck_norris_joke():
    url = "https://api.chucknorris.io/jokes/random?category=sports"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            joke_data = response.json()
            return joke_data['value']
        else:
            return "Failed to retrieve joke."
    except Exception as e:
        return f"An error occurred: {e}"

# Simple HTML Template

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chuck Norris Jokes</title>
</head>
<body>
<h1>Random Chuck Norris Joke</h1>
<p style="color: {{ color }};">{{ joke }}</p>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)

