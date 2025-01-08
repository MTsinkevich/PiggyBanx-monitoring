# Website Monitoring System with Visual Comparison

This project is a cloud-based system that monitors a website for changes, including both HTML content and visual updates. It uses a serverless architecture powered by AWS services and Python to detect changes and send notifications for significant updates.

## Features
- Monitors changes in both website HTML content and visual layout.
- Uses **Selenium** to capture screenshots and **OpenCV** to detect visual differences.
- Detects significant updates using SHA-256 hashing for HTML and image comparison for visual changes.
- Sends email notifications via **Amazon SNS** for detected changes.
- Stores historical data (hash values and screenshots) in **Amazon S3**.
- Scheduled execution using **Amazon CloudWatch Events**.

## Technologies Used
- **AWS Services**:
  - AWS Lambda
  - Amazon S3
  - Amazon SNS
  - Amazon CloudWatch
- **Python Libraries**:
  - Selenium
  - OpenCV
  - BeautifulSoup
  - Requests
  - Boto3

## Architecture
1. **AWS Lambda**: Executes the monitoring logic.
2. **Amazon CloudWatch**: Triggers the Lambda function at scheduled intervals.
3. **Amazon S3**: Stores historical data for HTML hashes and screenshots.
4. **Amazon SNS**: Sends notifications via email.
5. **Selenium and OpenCV**: Used for capturing and comparing screenshots to detect visual changes.

## Setup Instructions

### Prerequisites
- AWS account
- Python 3.8 or later
- Dependencies: Selenium, OpenCV, BeautifulSoup, Requests, Boto3
- Custom Lambda Layer for Selenium and OpenCV

### Steps to Deploy

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/website-monitoring-system.git
   cd website-monitoring-system
   ```

2. **Set Up AWS Resources**:
   - Create an S3 bucket to store historical data.
   - Set up an SNS topic for notifications and subscribe your email.

3. **Create a Lambda Layer for Selenium and OpenCV**:
   - Download pre-built layers or package dependencies into a ZIP file.
   - Upload the layer to AWS Lambda and attach it to your function.

4. **Deploy the Lambda Function**:
   - Upload the `lambda_function.py` code to a new Lambda function.
   - Configure environment variables:
     - `S3_BUCKET`: Name of your S3 bucket.
     - `SNS_TOPIC_ARN`: ARN of your SNS topic.
     - `URL`: Website URL to monitor.
   - Attach the Lambda function to the custom layer created earlier.

5. **Set Up CloudWatch Rule**:
   - Create a CloudWatch rule with a schedule (e.g., `rate(10 minutes)`).
   - Set the rule to trigger your Lambda function.

6. **Test the Setup**:
   - Run the Lambda function manually and ensure it:
     - Captures screenshots
     - Compares HTML and visual content
     - Sends notifications for significant changes

## Usage
- To monitor a new website, update the `URL` environment variable in the Lambda function.
- Check the S3 bucket for stored hashes and screenshots.
- Review email notifications for updates.

## Code Highlights

### Screenshot Capture with Selenium
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def capture_screenshot(url, screenshot_path='/tmp/current_screenshot.png'):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1200x800')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

    return screenshot_path
```

### Visual Comparison with OpenCV
```python
import cv2

def compare_images(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    diff = cv2.absdiff(img1, img2)
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    diff_percentage = (cv2.countNonZero(thresh) / thresh.size) * 100

    return diff_percentage
```

## Future Enhancements
- Add multi-language support for detecting changes in localized content.
- Use AWS Rekognition for advanced image analysis.
- Implement machine learning models to classify types of changes.
- Develop a web-based dashboard to visualize monitoring results.


## Author
- Maksym Tsinkevich
# PiggyBanx-monitoring
