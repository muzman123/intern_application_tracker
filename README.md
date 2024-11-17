# Email Application Tracker

Track your job application rejections automatically by scanning your email inbox and storing rejection emails in DynamoDB.

## Overview

This application connects to your Gmail account using IMAP protocol to scan for rejection emails from job applications. When found, these rejections are stored in an AWS DynamoDB table for tracking and analysis.

## Prerequisites

- Python 3.6+
- AWS CLI configured with appropriate credentials
- Gmail account
- Gmail App Password (2FA must be enabled)
- AWS account with DynamoDB access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/email-application-tracker.git
cd email-application-tracker
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Gmail Setup

1. Enable 2-Factor Authentication in your Gmail account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security
   - App Passwords
   - Generate a new app password for "Mail"

### AWS Setup

1. Install AWS CLI:
```bash
pip install awscli
```

2. Configure AWS credentials:
```bash
aws configure
```

3. Create DynamoDB table:
```bash
aws dynamodb create-table \
    --table-name ApplicationRejections \
    --attribute-definitions AttributeName=EmailID,AttributeType=S \
    --key-schema AttributeName=EmailID,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5
```

## Usage

1. Open `main.py` and update the following variables:
```python
EMAIL = "your.email@gmail.com"
APP_PASSWORD = "your-gmail-app-password"
START_DATE = "2024-01-01"  # Format: YYYY-MM-DD
```

2. Run the application:
```bash
python main.py
```

## How It Works

1. The program connects to your Gmail inbox using IMAP
2. Searches for emails from the specified start date
3. Analyzes email content for rejection patterns
4. Stores identified rejections in DynamoDB with:
   - EmailID (Primary Key)
   - Sender
   - Date
   - Subject
   - Content Preview

## Important Notes

- **Security**: Never commit your email credentials to version control
- **Performance**: Searching further back in time will increase processing time
- **Rate Limits**: Be mindful of Gmail's IMAP rate limits
- **Costs**: DynamoDB usage may incur AWS charges

## Troubleshooting

### Common Issues

1. **Connection Error**
   - Verify your App Password is correct
   - Ensure 2FA is enabled
   - Check your internet connection

2. **AWS Errors**
   - Confirm AWS CLI is properly configured
   - Verify DynamoDB table exists
   - Check IAM permissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details
