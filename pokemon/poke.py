from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_pokemon', methods=['POST'])
def get_pokemon():
    pokemon_id = request.form.get('id')
    if not pokemon_id:
       return jsonify({"error": "No ID provided"}), 400

    pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    pokemon_form_url = f'https://pokeapi.co/api/v2/pokemon-form/{pokemon_id}/'

    pokemon_response = requests.get(pokemon_url)
    pokemon_form_response = requests.get(pokemon_form_url)

    if pokemon_response.status_code != 200 or pokemon_form_response.status_code != 200:
        return jsonify({"error": "Failed to fetch data"}), 500

    pokemon_data = pokemon_response.json()
    pokemon_form_data = pokemon_form_response.json()

    stats = []
    for stat in pokemon_data['stats']:
        stats.append({
            "base_stat": stat['base_stat'],
            "effort": stat['effort'],
            "stat": {
                "name": stat['stat']['name'],
                "url": stat['stat']['url']
            }
        })

    result = {
        "stats": stats,
        "name": pokemon_form_data['name'],
        "sprites": {
            "back_default": pokemon_form_data['sprites']['back_default'],
            "back_female": pokemon_form_data['sprites']['back_female'],
            "back_shiny": pokemon_form_data['sprites']['back_shiny'],
            "back_shiny_female": pokemon_form_data['sprites']['back_shiny_female'],
            "front_default": pokemon_form_data['sprites']['front_default'],
            "front_female": pokemon_form_data['sprites']['front_female'],
            "front_shiny": pokemon_form_data['sprites']['front_shiny'],
            "front_shiny_female": pokemon_form_data['sprites']['front_shiny_female']
        }
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
