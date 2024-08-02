import sys
from PIL import Image
import numpy as np

def load_image(image_path):
    try:
        return Image.open(image_path).convert('RGB')
    except IOError:
        print(f"Error: Unable to open image file '{image_path}'")
        sys.exit(1)

def save_image(image_array, path):
    try:
        Image.fromarray(image_array.astype(np.uint8), 'RGB').save(path)
    except IOError:
        print(f"Error: Unable to save image to '{path}'")
        sys.exit(1)

def generate_random_matrix(shape, seed):
    np.random.seed(seed)
    return np.random.randint(0, 256, size=shape, dtype=np.uint8)

def encrypt_image(image_array, seed):
    random_matrix = generate_random_matrix(image_array.shape, seed)
    encrypted_image = (image_array.astype(np.int16) - random_matrix) % 256
    return encrypted_image.astype(np.uint8)

def decrypt_image(encrypted_image, seed):
    random_matrix = generate_random_matrix(encrypted_image.shape, seed)
    decrypted_image = (encrypted_image.astype(np.int16) + random_matrix) % 256
    return decrypted_image.astype(np.uint8)

def scale_image(image_array, original_max):
    return (image_array.astype(np.float32) / original_max * 255).astype(np.uint8)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_image> <-e/-d> [key]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    operation = sys.argv[2]
    
    try:
        key = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    except ValueError:
        print("Error: Key must be an integer")
        sys.exit(1)

    original_image = load_image(image_path)
    original_array = np.array(original_image)
    original_max = original_array.max()

    if operation == '-e':
        encrypted_image = encrypt_image(original_array, key)
        save_image(encrypted_image, image_path)
        print(f"Image encrypted and saved as '{image_path}'")
    elif operation == '-d':
        decrypted_image = decrypt_image(original_array, key)
        save_image(decrypted_image, image_path)
        print(f"Image decrypted and saved as '{image_path}'")
    else:
        print("Invalid operation. Use -e for encrypt or -d for decrypt.")
        sys.exit(1)

if __name__ == "__main__":
    main()