from selenium.webdriver.common.by import By

import re

class Paginator:
    def __init__(self, max_pages: int):
        self._max_pages = max_pages
        self._next_page_available = True
        self._current_page = 1

    def next_page(self, driver):
        pass

    def has_more_pages(self):
        return (self._current_page <= self._max_pages)


class ButtonPaginator(Paginator):
    def __init__(self, max_pages, button_selector):
        super().__init__(max_pages)
        self._button_selector = button_selector

    def next_page(self, driver):
        next_button = driver.find_element(By.CLASS_NAME, self._button_selector[1:])
        
        if not next_button:
            self._next_page_available = False
            return

        if next_button.tag_name != 'a':
            next_button = next_button.find_element(By.TAG_NAME, 'a')

        next_button.click()
        self._current_page += 1


class URLPaginator(Paginator):
    def __init__(self, max_pages, url_template):
        super().__init__(max_pages)
        self._url_template = url_template

    def next_page(self, driver):
        driver.get(self._render_template(driver.current_url))
        self._current_page += 1

    def _render_template(self, url):
        return url + re.sub(r"\{[^}]+\}", str(self._current_page + 1), self._url_template)