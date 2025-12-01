from flask import Blueprint, render_template
from flask import request
import requests
import os
#from dotenv import load_dotenv
#load_dotenv()

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def index():

    api_key = os.environ.get('UNSPLASH_KEY')

    # Handle missing API key
    if not api_key:
        return render_template('index.html', image_url=None, search_term='', error='API key not configured. Please set UNSPLASH_KEY environment variable.')

    default_query = 'motivation'
    search_term = default_query

    if request.method == 'POST':
        submitted_term = request.form.get('query', '').strip()
        if submitted_term:
            search_term = submitted_term

    api_url = f'https://api.unsplash.com/photos/random?query={search_term}&client_id={api_key}'
    api_response = requests.get(api_url)

    if api_response.status_code == 200:
        data = api_response.json()
        image_url = data['urls']['regular']
    else:
        image_url = None

    return render_template('index.html', image_url=image_url, search_term=search_term)



@main_blueprint.route('/conditional')
def conditional():
    user = 'admin'
    return render_template('conditional.html', user=user)


@main_blueprint.route('/loop')
def loop():
    users = ['admin', 'user', 'guest']
    return render_template('loop.html', items=users)


@main_blueprint.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f'Logged in as {username}'
    
    return render_template('form.html')