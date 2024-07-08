import re
import os

# Django Built-in modules
from django.core.management.base import BaseCommand

# Third Party Apps
from tqdm import tqdm


class Command(BaseCommand):
    help = "Minify html templates to reduce the size"

    def handle(self, *args, **kwargs):
        try:
            files = self.get_html_files(".")
            for file in tqdm(files):
                self.minify_file(file)
            self.stdout.write(f"{len(files)} files are minified!\r\n")

        except Exception as e:
            self.stdout.write(f"Something went wrong!\r\n{e}")

    def get_html_files(self, directory):
        """Gets all HTML files in a directory, including subdirectories."""
        files = []
        excluded_dirs = ['.git', 'venv', '.idea', 'migrations', 'locale', 'media', 'static', '__pycache__', 'menu']
        for dirpath, dirnames, filenames in os.walk(directory):
            if any(excluded_dir in dirpath for excluded_dir in excluded_dirs):
                continue

            for filename in filenames:
                if filename.endswith(".html"):
                    files.append(os.path.join(dirpath, filename))
        return files

    def strip_spaces_in_template(self, template_source):
        """
        Default function used to preprocess templates.

        To use Your own stripping function do not change this function, use
        **settings.TEMPLATE_MINIFIER_STRIP_FUNCTION property**!
        """
        # remove comments
        template_source = re.sub(r'{#.*#}', '', template_source)

        # strip whitespace between html tags
        template_source = re.sub(r'>\s+<', '><', template_source, flags=re.MULTILINE)

        # strip whitespace around django variables
        template_source = re.sub(r'>\s+{{', '>{{', template_source, flags=re.MULTILINE)
        template_source = re.sub(r'}}\s+<', '}}<', template_source, flags=re.MULTILINE)

        # strip whitespace around django and html tags
        template_source = re.sub(r'>\s+{%', '>{%', template_source, flags=re.MULTILINE)
        template_source = re.sub(r'%}\s+<', '%}<', template_source, flags=re.MULTILINE)

        # strip whitespace between django tags
        template_source = re.sub(r'%}\s+{%', '%}{%', template_source, flags=re.MULTILINE)

        # strip whitespace between django tags and variables
        # template_source = re.sub(r'%}\s+{{', '%}{{', template_source, flags=re.MULTILINE)
        # template_source = re.sub(r'}}\s+{%', '}}{%', template_source, flags=re.MULTILINE)

        # condense any white space
        template_source = re.sub(r'\s{2,}', ' ', template_source, flags=re.MULTILINE)

        # strip leading and trailing html
        template_source = template_source.strip()

        return template_source

    def minify_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            template_content = file.read()

        modified_content = self.strip_spaces_in_template(template_content)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
