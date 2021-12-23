# -*- coding: utf-8 -*-
from typing import List

from configuration import Configuration
from models.product import Product

__author__ = 'CoderGosha'

import logging
from webdriver_manager.chrome import ChromeDriverManager

from services.avito_block_service import AvitoBlockService
from services.request_service import RequestService


class AvitoParsing:

    def __init__(self, start_url, id_parser, block_service: AvitoBlockService):
        self.StartUrl = start_url
        self.ResultElement = []
        self.IdParser = id_parser
        self.block_service = block_service
        self.request_service = RequestService()

    def parsing_start(self) -> List[Product]:
        # При привешении блокировок метод выключит сервис
        self.block_service.is_parsing()

        return self._parsing_catalog_auto()

    def _parsing_catalog_auto(self) -> List[Product]:
        self.ResultElement = []

        try:
            # load the desired webpage
            driver = self.request_service.get(self.StartUrl)
            try:
                driver.find_element_by_class_name("icon-forbidden")
                self.block_service.add_block()
                return []
            except:
                pass
            # HACK
            wight = None

            for entry in driver.find_elements_by_xpath('//div[@itemtype="http://schema.org/Product"]'):
                link = entry.find_element_by_xpath('.//a[@itemprop="url"]').get_attribute("href")
                description = entry.find_element_by_xpath('.//meta[@itemprop="description"]').get_attribute("content")
                price = entry.find_element_by_xpath('.//span[@itemtype="http://schema.org/Offer"]').text
                name = entry.find_element_by_xpath('.//h3[@itemprop="name"]').text
                if not wight:
                    wight = entry.size["width"]
                if wight != entry.size["width"]:
                    #
                    logging.info(f"Skip: {link}")
                    continue

                if len(link) > 1:
                    link = link.replace('file:///', 'https://avito.ru/')
                    self.ResultElement.append(
                        Product(url=link, description=description, parser_id=self.IdParser, price=price, name=name))
                    logging.debug(f"{name}, {price}, {link}")
                if len(self.ResultElement) > 10:
                    break
        except Exception as ex:
            logging.error(ex)

        finally:
            pass

        logging.info('Parsing completed: %s - %i' % (self.StartUrl, len(self.ResultElement)))
        return self.ResultElement


def main():
    logging.basicConfig(level=logging.DEBUG)
    block = AvitoBlockService()
    parser = AvitoParsing(
        'https://www.avito.ru/vologda/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgkjlmQWQFF6AcTeyJmcm9tIjo0NCwidG8iOjYwfQ',
        1,
        block)
    result = parser.parsing_start()
    for r in result:
        logging.debug(f"{r.name}, {r.price}, {r.url}")


if __name__ == "__main__":
    main()
