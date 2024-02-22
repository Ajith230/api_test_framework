import logging

from framework.driver import Driver


class SimpleApiDriverCopy:
    def __init__(self, current_driver: Driver, url: str):
        self.current_driver = current_driver
        self.new_url = url

    def __enter__(self):
        class NewDriver(self.current_driver.__class__):
            def __init__(self, driver: Driver, url: str):
                super().__init__(driver.get_api_url())
                self.set_api_url(url)
                logging.info("Entered SimpleApiDriverCopy context manager with url: %s", url)

        return NewDriver(self.current_driver, self.new_url)

    def __exit__(self, *args):
        logging.info("Exiting SimpleApiDriverCopy context manager")
