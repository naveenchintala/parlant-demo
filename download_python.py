
import urllib.request
import json
import ssl
import sys
import os

# Allow unverified context just in case (for old python/certs)
ssl._create_default_https_context = ssl._create_unverified_context

url = "https://raw.githubusercontent.com/astral-sh/python-build-standalone/latest-release/latest-release.json"
print(f"Downloading {url}...")
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode())

# Find asset
target_arch = "aarch64-apple-darwin"
target_version = "3.11" # We want 3.11.x

found_url = None
# "assets" is a list. We iterate.
# Structure checking needed.
# Actually the schema might be complex, let's look for "assets" key.
# But often the JSON is a mapping or list of releases.
# Let's try to print keys if it fails.

# The JSON seems to be a huge list of assets directly or releases?
# Based on docs, it might be a mapping.
# Let's try to match strings.

from collections import deque
queue = deque([data])
best_asset = None

# We look for "browser_download_url" in a dict that also matches our criteria.
# But simpler: let's filter the assets list if "assets" exists.

# Actually, let's just use a specific known good tag/url if this is too complex for a one-shot script, 
# BUT the JSON approach is more robust.
# Let's assume 'releases' or flat list.

def find_url(obj):
    if isinstance(obj, list):
        for item in obj:
            res = find_url(item)
            if res: return res
    elif isinstance(obj, dict):
        if "url" in obj and "name" in obj:
            name = obj["name"]
            if target_arch in name and f"cpython-{target_version}" in name and "install_only" in name and not ".sha256" in name:
                return obj["url"]
        for k, v in obj.items():
            res = find_url(v)
            if res: return res
    return None

dl_url = find_url(data)

if not dl_url:
    print("Could not find suitable URL in JSON.")
    # Fallback to a hardcoded recent one if possible, or fail.
    # Fallback: 20240107 release
    dl_url = "https://github.com/indygreg/python-build-standalone/releases/download/20240107/cpython-3.11.7+20240107-aarch64-apple-darwin-install_only.tar.gz"
    print(f"Fallback to: {dl_url}")

print(f"Downloading Python from {dl_url}")
filename = "python_dist.tar.gz"
urllib.request.urlretrieve(dl_url, filename)
print("Download complete.")
