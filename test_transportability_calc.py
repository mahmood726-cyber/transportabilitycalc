"""
Selenium tests for Clinical Transportability Calculator.
20 tests covering all 5 tabs, calculations, examples, dark mode, exports, ARIA, etc.
"""
import io
import os
import sys
import json
import time
import math
import unittest

# Force UTF-8 stdout for Windows
if 'pytest' not in sys.modules and hasattr(sys.stdout, 'buffer'):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'transportability-calc.html')
FILE_URL = 'file:///' + HTML_PATH.replace('\\', '/')


def get_driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1400,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(3)
    return driver


class TransportabilityCalcTests(unittest.TestCase):
    """20 Selenium tests for the Clinical Transportability Calculator."""

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(FILE_URL)
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def reload(self):
        self.driver.get(FILE_URL)
        time.sleep(0.3)

    def fill_statins_example(self):
        """Click the Statins example button."""
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-example="statins"]')
        btn.click()
        time.sleep(0.2)

    def fill_tcas_example(self):
        """Click the TCAs example button."""
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-example="tcas"]')
        btn.click()
        time.sleep(0.2)

    def fill_betablockers_example(self):
        """Click the Beta-blockers example button."""
        btn = self.driver.find_element(By.CSS_SELECTOR, '[data-example="betablockers"]')
        btn.click()
        time.sleep(0.2)

    def click_calculate(self):
        btn = self.driver.find_element(By.ID, 'btnCalculate')
        btn.click()
        time.sleep(0.5)

    def get_verdict_score(self):
        el = self.driver.find_element(By.ID, 'verdict-score')
        return float(el.text)

    def get_verdict_label(self):
        el = self.driver.find_element(By.ID, 'verdict-label')
        return el.text

    # ===== TEST 1: Page loads with correct title =====
    def test_01_page_loads(self):
        self.assertIn('Clinical Transportability Calculator', self.driver.title)

    # ===== TEST 2: All 5 tabs exist with correct ARIA roles =====
    def test_02_tabs_exist(self):
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        self.assertEqual(len(tabs), 5)
        panels = self.driver.find_elements(By.CSS_SELECTOR, '[role="tabpanel"]')
        self.assertEqual(len(panels), 5)
        # First tab is selected
        self.assertEqual(tabs[0].get_attribute('aria-selected'), 'true')

    # ===== TEST 3: Tab switching works =====
    def test_03_tab_switching(self):
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '[role="tab"]')
        # Click assessment tab
        tabs[1].click()
        time.sleep(0.2)
        self.assertEqual(tabs[1].get_attribute('aria-selected'), 'true')
        self.assertEqual(tabs[0].get_attribute('aria-selected'), 'false')
        panel = self.driver.find_element(By.ID, 'panel-assess')
        self.assertIn('active', panel.get_attribute('class'))
        # Go back to input tab
        tabs[0].click()
        time.sleep(0.2)

    # ===== TEST 4: Statins example loads correct values =====
    def test_04_statins_example(self):
        self.reload()
        self.fill_statins_example()
        effect = self.driver.find_element(By.ID, 'inp-effect').get_attribute('value')
        self.assertEqual(effect, '0.75')
        k = self.driver.find_element(By.ID, 'inp-k').get_attribute('value')
        self.assertEqual(k, '26')
        domain = Select(self.driver.find_element(By.ID, 'inp-domain'))
        self.assertEqual(domain.first_selected_option.get_attribute('value'), 'cardiovascular')

    # ===== TEST 5: TCAs example loads correct values =====
    def test_05_tcas_example(self):
        self.reload()
        self.fill_tcas_example()
        effect = self.driver.find_element(By.ID, 'inp-effect').get_attribute('value')
        self.assertEqual(effect, '0.64')
        i2 = self.driver.find_element(By.ID, 'inp-i2').get_attribute('value')
        self.assertEqual(i2, '68')

    # ===== TEST 6: Beta-blockers example loads =====
    def test_06_betablockers_example(self):
        self.reload()
        self.fill_betablockers_example()
        effect = self.driver.find_element(By.ID, 'inp-effect').get_attribute('value')
        self.assertEqual(effect, '0.77')
        scale = Select(self.driver.find_element(By.ID, 'inp-scale'))
        self.assertEqual(scale.first_selected_option.get_attribute('value'), 'large')

    # ===== TEST 7: Statins example reflects the shipped low-transportability verdict =====
    def test_07_statins_example_verdict(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        label = self.get_verdict_label()
        score = self.get_verdict_score()
        self.assertIn('LOW', label)
        self.assertLess(score, 0.70)

    # ===== TEST 8: TCAs calculation gives LOW transportability =====
    def test_08_tcas_low_transport(self):
        self.reload()
        self.fill_tcas_example()
        self.click_calculate()
        label = self.get_verdict_label()
        score = self.get_verdict_score()
        # TCAs from 1970s-80s should have low transportability
        self.assertLess(score, 0.70)
        self.assertIn('LOW', label)

    # ===== TEST 9: Assessment tab shows results after calculation =====
    def test_09_assessment_results_visible(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        results = self.driver.find_element(By.ID, 'assess-results')
        self.assertEqual(results.value_of_css_property('display'), 'block')
        placeholder = self.driver.find_element(By.ID, 'assess-placeholder')
        self.assertEqual(placeholder.value_of_css_property('display'), 'none')

    # ===== TEST 10: Component bars are rendered =====
    def test_10_component_bars(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        bars = self.driver.find_elements(By.CSS_SELECTOR, '.component-bar-container')
        self.assertEqual(len(bars), 5)

    # ===== TEST 11: Gauge needle is present and rotated =====
    def test_11_gauge_needle(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        needle = self.driver.find_element(By.ID, 'gauge-needle')
        transform = needle.get_attribute('transform')
        self.assertIn('rotate', transform)

    # ===== TEST 12: Sensitivity tab shows temporal chart =====
    def test_12_sensitivity_tab(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        # Switch to sensitivity tab
        tab = self.driver.find_element(By.ID, 'tab-sensitivity')
        tab.click()
        time.sleep(0.3)
        canvas = self.driver.find_element(By.ID, 'chart-temporal')
        self.assertTrue(canvas.is_displayed())

    # ===== TEST 13: Factor isolation table is populated =====
    def test_13_isolation_table(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        tab = self.driver.find_element(By.ID, 'tab-sensitivity')
        tab.click()
        time.sleep(0.3)
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-isolation tbody tr')
        self.assertEqual(len(rows), 5)

    # ===== TEST 14: Domain comparison table has all domains =====
    def test_14_domain_table(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        tab = self.driver.find_element(By.ID, 'tab-sensitivity')
        tab.click()
        time.sleep(0.3)
        rows = self.driver.find_elements(By.CSS_SELECTOR, '#table-domains tbody tr')
        self.assertEqual(len(rows), 13)  # 13 domains

    # ===== TEST 15: Benchmarks tab shows histogram =====
    def test_15_benchmarks_histogram(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        tab = self.driver.find_element(By.ID, 'tab-benchmarks')
        tab.click()
        time.sleep(0.3)
        bars = self.driver.find_elements(By.CSS_SELECTOR, '.histogram-bar')
        self.assertEqual(len(bars), 20)

    # ===== TEST 16: Percentile text is populated =====
    def test_16_percentile_text(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        tab = self.driver.find_element(By.ID, 'tab-benchmarks')
        tab.click()
        time.sleep(0.3)
        text = self.driver.find_element(By.ID, 'percentile-text').text
        self.assertIn('more transportable than', text)
        self.assertIn('Cochrane', text)

    # ===== TEST 17: Report tab generates methods text =====
    def test_17_report_generated(self):
        self.reload()
        self.fill_statins_example()
        self.click_calculate()
        tab = self.driver.find_element(By.ID, 'tab-report')
        tab.click()
        time.sleep(0.3)
        content = self.driver.find_element(By.ID, 'report-content').text
        self.assertIn('Ahmad', content)
        self.assertIn('Bareinboim', content)
        self.assertIn('Dahabreh', content)
        self.assertIn('CTE penalty index', content)

    # ===== TEST 18: Dark mode toggle works =====
    def test_18_dark_mode(self):
        self.reload()
        btn = self.driver.find_element(By.ID, 'btnDarkMode')
        # Toggle on
        btn.click()
        time.sleep(0.2)
        body_class = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        self.assertIn('dark-mode', body_class)
        self.assertEqual(btn.text, 'Light Mode')
        # Toggle off
        btn.click()
        time.sleep(0.2)
        body_class = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class')
        self.assertNotIn('dark-mode', body_class)
        self.assertEqual(btn.text, 'Dark Mode')

    # ===== TEST 19: Reset clears inputs =====
    def test_19_reset(self):
        self.reload()
        self.fill_statins_example()
        # Verify an input is filled
        self.assertNotEqual(self.driver.find_element(By.ID, 'inp-effect').get_attribute('value'), '')
        # Click reset
        self.driver.find_element(By.ID, 'btnReset').click()
        time.sleep(0.3)
        # Check input is cleared
        self.assertEqual(self.driver.find_element(By.ID, 'inp-effect').get_attribute('value'), '')

    # ===== TEST 20: Validation rejects incomplete input =====
    def test_20_validation_rejects_incomplete(self):
        self.reload()
        # Clear default target year to ensure validation works
        target_year = self.driver.find_element(By.ID, 'inp-target-year')
        target_year.clear()
        # Try to calculate without filling anything
        self.click_calculate()
        # Should show an alert - switch to it
        try:
            alert = WebDriverWait(self.driver, 2).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            self.assertIn('required', alert_text.lower())
        except Exception:
            # If no alert, check that assessment results are still hidden
            placeholder = self.driver.find_element(By.ID, 'assess-placeholder')
            self.assertNotEqual(placeholder.value_of_css_property('display'), 'none')


if __name__ == '__main__':
    # Kill any orphan chrome processes
    os.system('taskkill /f /im chromedriver.exe 2>NUL')
    os.system('taskkill /f /im chrome.exe 2>NUL')
    time.sleep(1)
    unittest.main(verbosity=2)
