import os
import re
import html
import requests


# =========================
# Zammad configuration
# =========================

ZAMMAD_URL = "http://localhost:3000"
ZAMMAD_TOKEN = os.environ["ZAMMAD_TOKEN"]

PROCESSED_FILE = "processed_tickets.txt"


# =========================
# Zammad headers
# =========================

def zammad_headers():
    return {
        "Authorization": f"Token token={ZAMMAD_TOKEN}",
        "Content-Type": "application/json"
    }


# =========================
# Get tickets
# =========================

def get_tickets():
    url = f"{ZAMMAD_URL}/api/v1/tickets"

    response = requests.get(
        url,
        headers=zammad_headers(),
        params={
            "limit": 100,
            "order_by": "created_at",
            "order_direction": "desc"
        }
    )

    response.raise_for_status()
    return response.json()


# =========================
# Get one ticket
# =========================

def get_ticket(ticket_id):
    url = f"{ZAMMAD_URL}/api/v1/tickets/{ticket_id}"

    response = requests.get(
        url,
        headers=zammad_headers()
    )

    response.raise_for_status()
    return response.json()


# =========================
# Get ticket articles
# =========================

def get_articles(ticket_id):
    url = f"{ZAMMAD_URL}/api/v1/ticket_articles/by_ticket/{ticket_id}"

    response = requests.get(
        url,
        headers=zammad_headers()
    )

    response.raise_for_status()
    return response.json()


# =========================
# Clean HTML from email
# =========================

def clean_html(text):
    text = html.unescape(text)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Clean whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================
# Extract customer email
# =========================

def extract_customer_email(articles):

    customer_articles = [
        article
        for article in articles
        if article.get("sender") == "Customer"
        and article.get("internal") is False
    ]

    if not customer_articles:
        raise ValueError("No customer article found")

    # Use latest customer article
    article = customer_articles[-1]

    body = article.get("body", "")

    return clean_html(body)


# =========================
# Classify email
# =========================

def classify(text):

    text = text.lower()

    # Network problems
    if any(word in text for word in [
        "wifi",
        "wi-fi",
        "internet",
        "network",
        "connection",
        "connect"
    ]):
        return "network"

    # Software problems
    if any(word in text for word in [
        "software",
        "application",
        "program",
        "crash",
        "error"
    ]):
        return "software"

    # Account problems
    if any(word in text for word in [
        "password",
        "login",
        "account",
        "access"
    ]):
        return "account"

    return "other"


# =========================
# Update Zammad ticket
# =========================

def update_ticket(ticket_id, category):

    url = f"{ZAMMAD_URL}/api/v1/tickets/{ticket_id}"

    payload = {
        "category": category
    }

    response = requests.put(
        url,
        headers=zammad_headers(),
        json=payload
    )

    response.raise_for_status()

    return response.json()


# =========================
# Processed ticket handling
# =========================

def load_processed_tickets():

    if not os.path.exists(PROCESSED_FILE):
        return set()

    with open(PROCESSED_FILE, "r") as file:
        return {
            line.strip()
            for line in file
            if line.strip()
        }


def save_processed_ticket(ticket_id):

    with open(PROCESSED_FILE, "a") as file:
        file.write(f"{ticket_id}\n")


# =========================
# Find new ticket
# =========================

def get_new_ticket():

    tickets = get_tickets()
    processed = load_processed_tickets()

    for ticket in tickets:

        ticket_id = str(ticket["id"])

        if ticket_id not in processed:
            return ticket_id

    return None


# =========================
# Main
# =========================

def main():

    print("Checking Zammad for new tickets...")

    ticket_id = get_new_ticket()

    if ticket_id is None:
        print("No new tickets to process.")
        return

    print(f"Processing ticket #{ticket_id}...")

    # Get ticket
    ticket = get_ticket(ticket_id)

    print(f"Ticket title: {ticket.get('title')}")

    # Get articles
    articles = get_articles(ticket_id)

    # Extract customer's message
    text = extract_customer_email(articles)

    print(f"Customer message: {text}")

    # Classify
    category = classify(text)

    print(f"Category: {category}")

    # Update Zammad
    update_ticket(ticket_id, category)

    print(f"Ticket #{ticket_id} updated successfully.")

    # Remember that this ticket was processed
    save_processed_ticket(ticket_id)

    print("Done.")


if __name__ == "__main__":
    main()
