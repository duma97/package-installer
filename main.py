import eel
import json

eel.init('web')

all_packages = []
try:
    with open('web/packages.json', 'r') as f:
        all_packages = json.load(f)
    print(f"Loaded {len(all_packages)} packages from the database.")
except Exception as e:
    print(f"Error loading package database: {e}")


@eel.expose
def search_packages(query):
    if not query:
        return all_packages

    query = query.lower()
    search_results = []
    for package in all_packages:
        if query in package['name'].lower() or query in package['description'].lower():
            search_results.append(package)

    return search_results


if __name__ == "__main__":
    eel.start('index.html')