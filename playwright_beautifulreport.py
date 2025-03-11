import re
from playwright.sync_api import Page, expect, sync_playwright
import unittest
from BeautifulReport import BeautifulReport

basedir = "projest_path"


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = sync_playwright().start()
        cls.browser = cls.p.chromium.launch()
        cls.context = cls.browser.new_context()
        cls.context.set_default_timeout(5_000)

    def setUp(self):
        self.page = Test.context.new_page()

    def tearDown(self):
        self.page.close()

    @classmethod
    def tearDownClass(cls):
        cls.context.close()
        cls.browser.close()
        cls.p.stop()

    def test_has_title(self):
        self.page.goto("https://playwright.dev/")

        # Expect a title "to contain" a substring.
        expect(self.page).to_have_title(re.compile("Playwright"))

    def test_get_started_link(self):
        page = self.page
        page.goto("https://playwright.dev/")

        # Click the get started link.
        page.get_by_role("link", name="Get started").click()

        # Expects page to have a heading with the name of Installation.
        expect(page.get_by_role("heading", name="Installation")).to_be_visible()


if __name__ == '__main__':
    test_suite = unittest.defaultTestLoader.discover(basedir, pattern='playwright_beautifulreport.py')
    result = BeautifulReport(test_suite)
    result.report(filename='report', description='Playwright', log_path=basedir)
