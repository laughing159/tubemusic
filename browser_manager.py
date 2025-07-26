import random
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from loguru import logger
from config import AutomationConfig

class BrowserManager:
    def __init__(self, config: AutomationConfig):
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        
    def setup_browser(self) -> webdriver.Chrome:
        """Setup and configure Chrome browser with anti-detection measures"""
        try:
            if self.config.use_undetected_chrome:
                options = uc.ChromeOptions()
            else:
                options = Options()
            
            # Basic options
            if self.config.headless:
                options.add_argument("--headless")
            
            # Anti-detection measures
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Performance optimizations
            if self.config.disable_images:
                prefs = {"profile.managed_default_content_settings.images": 2}
                options.add_experimental_option("prefs", prefs)
            
            # Random user agent
            if self.config.rotate_user_agents:
                user_agents = [
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                ]
                options.add_argument(f"--user-agent={random.choice(user_agents)}")
            
            # Proxy settings
            if self.config.proxy_host and self.config.proxy_port:
                options.add_argument(f"--proxy-server={self.config.proxy_host}:{self.config.proxy_port}")
            
            # Create driver
            if self.config.use_undetected_chrome:
                self.driver = uc.Chrome(options=options)
            else:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            
            # Configure timeouts
            self.driver.implicitly_wait(self.config.implicit_wait)
            self.driver.set_page_load_timeout(self.config.page_load_timeout)
            
            # Setup WebDriverWait
            self.wait = WebDriverWait(self.driver, self.config.implicit_wait)
            
            # Execute anti-detection script
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            logger.info("Browser setup completed successfully")
            return self.driver
            
        except Exception as e:
            logger.error(f"Failed to setup browser: {e}")
            raise
    
    def random_delay(self):
        """Add random delay between actions"""
        delay = random.uniform(self.config.min_delay, self.config.max_delay)
        time.sleep(delay)
    
    def safe_click(self, element_locator, timeout=10):
        """Safely click an element with retry logic"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(element_locator)
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.random_delay()
            element.click()
            return True
        except TimeoutException:
            logger.warning(f"Element not clickable: {element_locator}")
            return False
    
    def safe_send_keys(self, element_locator, text, timeout=10):
        """Safely send keys to an element with human-like typing"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(element_locator)
            )
            element.clear()
            
            # Human-like typing
            for char in text:
                element.send_keys(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            return True
        except TimeoutException:
            logger.warning(f"Element not found: {element_locator}")
            return False
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for element to be present"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("Browser closed successfully")
            except Exception as e:
                logger.error(f"Error closing browser: {e}")
    
    def __enter__(self):
        self.setup_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()