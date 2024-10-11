import os
from PIL import Image


def resize_image(input_path, output_path, size=(216, 216)):
    with Image.open(input_path) as img:
        # Resize the image
        img_resized = img.resize(size, Image.LANCZOS)

        # Convert the image to PNG format
        img_resized.save(output_path, format="PNG")
        print(f"Resized image saved to {output_path}")


def main():
    input_folder = "input_images"
    output_folder = "resized_images"

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all images in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"resized_{os.path.splitext(filename)[0]}.png")
            resize_image(input_path, output_path)


if __name__ == "__main__":
    main()