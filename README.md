
# Account Registration Automation Tool

⚠️ **IMPORTANT DISCLAIMER**: This tool is for educational and testing purposes only. Automated account registration may violate the Terms of Service of various platforms. Use responsibly and at your own risk.

## Overview

This automation tool helps register accounts on various platforms including Gmail and Cursor. It uses Selenium WebDriver with anti-detection measures to simulate human-like behavior during the registration process.

## Features

- 🤖 **Automated Registration**: Support for Gmail and Cursor account registration
- 🎭 **Anti-Detection**: Uses undetected-chromedriver and human-like behavior simulation
- 📊 **Realistic Data Generation**: Creates believable account information using Faker
- 🔄 **Batch Processing**: Register multiple accounts in sequence
- 📝 **Detailed Logging**: Comprehensive logging with different levels
- 💾 **Result Tracking**: Saves registration results to JSON files
- ⚙️ **Configurable**: Extensive configuration options via environment variables

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd account-registration-automation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup configuration**:
   ```bash
   cp .env.example .env
   # Edit .env file with your preferences
   ```

4. **Install Chrome browser** (if not already installed):
   - The tool will automatically download ChromeDriver
   - Make sure Google Chrome is installed on your system

## Usage

### Basic Usage

```bash
# Register 1 account for both Gmail and Cursor
python main.py

# Register 3 Gmail accounts only
python main.py --service gmail --count 3

# Register 2 Cursor accounts only
python main.py --service cursor --count 2

# Run in headless mode
python main.py --headless --count 5

# Test mode (generate data without registration)
python main.py --test-mode --count 10
```

### Command Line Options

- `--service {gmail,cursor,both}`: Choose which service to register for (default: both)
- `--count N`: Number of accounts to register (default: 1)
- `--headless`: Run browser in headless mode
- `--output FILE`: Specify output file for results
- `--test-mode`: Generate account data without actual registration

### Examples

```bash
# Register 5 Gmail accounts in headless mode
python main.py --service gmail --count 5 --headless

# Test account generation for 10 accounts
python main.py --test-mode --count 10 --output test_accounts.json

# Register accounts for both services
python main.py --service both --count 2 --output my_results.json
```

## Configuration

The tool can be configured via the `.env` file or environment variables:

### Browser Settings
- `HEADLESS`: Run browser in headless mode (true/false)
- `IMPLICIT_WAIT`: Selenium implicit wait time in seconds
- `PAGE_LOAD_TIMEOUT`: Page load timeout in seconds

### Rate Limiting
- `MIN_DELAY`: Minimum delay between actions (seconds)
- `MAX_DELAY`: Maximum delay between actions (seconds)

### Anti-Detection
- `USE_UNDETECTED_CHROME`: Use undetected-chromedriver (recommended)
- `ROTATE_USER_AGENTS`: Rotate user agents between requests
- `DISABLE_IMAGES`: Disable image loading for faster browsing

### Proxy Support
- `PROXY_HOST`: Proxy server host
- `PROXY_PORT`: Proxy server port

## Project Structure

```
account-registration-automation/
├── main.py                 # Main application entry point
├── config.py              # Configuration management
├── browser_manager.py     # Browser setup and management
├── account_generator.py   # Account data generation
├── gmail_registrar.py     # Gmail registration logic
├── cursor_registrar.py    # Cursor registration logic
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
└── README.md             # This file
```

## Important Notes

### Legal and Ethical Considerations

1. **Terms of Service**: Automated registration may violate platform ToS
2. **Rate Limiting**: Platforms implement rate limiting and bot detection
3. **Phone Verification**: Many services require phone verification
4. **Educational Use**: This tool is intended for learning and testing only

### Technical Limitations

1. **CAPTCHA**: Modern platforms use CAPTCHA to prevent automation
2. **Phone Verification**: Gmail requires phone verification for new accounts
3. **IP Blocking**: Excessive requests may result in IP blocking
4. **Dynamic Elements**: Web elements may change, breaking selectors

### Success Rate Expectations

- **Gmail**: Very low success rate due to strong anti-bot measures
- **Cursor**: May have higher success rate but still challenging
- **General**: Success rates vary based on platform defenses and timing

## Troubleshooting

### Common Issues

1. **ChromeDriver Issues**:
   ```bash
   # Update webdriver-manager
   pip install --upgrade webdriver-manager
   ```

2. **Element Not Found**:
   - Web pages may have changed
   - Check browser console for errors
   - Verify selectors are still valid

3. **Timeout Errors**:
   - Increase timeout values in config
   - Check internet connection
   - Try non-headless mode for debugging

4. **Phone Verification Required**:
   - This is expected for Gmail
   - Manual intervention required
   - Consider using services that don't require phone verification

### Debug Mode

Run without headless mode to see what's happening:

```bash
python main.py --count 1 --service cursor
```

Check the logs in `automation.log` for detailed information.

## Output

The tool generates several types of output:

1. **Console Output**: Real-time progress and results
2. **Log File**: Detailed logs in `automation.log`
3. **JSON Results**: Account data and results in `registered_accounts.json`

### Sample Output Structure

```json
{
  "success": true,
  "email": "john.doe123@gmail.com",
  "error": null,
  "step_reached": "account_created",
  "account_data": {
    "email": "john.doe123@gmail.com",
    "password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1(555)123-4567",
    "birth_date": "01/15/1990"
  },
  "service": "gmail",
  "attempt_number": 1
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes only. Use at your own risk and ensure compliance with applicable laws and terms of service.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `automation.log`
3. Create an issue with detailed information

---

**Remember**: Always respect platform terms of service and use automation responsibly!
