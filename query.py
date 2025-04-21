import gdown
import os

file_url = "https://drive.google.com/uc?id=1BU9X7Ipxa4BjMNG5wRC53XcuspfxHnBf"

folder_name = "data"
os.makedirs(folder_name, exist_ok=True)
output_path = os.path.join(folder_name, "data.csv")
gdown.download(file_url, output_path, quiet=False)

print(f"Data saved to {output_path}")
