import yaml
import json
import time
import re
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from exceptions import *

class Sucateiro:
    def __init__(self, config_file):
        self._config = self._load_config(config_file)
        self._output = None

    def _load_config(self, config_file):
        with open(config_file, 'r') as file:
            return yaml.safe_load(file)

    def _scrape(self):

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        output = None

        for target in self._config['targets']:
            url = target['url']
            data = target['data']
            driver.get(url)

            for item in data:
                item_config = data[item]

                # Parse data
                if item == 'list':
                    pagination = target['pagination'] if 'pagination' in target.keys() else None
                    next_page = True
                    max_pages = pagination['max_pages'] if pagination else 1
                    cur_page = 1
                    output = []
                    while (cur_page <= max_pages and next_page):
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        container = item_config['container']
                        containers = soup.select(container)
                        
                        for c in containers:
                            obj = {}
                            for f in item_config["fields"]:
                                position = f['position'] if 'position' in f.keys() else None
                                transform = f['transform'] if 'transform' in f.keys() else None

                                obj[f['name']] = self._retrieve_field(c, f['selector'], f['type'], position, transform, when)
                            output.append(obj)

                        # Handle Pagination navigation
                        if pagination:
                            if pagination['navigation'] == 'button':
                                next_button = soup.select_one(pagination['selector'])
                                if next_button is None:
                                    next_page = False
                                else:
                                    next_button = driver.find_element(By.CLASS_NAME, pagination['selector'][1:])
                                    if next_button.tag_name == 'a':
                                        next_button.click()
                                    else:
                                        next_button = next_button.find_element(By.TAG_NAME, 'a')
                                    cur_page += 1
                                    next_button.click()
                            elif pagination['navigation'] == 'url':
                                cur_page += 1
                                driver.get(url +  re.sub(r"\{[^}]+\}", str(cur_page), pagination['url_template']))
                        else:
                            next_page = False
                                             
        driver.close()
        self._output = output
        return output

    def _retrieve_field(self, container, selector, type, position, transform, when):
        field = None
        element = container.select_one(selector)
        if not element:
            return field

        if position == 'next':
            element = element.next_sibling        

        if type == "text":
            field = element.text.strip()
        elif type == "number":
            field = int(element.text.strip())
        elif type == "image":
            if not element.has_attr("src"):
                element = element.find("img")
            field = element["src"]

        if transform:
            for t in transform:
                operation = t["operation"]
                if operation == "split":
                    on = t["by"]
                    idx = t["index"]
                    if on is None or idx is None:
                        raise InvalidOperationArguments(f"Invalid operation arguments for {operation}.")
                    field = field.split(on)[idx].strip()
                else:
                    raise InvalidOperation(f"Operation {operation} not supported.")

        return field


    def _dump(self):
        out_conf = self._config["output"]

        if out_conf["format"] == "json":
            with open(out_conf["file"], "w") as f:
                json.dump(self._output, f, indent=4)

if __name__ == "__main__":
    s = Sucateiro(sys.argv[1])
    s._scrape()
    s._dump()