import os
from tkinter import Tk, filedialog
from PIL import Image, ImageDraw, ImageFont

# Function to get the folder path from the user
def select_folder():
    root = Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title="Select a Folder with Images")
    return folder_path

# Function to add labels to the image
def add_labels_to_image(image_path, output_folder):
    # Open the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size

    # Load the default macOS font
    try:
        font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", int(height / 20))  # Scale font based on image height
        bold_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", int(height / 20))  # Bold font
    except IOError:
        font = ImageFont.load_default()
        bold_font = font

    # Define the labels
    top_left_label = ""
    top_right_label = ""
    bottom_center_label = "May contain CUI//SP-EXPT (ITAR/EAR)"

    # Define positions for the labels
    top_left_position = (10, 10)
    top_right_position = (width - 10 - draw.textbbox((0, 0), top_right_label, font=bold_font)[2], 10)
    bottom_center_position = (width // 2 - (draw.textbbox((0, 0), bottom_center_label, font=font)[2] // 2), height - int(height / 10))

    # Define the highlight colors (yellow for bottom label)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)

    # Draw the labels
    # Top left label (blue and bold)
    draw.text(top_left_position, top_left_label, fill=blue, font=bold_font)

    # Top right label (blue and bold)
    draw.text(top_right_position, top_right_label, fill=blue, font=bold_font)

    # Bottom center label (with yellow background and red text)
    bottom_label_width, bottom_label_height = draw.textbbox((0, 0), bottom_center_label, font=font)[2:4]
    draw.rectangle(
        [(bottom_center_position[0] - 10, bottom_center_position[1] - 5), 
         (bottom_center_position[0] + bottom_label_width + 10, bottom_center_position[1] + bottom_label_height + 5)],
        fill=yellow
    )
    draw.text(bottom_center_position, bottom_center_label, fill=red, font=font)

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save the modified image with a new name in the output folder
    output_image_path = os.path.join(output_folder, os.path.basename(image_path))
    img.save(output_image_path)

# Main function to process the folder
def process_images_in_folder():
    folder_path = select_folder()

    if not folder_path:
        print("No folder selected. Exiting.")
        return

    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not image_files:
        print("No images found in the folder. Exiting.")
        return

    # Create an output folder to save the modified images
    output_folder = os.path.join(folder_path, "modified_images")

    # Process each image
    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        add_labels_to_image(image_path, output_folder)
        print(f"Processed {image_file}")

if __name__ == "__main__":
    process_images_in_folder()