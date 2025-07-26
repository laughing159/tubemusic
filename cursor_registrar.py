import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
from browser_manager import BrowserManager
from config import AccountData

class CursorRegistrar:
    def __init__(self, browser_manager: BrowserManager):
        self.browser = browser_manager
        self.driver = browser_manager.driver
        
    def register_account(self, account_data: AccountData) -> dict:
        """
        Attempt to register a Cursor account
        Note: This is for educational purposes and may not work due to anti-bot measures.
        """
        result = {
            'success': False,
            'email': account_data.email,
            'error': None,
            'step_reached': None
        }
        
        try:
            logger.info(f"Starting Cursor registration for {account_data.email}")
            
            # Navigate to Cursor signup page
            self.driver.get("https://cursor.sh/sign-up")
            self.browser.random_delay()
            result['step_reached'] = 'page_loaded'
            
            # Wait for page to fully load
            time.sleep(3)
            
            # Check if we're on the right page
            if "sign-up" not in self.driver.current_url.lower() and "signup" not in self.driver.current_url.lower():
                # Try alternative URLs
                alternative_urls = [
                    "https://www.cursor.so/sign-up",
                    "https://cursor.com/signup",
                    "https://app.cursor.sh/signup"
                ]
                
                for url in alternative_urls:
                    try:
                        self.driver.get(url)
                        time.sleep(2)
                        if self.driver.current_url != url:
                            continue
                        break
                    except:
                        continue
                else:
                    result['error'] = 'Could not find Cursor signup page'
                    return result
            
            result['step_reached'] = 'signup_page_found'
            
            # Look for email field with various possible selectors
            email_selectors = [
                (By.ID, "email"),
                (By.NAME, "email"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.CSS_SELECTOR, "input[placeholder*='email' i]"),
                (By.CSS_SELECTOR, "input[placeholder*='Email' i]"),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email')]")
            ]
            
            email_field_found = False
            for selector_type, selector in email_selectors:
                try:
                    email_element = self.browser.wait_for_element((selector_type, selector), timeout=5)
                    if email_element:
                        if self.browser.safe_send_keys((selector_type, selector), account_data.email):
                            email_field_found = True
                            result['step_reached'] = 'email_filled'
                            break
                except:
                    continue
            
            if not email_field_found:
                result['error'] = 'Email field not found'
                return result
            
            # Look for password field
            password_selectors = [
                (By.ID, "password"),
                (By.NAME, "password"),
                (By.CSS_SELECTOR, "input[type='password']"),
                (By.CSS_SELECTOR, "input[placeholder*='password' i]"),
                (By.CSS_SELECTOR, "input[placeholder*='Password' i]"),
                (By.XPATH, "//input[@type='password']")
            ]
            
            password_field_found = False
            for selector_type, selector in password_selectors:
                try:
                    password_element = self.browser.wait_for_element((selector_type, selector), timeout=5)
                    if password_element:
                        if self.browser.safe_send_keys((selector_type, selector), account_data.password):
                            password_field_found = True
                            result['step_reached'] = 'password_filled'
                            break
                except:
                    continue
            
            if not password_field_found:
                result['error'] = 'Password field not found'
                return result
            
            # Look for confirm password field (if exists)
            confirm_password_selectors = [
                (By.ID, "confirm-password"),
                (By.ID, "confirmPassword"),
                (By.NAME, "confirm-password"),
                (By.NAME, "confirmPassword"),
                (By.CSS_SELECTOR, "input[placeholder*='confirm' i]"),
                (By.XPATH, "//input[contains(@placeholder, 'confirm') or contains(@placeholder, 'Confirm')]")
            ]
            
            for selector_type, selector in confirm_password_selectors:
                try:
                    confirm_element = self.browser.wait_for_element((selector_type, selector), timeout=3)
                    if confirm_element:
                        self.browser.safe_send_keys((selector_type, selector), account_data.password)
                        result['step_reached'] = 'confirm_password_filled'
                        break
                except:
                    continue
            
            # Look for first name field (if exists)
            if account_data.first_name:
                first_name_selectors = [
                    (By.ID, "firstName"),
                    (By.ID, "first-name"),
                    (By.NAME, "firstName"),
                    (By.NAME, "first-name"),
                    (By.CSS_SELECTOR, "input[placeholder*='first' i]"),
                    (By.XPATH, "//input[contains(@placeholder, 'first') or contains(@placeholder, 'First')]")
                ]
                
                for selector_type, selector in first_name_selectors:
                    try:
                        element = self.browser.wait_for_element((selector_type, selector), timeout=3)
                        if element:
                            self.browser.safe_send_keys((selector_type, selector), account_data.first_name)
                            result['step_reached'] = 'first_name_filled'
                            break
                    except:
                        continue
            
            # Look for last name field (if exists)
            if account_data.last_name:
                last_name_selectors = [
                    (By.ID, "lastName"),
                    (By.ID, "last-name"),
                    (By.NAME, "lastName"),
                    (By.NAME, "last-name"),
                    (By.CSS_SELECTOR, "input[placeholder*='last' i]"),
                    (By.XPATH, "//input[contains(@placeholder, 'last') or contains(@placeholder, 'Last')]")
                ]
                
                for selector_type, selector in last_name_selectors:
                    try:
                        element = self.browser.wait_for_element((selector_type, selector), timeout=3)
                        if element:
                            self.browser.safe_send_keys((selector_type, selector), account_data.last_name)
                            result['step_reached'] = 'last_name_filled'
                            break
                    except:
                        continue
            
            # Handle terms and conditions checkbox (if exists)
            terms_selectors = [
                (By.CSS_SELECTOR, "input[type='checkbox']"),
                (By.XPATH, "//input[@type='checkbox']"),
                (By.CSS_SELECTOR, "input[name*='terms']"),
                (By.CSS_SELECTOR, "input[name*='agree']"),
                (By.XPATH, "//input[contains(@name, 'terms') or contains(@name, 'agree')]")
            ]
            
            for selector_type, selector in terms_selectors:
                try:
                    checkbox = self.browser.wait_for_element((selector_type, selector), timeout=3)
                    if checkbox and not checkbox.is_selected():
                        self.browser.safe_click((selector_type, selector))
                        result['step_reached'] = 'terms_accepted'
                        break
                except:
                    continue
            
            # Look for submit button
            submit_selectors = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.CSS_SELECTOR, "input[type='submit']"),
                (By.XPATH, "//button[contains(text(), 'Sign up') or contains(text(), 'Sign Up') or contains(text(), 'Create') or contains(text(), 'Register')]"),
                (By.XPATH, "//input[@value='Sign up' or @value='Sign Up' or @value='Create' or @value='Register']"),
                (By.ID, "submit"),
                (By.CLASS_NAME, "submit"),
                (By.CSS_SELECTOR, ".btn-primary"),
                (By.CSS_SELECTOR, ".signup-btn")
            ]
            
            submit_clicked = False
            for selector_type, selector in submit_selectors:
                try:
                    submit_element = self.browser.wait_for_element((selector_type, selector), timeout=5)
                    if submit_element and submit_element.is_enabled():
                        if self.browser.safe_click((selector_type, selector)):
                            submit_clicked = True
                            result['step_reached'] = 'form_submitted'
                            break
                except:
                    continue
            
            if not submit_clicked:
                result['error'] = 'Submit button not found or not clickable'
                return result
            
            # Wait for response
            time.sleep(5)
            
            # Check for success indicators
            current_url = self.driver.current_url
            page_source = self.driver.page_source.lower()
            
            success_indicators = [
                "welcome",
                "dashboard",
                "success",
                "verification",
                "check your email",
                "account created"
            ]
            
            error_indicators = [
                "error",
                "invalid",
                "already exists",
                "taken",
                "failed"
            ]
            
            # Check URL for success
            if any(indicator in current_url.lower() for indicator in success_indicators):
                result['success'] = True
                result['step_reached'] = 'account_created'
                logger.success(f"Cursor account created successfully: {account_data.email}")
                return result
            
            # Check page content for success/error messages
            if any(indicator in page_source for indicator in success_indicators):
                result['success'] = True
                result['step_reached'] = 'account_created'
                logger.success(f"Cursor account created successfully: {account_data.email}")
                return result
            
            if any(indicator in page_source for indicator in error_indicators):
                result['error'] = 'Registration failed - error message detected'
                result['step_reached'] = 'error_detected'
                return result
            
            # If we can't determine success/failure
            result['error'] = 'Registration status unclear'
            result['step_reached'] = 'status_unclear'
            
        except TimeoutException as e:
            result['error'] = f'Timeout: {e}'
            logger.error(f"Timeout during Cursor registration: {e}")
        except Exception as e:
            result['error'] = f'Unexpected error: {e}'
            logger.error(f"Unexpected error during Cursor registration: {e}")
        
        return result
    
    def check_registration_success(self) -> bool:
        """Check if registration was successful by analyzing the current page"""
        try:
            current_url = self.driver.current_url.lower()
            page_source = self.driver.page_source.lower()
            
            # Success indicators
            success_patterns = [
                "dashboard",
                "welcome",
                "profile",
                "settings",
                "logout",
                "account created",
                "registration successful"
            ]
            
            return any(pattern in current_url or pattern in page_source for pattern in success_patterns)
            
        except Exception as e:
            logger.error(f"Error checking registration success: {e}")
            return False