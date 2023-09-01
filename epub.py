import zipfile
import os
from bs4 import BeautifulSoup
import cssutils

# Replace 'input.epub' with the path to your EPUB file
epub_file_path = r"C:\Users\pauleena phan\Downloads\PragmaticProgrammer.epub"

# Create a temporary directory to extract and modify the EPUB contents
temp_dir = 'temp_epub'
os.makedirs(temp_dir, exist_ok=True)

# Extract the EPUB contents to the temporary directory
with zipfile.ZipFile(epub_file_path, 'r') as epub_zip:
    epub_zip.extractall(temp_dir)

# Modify the HTML and CSS files
for root, _, files in os.walk(temp_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if file_path.endswith('.xhtml'):  # Modify HTML files
            with open(file_path, 'r', encoding='utf-8') as html_file:
                content = html_file.read()
                soup = BeautifulSoup(content, 'html.parser')

                # Modify the HTML content here using BeautifulSoup methods
                # Example: Change text color to pink for all <p> elements
                for paragraph in soup.find_all('p'):
                    paragraph['style'] = 'color: yellow;'

                # Save the modified HTML back
                with open(file_path, 'w', encoding='utf-8') as modified_html_file:
                    modified_html_file.write(str(soup))

        elif file_path.endswith('.css'):  # Modify CSS files
            with open(file_path, 'r', encoding='utf-8') as css_file:
                css_content = css_file.read()
                stylesheet = cssutils.CSSParser().parseString(css_content)

                # Modify background color rules
                for rule in stylesheet:
                    # Example: Change the background color to red for all 'body' elements
                    if 'body' in rule.selectorText:
                        rule.style['background-color'] = 'red'

                # Save the modified CSS back
                with open(file_path, 'w', encoding='utf-8') as modified_css_file:
                    modified_css_file.write(stylesheet.cssText.decode('utf-8'))

# Re-zip the modified contents back to the EPUB file
modified_epub_path = 'modified.epub'
with zipfile.ZipFile(modified_epub_path, 'w') as new_epub:
    for root, _, files in os.walk(temp_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, temp_dir)
            new_epub.write(file_path, rel_path)

# Clean up temporary directory
for root, dirs, files in os.walk(temp_dir, topdown=False):
    for file in files:
        os.remove(os.path.join(root, file))
    for directory in dirs:
        os.rmdir(os.path.join(root, directory))
os.rmdir(temp_dir)



print("Modifications applied. Modified EPUB saved as 'modified.epub'")
