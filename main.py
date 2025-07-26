#!/usr/bin/env python3
"""
Account Registration Automation Tool

IMPORTANT DISCLAIMER:
This tool is for educational and testing purposes only. 
Automated account registration may violate Terms of Service of various platforms.
Use responsibly and at your own risk.

Author: AI Assistant
"""

import json
import sys
import argparse
from typing import List, Dict
from pathlib import Path
from loguru import logger

from config import get_config, AccountData
from account_generator import AccountGenerator
from browser_manager import BrowserManager
from gmail_registrar import GmailRegistrar
from cursor_registrar import CursorRegistrar

class AutomationManager:
    def __init__(self):
        self.config = get_config()
        self.account_generator = AccountGenerator()
        self.results = []
        
        # Setup logging
        logger.remove()
        logger.add(
            sys.stderr, 
            level=self.config.log_level,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
        )
        logger.add(
            "automation.log",
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
            rotation="10 MB"
        )
    
    def register_gmail_accounts(self, count: int) -> List[Dict]:
        """Register multiple Gmail accounts"""
        logger.info(f"Starting Gmail registration for {count} accounts")
        results = []
        
        # Generate account data
        accounts = self.account_generator.generate_multiple_accounts(count, "gmail.com")
        
        for i, account_data in enumerate(accounts, 1):
            logger.info(f"Processing Gmail account {i}/{count}: {account_data.email}")
            
            try:
                with BrowserManager(self.config) as browser:
                    registrar = GmailRegistrar(browser)
                    result = registrar.register_account(account_data)
                    result['account_data'] = account_data.dict()
                    result['service'] = 'gmail'
                    result['attempt_number'] = i
                    results.append(result)
                    
                    if result['success']:
                        logger.success(f"✅ Gmail account {i} created successfully")
                    else:
                        logger.error(f"❌ Gmail account {i} failed: {result['error']}")
                        
            except Exception as e:
                error_result = {
                    'success': False,
                    'email': account_data.email,
                    'error': f'Browser setup failed: {e}',
                    'step_reached': 'browser_setup_failed',
                    'account_data': account_data.dict(),
                    'service': 'gmail',
                    'attempt_number': i
                }
                results.append(error_result)
                logger.error(f"❌ Gmail account {i} browser setup failed: {e}")
        
        return results
    
    def register_cursor_accounts(self, count: int) -> List[Dict]:
        """Register multiple Cursor accounts"""
        logger.info(f"Starting Cursor registration for {count} accounts")
        results = []
        
        # Generate account data
        accounts = []
        for _ in range(count):
            account = self.account_generator.generate_cursor_specific_data()
            accounts.append(account)
        
        for i, account_data in enumerate(accounts, 1):
            logger.info(f"Processing Cursor account {i}/{count}: {account_data.email}")
            
            try:
                with BrowserManager(self.config) as browser:
                    registrar = CursorRegistrar(browser)
                    result = registrar.register_account(account_data)
                    result['account_data'] = account_data.dict()
                    result['service'] = 'cursor'
                    result['attempt_number'] = i
                    results.append(result)
                    
                    if result['success']:
                        logger.success(f"✅ Cursor account {i} created successfully")
                    else:
                        logger.error(f"❌ Cursor account {i} failed: {result['error']}")
                        
            except Exception as e:
                error_result = {
                    'success': False,
                    'email': account_data.email,
                    'error': f'Browser setup failed: {e}',
                    'step_reached': 'browser_setup_failed',
                    'account_data': account_data.dict(),
                    'service': 'cursor',
                    'attempt_number': i
                }
                results.append(error_result)
                logger.error(f"❌ Cursor account {i} browser setup failed: {e}")
        
        return results
    
    def save_results(self, results: List[Dict], filename: str = None):
        """Save registration results to JSON file"""
        if not filename:
            filename = self.config.output_file
        
        # Ensure the file has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
    
    def print_summary(self, results: List[Dict]):
        """Print a summary of registration results"""
        total_attempts = len(results)
        successful = sum(1 for r in results if r['success'])
        failed = total_attempts - successful
        
        logger.info("\n" + "="*50)
        logger.info("REGISTRATION SUMMARY")
        logger.info("="*50)
        logger.info(f"Total attempts: {total_attempts}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success rate: {(successful/total_attempts*100):.1f}%" if total_attempts > 0 else "0%")
        
        if successful > 0:
            logger.info("\n✅ SUCCESSFUL ACCOUNTS:")
            for result in results:
                if result['success']:
                    logger.info(f"  - {result['email']} ({result['service']})")
        
        if failed > 0:
            logger.info("\n❌ FAILED ACCOUNTS:")
            for result in results:
                if not result['success']:
                    logger.info(f"  - {result['email']} ({result['service']}): {result['error']}")
        
        logger.info("="*50)

def main():
    parser = argparse.ArgumentParser(
        description="Account Registration Automation Tool",
        epilog="⚠️  DISCLAIMER: This tool is for educational purposes only. Use responsibly!"
    )
    
    parser.add_argument(
        '--service', 
        choices=['gmail', 'cursor', 'both'], 
        default='both',
        help='Service to register accounts for (default: both)'
    )
    
    parser.add_argument(
        '--count', 
        type=int, 
        default=1,
        help='Number of accounts to register (default: 1)'
    )
    
    parser.add_argument(
        '--headless', 
        action='store_true',
        help='Run browser in headless mode'
    )
    
    parser.add_argument(
        '--output', 
        type=str,
        help='Output file for results (default: registered_accounts.json)'
    )
    
    parser.add_argument(
        '--test-mode', 
        action='store_true',
        help='Test mode - generate account data without registration'
    )
    
    args = parser.parse_args()
    
    # Display disclaimer
    print("\n" + "="*60)
    print("⚠️  IMPORTANT DISCLAIMER")
    print("="*60)
    print("This tool is for EDUCATIONAL and TESTING purposes only.")
    print("Automated account registration may violate Terms of Service.")
    print("The authors are not responsible for misuse of this tool.")
    print("Use at your own risk and ensure compliance with applicable laws.")
    print("="*60)
    
    response = input("\nDo you understand and accept these terms? (yes/no): ").lower().strip()
    if response not in ['yes', 'y']:
        print("Exiting...")
        sys.exit(0)
    
    # Initialize automation manager
    automation = AutomationManager()
    
    # Override config with command line arguments
    if args.headless:
        automation.config.headless = True
    
    # Test mode - just generate account data
    if args.test_mode:
        logger.info("Running in test mode - generating account data only")
        accounts = automation.account_generator.generate_multiple_accounts(args.count)
        
        print(f"\n📊 Generated {len(accounts)} test accounts:")
        for i, account in enumerate(accounts, 1):
            print(f"{i}. {account.email} | {account.first_name} {account.last_name}")
        
        if args.output:
            test_results = [{'account_data': account.dict(), 'test_mode': True} for account in accounts]
            automation.save_results(test_results, args.output)
        
        return
    
    # Run registration
    all_results = []
    
    if args.service in ['gmail', 'both']:
        logger.info(f"🚀 Starting Gmail registration for {args.count} accounts")
        gmail_results = automation.register_gmail_accounts(args.count)
        all_results.extend(gmail_results)
    
    if args.service in ['cursor', 'both']:
        logger.info(f"🚀 Starting Cursor registration for {args.count} accounts")
        cursor_results = automation.register_cursor_accounts(args.count)
        all_results.extend(cursor_results)
    
    # Save and display results
    automation.save_results(all_results, args.output)
    automation.print_summary(all_results)
    
    logger.info("🏁 Automation completed!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⏹️  Automation stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Fatal error: {e}")
        sys.exit(1)