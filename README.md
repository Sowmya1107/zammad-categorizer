# Zammad Ticket Categorizer

A Python application that automatically retrieves tickets from a local Zammad instance, extracts the customer message, categorizes the ticket, and updates the ticket category through the Zammad REST API.

## Project Structure

    zammad-categorizer/
    ├── categorizer.py
    ├── README.md
    ├── .gitignore
    └── processed_tickets.txt

## Technologies

- Python 3
- Zammad
- Zammad REST API
- Ubuntu / WSL
- Git
- GitHub
- Python Requests

## How the System Works

    Customer
       |
       | Email
       v
    Zammad
       |
       | REST API
       v
    Python Categorizer
       |
       | Retrieve ticket
       v
    Retrieve ticket articles
       |
       v
    Extract customer message
       |
       v
    Categorize ticket
       |
       v
    Update Zammad category
       |
       v
    Store processed ticket ID

## 1. Ubuntu / WSL Setup

Check Python:

    python3 --version

Check Python location:

    which python3

Check Ubuntu:

    lsb_release -a

## 2. Zammad Setup

Zammad is running locally at:

    http://localhost:3000

Open Zammad in the browser:

    http://localhost:3000

Check Zammad status:

    sudo systemctl status zammad

Start Zammad:

    sudo systemctl start zammad

Stop Zammad:

    sudo systemctl stop zammad

Restart Zammad:

    sudo systemctl restart zammad

Test Zammad:

    sudo zammad run rails r "puts 'Zammad is working'"

## 3. Zammad Email Setup

Zammad can receive emails and automatically create tickets.

In Zammad go to:

    Admin
    -> Channels
    -> Email

Configure the email account.

For Gmail, an App Password can be used when required.

The workflow is:

    Gmail
      |
      v
    Zammad Email Channel
      |
      v
    Zammad Ticket
      |
      v
    Python Categorizer

Do not store Gmail passwords or App Passwords in the project.

## 4. Zammad API Setup

Zammad API base URL:

    http://localhost:3000/api/v1/

Test the API:

    curl http://localhost:3000/api/v1/tickets

## 5. Create Zammad API Token

In Zammad:

    Profile
    -> Access Tokens
    -> Create Access Token

Copy the generated API token.

Test authentication:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/users/me

Replace:

    YOUR_API_TOKEN

with the actual token.

Never commit the real API token to GitHub.

## 6. Find a Zammad Ticket ID

Zammad has a ticket number and an internal ticket ID.

Example:

    Ticket number: 45008
    Ticket ID:     8

Find the ticket ID:

    sudo zammad run rails r "t=Ticket.find_by(number: '45008'); puts({id: t&.id, number: t&.number, title: t&.title}.inspect)"

Example result:

    {:id=>8, :number=>"45008", :title=>"Test Email"}

## 7. Retrieve a Ticket

For ticket ID 8:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/tickets/8 | python3 -m json.tool

## 8. Retrieve Ticket Articles

Ticket articles contain the customer message.

For ticket ID 8:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/ticket_articles/by_ticket/8 | python3 -m json.tool

## 9. Python Setup

Check Python:

    python3 --version

Check pip:

    python3 -m pip --version

Install Requests:

    python3 -m pip install requests

Test Requests:

    python3 -c "import requests; print(requests.__version__)"

If pip or venv cannot be installed because of Ubuntu Python package conflicts, check:

    apt-cache policy python3 python3.12 python3.14 python3-pip python3-venv

## 10. Clone the Project

Clone the GitHub repository:

    git clone https://github.com/Sowmya1107/zammad-categorizer.git

Enter the project:

    cd zammad-categorizer

Check files:

    ls -la

## 11. Configure API Token

Set the Zammad API token as an environment variable:

    export ZAMMAD_API_TOKEN="YOUR_API_TOKEN"

Check that it is set:

    echo $ZAMMAD_API_TOKEN

Do not commit the actual token.

## 12. Run the Categorizer

Go to the project:

    cd ~/zammad-categorizer

Run the application:

    python3 categorizer.py

The application:

1. Retrieves tickets from Zammad.
2. Retrieves ticket articles.
3. Extracts the customer message.
4. Categorizes the message.
5. Updates the ticket category.
6. Records the processed ticket.

## 13. Ticket Categories

The application currently supports:

    account
    software
    technical
    other

Example software ticket:

    My Visual Studio is not working.

Result:

    software

Example technical ticket:

    My laptop cannot connect to Wi-Fi.

Result:

    technical

Example account ticket:

    I cannot access my account.

Result:

    account

If no classification rule matches:

    other

## 14. Processed Tickets

Processed ticket IDs are stored in:

    processed_tickets.txt

Example:

    5
    6
    7
    8

This prevents the same ticket from being processed repeatedly.

The file is excluded from Git.

## 15. Test Software Ticket

Create a ticket in Zammad:

    Title:
    Software is not working

    Message:
    Hello, my Visual Studio is not working.

Run:

    python3 categorizer.py

Expected category:

    software

## 16. Test Technical Ticket

Create:

    Title:
    Wi-Fi Problem

    Message:
    My laptop cannot connect to Wi-Fi.

Run:

    python3 categorizer.py

Expected category:

    technical

## 17. Test Account Ticket

Create:

    Title:
    Account Problem

    Message:
    I cannot access my account.

Run:

    python3 categorizer.py

Expected category:

    account

## 18. Test Other Ticket

Create:

    Title:
    Test Email

    Message:
    Hello, this is only a test message.

Run:

    python3 categorizer.py

Expected category:

    other

## 19. Verify the Ticket in Zammad

Open:

    http://localhost:3000

Open the ticket and check the category.

## 20. Verify the Ticket Using the API

For ticket ID 8:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/tickets/8 | python3 -m json.tool

Look for:

    "category": "software"

or:

    "category": "technical"

or:

    "category": "account"

or:

    "category": "other"

## 21. Check Ticket State

The API also returns the ticket state.

Check:

    state_id
    category

Example:

    "state_id": 4

A ticket can be successfully categorized even if it is closed.

## 22. Troubleshooting Zammad

Check status:

    sudo systemctl status zammad

Restart:

    sudo systemctl restart zammad

Test:

    sudo zammad run rails r "puts 'Zammad is working'"

Open:

    http://localhost:3000

## 23. Troubleshooting API

Test authentication:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/users/me

Get ticket:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/tickets/8 | python3 -m json.tool

Get articles:

    curl -H "Authorization: Token token=YOUR_API_TOKEN" http://localhost:3000/api/v1/ticket_articles/by_ticket/8 | python3 -m json.tool

## 24. Troubleshooting Categorization

If the category is:

    other

check the classification rules in:

    categorizer.py

Make sure the customer message contains keywords handled by the categorization logic.

For example, software-related messages may contain:

    software
    application
    program
    Visual Studio
    IDE

Technical messages may contain:

    Wi-Fi
    network
    internet
    connection
    laptop
    computer
    hardware
    device

Account messages may contain:

    account
    login
    password
    username
