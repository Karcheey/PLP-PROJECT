import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract filename from URL, or generate one if not available."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:  # if empty, generate a default one
        filename = "downloaded_image.jpg"
    return filename

def is_duplicate(filepath, content):
    """Check if the file already exists and has the same content."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            existing_hash = hashlib.md5(f.read()).hexdigest()
        new_hash = hashlib.md5(content).hexdigest()
        return existing_hash == new_hash
    return False

def fetch_image(url):
    try:
        # Create directory if it doesn't exist
        os.makedirs("Fetched_Images", exist_ok=True)

        # Fetch the image
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for bad status codes

        # Check Content-Type header to ensure it’s an image
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ The URL does not point to an image. Content-Type: {content_type}")
            return

        # Extract filename or generate one
        filename = get_filename_from_url(url)
        filepath = os.path.join("Fetched_Images", filename)

        # Check for duplicates before saving
        if is_duplicate(filepath, response.content):
            print(f"⚠ Duplicate detected: {filename} already exists with same content.")
            return

        # Save the image
        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Allow multiple URLs (comma-separated)
    urls = input("Please enter one or more image URLs (comma-separated): ")
    urls = [url.strip() for url in urls.split(",") if url.strip()]

    for url in urls:
        fetch_image(url)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
