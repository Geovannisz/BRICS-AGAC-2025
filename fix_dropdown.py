import os
from bs4 import BeautifulSoup

def get_html_files(root_dir):
    """Recursively finds all HTML files in a directory."""
    html_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".html"):
                html_files.append(os.path.join(root, file))
    return html_files

def fix_dropdown_in_file(filepath):
    """
    Corrects the HTML structure of dropdown menus by removing translation
    attributes from `<li>` elements, as they break functionality.
    """
    print(f"Checking/Fixing dropdown in: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    dropdown_items = soup.select('.dropdown-menu li')
    fixed_count = 0

    for li in dropdown_items:
        # Check if the incorrect attributes exist on the <li>
        if li.has_attr('data-lang-en') or li.has_attr('data-lang-pt'):
            del li['data-lang-en']
            del li['data-lang-pt']
            fixed_count += 1

            # Ensure the nested <a> tag has the attributes (it should already, but let's be safe)
            a_tag = li.find('a', class_='dropdown-item')
            if a_tag and not a_tag.has_attr('data-lang-en'):
                 original_text = a_tag.string.strip()
                 # This is just a fallback, the main translation script should handle this.
                 a_tag['data-lang-en'] = original_text
                 a_tag['data-lang-pt'] = original_text


    if fixed_count > 0:
        print(f"  Fixed {fixed_count} broken dropdown items.")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
    else:
        print("  No broken dropdown items found.")


if __name__ == "__main__":
    all_files = get_html_files('.')
    # Exclude the thank you page as it doesn't have the full navbar
    files_to_process = [f for f in all_files if 'thank-you.html' not in f]

    for file_path in files_to_process:
        fix_dropdown_in_file(file_path)

    print("\nDropdown fix script finished.")
