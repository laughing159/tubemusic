import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from loguru import logger
from browser_manager import BrowserManager
from config import AccountData, AutomationConfig

class GmailRegistrar:
    def __init__(self, browser_manager: BrowserManager):
        self.browser = browser_manager
        self.driver = browser_manager.driver
        
    def register_account(self, account_data: AccountData) -> dict:
        """
        Attempt to register a Gmail account
        Note: This is for educational purposes. Gmail has strong anti-bot measures.
        """
        result = {
            'success': False,
            'email': account_data.email,
            'error': None,
            'step_reached': None
        }
        
        try:
            logger.info(f"Starting Gmail registration for {account_data.email}")
            
            # Navigate to Gmail signup page
            self.driver.get("https://accounts.google.com/signup/v2/webcreateaccount?flowName=GlifWebSignIn&flowEntry=SignUp")
            self.browser.random_delay()
            result['step_reached'] = 'page_loaded'
            
            # Fill first name
            if not self._fill_field(By.ID, "firstName", account_data.first_name):
                result['error'] = 'Failed to fill first name'
                return result
            result['step_reached'] = 'first_name_filled'
            
            # Fill last name
            if not self._fill_field(By.ID, "lastName", account_data.last_name):
                result['error'] = 'Failed to fill last name'
                return result
            result['step_reached'] = 'last_name_filled'
            
            # Click Next
            if not self.browser.safe_click((By.ID, "collectNameNext")):
                result['error'] = 'Failed to click Next after names'
                return result
            result['step_reached'] = 'names_submitted'
            
            # Fill birth date and gender
            time.sleep(2)  # Wait for page transition
            
            # Birth month (dropdown)
            try:
                month_dropdown = Select(self.driver.find_element(By.ID, "month"))
                birth_parts = account_data.birth_date.split('/')
                month_dropdown.select_by_value(birth_parts[0])
                self.browser.random_delay()
                result['step_reached'] = 'birth_month_selected'
            except Exception as e:
                logger.warning(f"Failed to select birth month: {e}")
            
            # Birth day
            if not self._fill_field(By.ID, "day", birth_parts[1]):
                logger.warning("Failed to fill birth day")
            
            # Birth year
            if not self._fill_field(By.ID, "year", birth_parts[2]):
                logger.warning("Failed to fill birth year")
            
            # Gender selection
            try:
                gender_dropdown = Select(self.driver.find_element(By.ID, "gender"))
                gender_dropdown.select_by_value(str(random.randint(1, 3)))  # Random gender
                self.browser.random_delay()
                result['step_reached'] = 'personal_info_filled'
            except Exception as e:
                logger.warning(f"Failed to select gender: {e}")
            
            # Click Next
            if not self.browser.safe_click((By.ID, "birthdaygenderNext")):
                result['error'] = 'Failed to click Next after personal info'
                return result
            result['step_reached'] = 'personal_info_submitted'
            
            # Username selection
            time.sleep(3)  # Wait for username page
            
            # Try to use suggested username or create custom one
            try:
                # Look for suggested usernames first
                suggested_usernames = self.driver.find_elements(By.CSS_SELECTOR, "[data-value]")
                if suggested_usernames:
                    suggested_usernames[0].click()
                    self.browser.random_delay()
                    result['step_reached'] = 'username_selected'
                else:
                    # Create custom username
                    username = account_data.email.split('@')[0]
                    if not self._fill_field(By.ID, "username", username):
                        result['error'] = 'Failed to fill username'
                        return result
                    result['step_reached'] = 'username_entered'
            except Exception as e:
                logger.error(f"Username selection failed: {e}")
                result['error'] = f'Username selection failed: {e}'
                return result
            
            # Click Next
            if not self.browser.safe_click((By.ID, "next")):
                result['error'] = 'Failed to click Next after username'
                return result
            result['step_reached'] = 'username_submitted'
            
            # Password creation
            time.sleep(2)
            if not self._fill_field(By.NAME, "Passwd", account_data.password):
                result['error'] = 'Failed to fill password'
                return result
            
            if not self._fill_field(By.NAME, "ConfirmPasswd", account_data.password):
                result['error'] = 'Failed to confirm password'
                return result
            result['step_reached'] = 'password_filled'
            
            # Click Next
            if not self.browser.safe_click((By.ID, "createpasswordNext")):
                result['error'] = 'Failed to click Next after password'
                return result
            result['step_reached'] = 'password_submitted'
            
            # Phone verification (this is where most automation fails)
            time.sleep(3)
            
            # Check if phone verification is required
            if self._is_phone_verification_required():
                logger.warning("Phone verification required - this typically blocks automation")
                result['error'] = 'Phone verification required'
                result['step_reached'] = 'phone_verification_required'
                
                # Attempt to fill phone number anyway
                if account_data.phone:
                    phone_field = self.driver.find_element(By.ID, "phoneNumberId")
                    if phone_field:
                        self._fill_field(By.ID, "phoneNumberId", account_data.phone)
                        self.browser.random_delay()
                        
                        # Click Next to send verification
                        self.browser.safe_click((By.ID, "next"))
                        result['step_reached'] = 'phone_submitted'
                        
                        # At this point, manual intervention would be needed for SMS code
                        logger.info("Phone verification code required - manual intervention needed")
                
                return result
            
            # If we get here without phone verification, continue
            result['step_reached'] = 'phone_verification_skipped'
            
            # Check for account creation success
            time.sleep(5)
            current_url = self.driver.current_url
            
            if "welcome" in current_url.lower() or "myaccount.google.com" in current_url:
                result['success'] = True
                result['step_reached'] = 'account_created'
                logger.success(f"Gmail account created successfully: {account_data.email}")
            else:
                result['error'] = 'Account creation status unclear'
                result['step_reached'] = 'creation_status_unclear'
            
        except TimeoutException as e:
            result['error'] = f'Timeout: {e}'
            logger.error(f"Timeout during Gmail registration: {e}")
        except Exception as e:
            result['error'] = f'Unexpected error: {e}'
            logger.error(f"Unexpected error during Gmail registration: {e}")
        
        return result
    
    def _fill_field(self, by, locator, value):
        """Helper method to fill form fields"""
        try:
            return self.browser.safe_send_keys((by, locator), value)
        except Exception as e:
            logger.error(f"Failed to fill field {locator}: {e}")
            return False
    
    def _is_phone_verification_required(self) -> bool:
        """Check if phone verification is required"""
        try:
            # Look for phone verification indicators
            phone_indicators = [
                "phoneNumberId",
                "Enter your phone number",
                "Verify your phone number",
                "phone-verification"
            ]
            
            for indicator in phone_indicators:
                try:
                    if indicator.startswith("#") or indicator.startswith("."):
                        elements = self.driver.find_elements(By.CSS_SELECTOR, indicator)
                    else:
                        elements = self.driver.find_elements(By.PARTIAL_LINK_TEXT, indicator)
                        if not elements:
                            elements = self.driver.find_elements(By.ID, indicator)
                    
                    if elements:
                        return True
                except:
                    continue
            
            return False
        except Exception:
            return True  # Assume phone verification is required if we can't determine