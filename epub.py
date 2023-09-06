import zipfile
from io import BytesIO
from PIL import Image, ImageOps
from bs4 import BeautifulSoup
import os

# Function to flip an image upside down
def flip_image(image):
    return ImageOps.flip(image)

# Function to remove src attributes from images within a specific class in an HTML file
def remove_src_attributes_from_class(html_content, class_name):
    soup = BeautifulSoup(html_content, 'html.parser')
    elements_to_remove = soup.find_all(class_=class_name)
    
    for element in elements_to_remove:
        # Find all <img> elements within the class and remove their src attribute
        for img_element in element.find_all('img'):
            img_element['src'] = ''
    
    return str(soup)

# Function to remove specified text from HTML
def remove_text_from_html(html_content, text_to_remove):
    soup = BeautifulSoup(html_content, 'html.parser')
    for element in soup.find_all(text=True):
        if text_to_remove in element:
            element.replace_with(element.replace(text_to_remove, ''))

    return str(soup)


# Function to create a new EPUB file with removed src attributes from images in the "calibre_6" class
def create_modified_epub(input_epub, output_epub):
    # Create a temporary directory to extract the EPUB content
    temp_dir = "temp_epub"
    os.makedirs(temp_dir, exist_ok=True)
    with zipfile.ZipFile(input_epub, 'r') as epub_file:
        epub_file.extractall(temp_dir)

    # Create a new EPUB file
    with zipfile.ZipFile(output_epub, 'w', zipfile.ZIP_DEFLATED) as new_epub_file:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as file:
                    content = file.read()
                
                if file_path.endswith(('.jpg', '.jpeg', '.png')):
                    image = Image.open(BytesIO(content))
                    flipped_image = flip_image(image)
                    flipped_image_bytes = BytesIO()
                    flipped_image.save(flipped_image_bytes, format=image.format)
                    content = flipped_image_bytes.getvalue()
                elif file_path.endswith('.html'):
                    # Remove specified text from HTML content
                    content = remove_text_from_html(content, "I l@ve RuBoard")  # Specify the text to remove

                arcname = os.path.relpath(file_path, temp_dir)
                new_epub_file.writestr(arcname, content)

if __name__ == "__main__":
    input_epub = "PragmaticProgrammer.epub"  # Replace with your input EPUB file
    output_epub = "output.epub"  # Replace with your desired output EPUB file

    create_modified_epub(input_epub, output_epub)
    print("Images flipped and text removed successfully in the EPUB!")
