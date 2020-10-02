import requests
import json
import sys
import os

DB_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
TOKEN = os.environ.get('TOKEN')
API = os.environ.get('API', 'http://localhost:8000')

def main():
    with open('database.json') as input_file:
        database = json.load(input_file)
    mapped_database = []
    for entry in database:
        mapped_entry = {
            'name' : entry['name'],
            'config' : entry,
        }
        mapped_database.append(mapped_entry)
    response = requests.post(f'{API}/v1/klaro/services', json={
        'services' : mapped_database,
        }, headers={'Authorization': f'bearer {TOKEN}'})
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print(DB_DIR)
    if not TOKEN:
        sys.stderr.write("Please put the access token in the TOKEN environment variable.\n")
        exit(-1)
    main()