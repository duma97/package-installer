import eel
import json
from lunr import lunr  # Import the lunr library

eel.init('web')

all_packages = []
# Create a dictionary for quick lookups by package ID. This will be very fast.
packages_by_id = {}
search_index = None  # This will hold our search index.

try:
    with open('web/packages.json', 'r') as f:
        all_packages = json.load(f)
        # Populate the lookup dictionary using the package 'id' as the key.
        packages_by_id = {pkg['id']: pkg for pkg in all_packages}

    print(f"Loaded {len(all_packages)} packages. Building search index...")

    # Build the lunr index once at startup.
    # We define which fields to search ('name', 'description')
    # and which field is the unique reference ('id').
    search_index = lunr(
        ref='id',
        fields=('name', 'description'),
        documents=all_packages
    )
    print("Search index built successfully.")

except Exception as e:
    print(f"Error loading package database or building index: {e}")


@eel.expose
def search_packages(query):
    # If the search bar is empty, return all packages.
    if not query:
        return all_packages

    # If the index failed to build, fall back to the old, simple search.
    if not search_index:
        print("Warning: Search index not available. Using basic search.")
        query = query.lower()
        return [pkg for pkg in all_packages if query in pkg['name'].lower() or query in pkg['description'].lower()]

    try:
        # Use the lunr index to perform a search.
        # The wildcard `*` enables "search-as-you-type" functionality.
        # A tilde `~1` can be added to allow for one typo (e.g., `query~1`).
        search_results = search_index.search(f'{query}*')

        # The results from lunr are a list of dicts like {'ref': 'firefox', 'score': ...}.
        # We use our fast `packages_by_id` dictionary to get the full package details for each result.
        return [packages_by_id[result['ref']] for result in search_results]
    except Exception as e:
        print(f"Error during search: {e}")
        return []


if __name__ == "__main__":
    eel.start('index.html')
