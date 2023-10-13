import os
import requests
import tarfile

# URL of the dataset
dataset_url = "http://image.ntua.gr/iva/datasets/flickr_logos/flickr_logos_27_dataset.tar.gz"

# Path to save the downloaded file
current_folder = os.path.abspath(os.path.dirname(__file__))
save_path = os.path.join(current_folder, "flickr_logos_27_dataset.tar.gz")

# Function to download the dataset
def download_dataset(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Dataset downloaded successfully: {save_path}")
    else:
        print("Failed to download the dataset. Please check the URL.")

# Function to extract the dataset
def extract_dataset(path, extract_to=current_folder):
    with tarfile.open(path, "r:gz") as tar:
        tar.extractall(path=extract_to)
        print(f"Dataset extracted successfully: {path}")
        
        # Get names of all items in the tar archive
        members = tar.getnames()
        
        # Check each item if it's a tar file
        for member in members:
            if member.endswith(('.tar.gz', '.tgz')):
                nested_tar_path = os.path.join(extract_to, member)
                extract_dataset(nested_tar_path, os.path.dirname(nested_tar_path))
                os.remove(nested_tar_path)  # remove the nested tar file after extraction

# Download the dataset
download_dataset(dataset_url, save_path)

# Extract the dataset
extract_dataset(save_path)
