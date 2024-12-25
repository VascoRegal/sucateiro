
from config import Config
from paginator import URLPaginator, ButtonPaginator
from transformation import Transformations

from selenium import webdriver

from bs4 import BeautifulSoup

import sys
import time
import json

class Sucateiro:

    def __init__(self, input_file):
        self._config = Config(input_file)

        # Setup Paginator
        self._paginator = None
        paginator_conf = self._config.get_pagination()
        if paginator_conf:
            paginator_type = paginator_conf['navigation']
            if paginator_type == 'url':
                self._paginator = URLPaginator(
                    paginator_conf['max_pages'],
                    paginator_conf['url_template']
                )

            elif paginator_type == 'button':
                self._paginator = ButtonPaginator(
                    paginator_conf['max_pages'],
                    paginator_conf['selector']
                )

            else:
                print('>>> Paginator not Implemented.')
                exit(1)

        # Setup WebDriver
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        self._driver = webdriver.Chrome(options=options)

    def _run(self):
        output = None
        url = self._config.get_target_url()
        data = self._config.get_data()

        self._driver.get(url)

        for item in data:
            item_conf = data[item]

            while (True):
                soup = BeautifulSoup(self._driver.page_source, 'html.parser')
                if item == 'list':
                    if not output:
                        output = []
                    results = self._parse_list(item, item_conf, soup)
                    output.extend(results)
                else:
                    print(f">>> Data Type {item} not implemented.")
                    exit(1)
                
                if self._paginator == None or not self._paginator.has_more_pages():
                    break
                else:
                    self._paginator.next_page(self._driver)
        return output

    def _parse_list(self, item, item_conf, soup):
        result = []
        containers = soup.select(item_conf['container'])
        
        for container in containers:
            obj = {}
            for field in self._config.get_fields(item):
                obj[field['name']] = self._parse_field(field, container)
            result.append(obj)
        return result

    def _parse_field(self, field_conf, container):
        field = None
        element = container.select_one(field_conf['selector'])
        if not element:
            return field_conf['default'] if 'deault' in field_conf.keys() else None

        if field_conf.get('position') == 'next':
            element = element.next_sibling

        if field_conf['type'] == 'image':
            if not element.has_attr("src"):
                element = element.find("img")
            field = element["src"]
            return field

        field = element.text.strip()

        if field_conf.get('transform'):
            for transformation in field_conf['transform']:
                if transformation['operation'] == 'split':
                    field = Transformations.split_transformation(field, transformation)
                elif transformation['operation'] == 'splice':
                    field = Transformations.splice_transformation(field, transformation)
                elif transformation['operation'] == 'replace':
                    field = Transformations.replace_transformation(field, transformation)
                else:
                    print(f"Transformation {transformation['operation']} not supported.")
                    exit(1)
       
        if field_conf['type'] == "number":
            field = int(field)

        if field_conf['type'] == "float":
            field = float(field)

        return field

    def _dump(self, output):
        out_conf = self._config.get_output()
        if out_conf["format"] == "json":
            with open(out_conf["file"], "w") as f:
                json.dump(output, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    s = Sucateiro(sys.argv[1])
    output = s._run()
    s._dump(output)