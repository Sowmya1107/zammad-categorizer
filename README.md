# Zammad Ticket Categorizer

A Python-based ticket categorization pipeline that automatically retrieves incoming email tickets from Zammad, extracts the customer message, classifies the ticket, and updates the ticket category through the Zammad REST API.

## Workflow

```text
Incoming Email
      ↓
    Zammad
      ↓
  Zammad Ticket
      ↓
Retrieve Ticket through API
      ↓
Extract Customer Email
      ↓
Classification
      ↓
Determine Category
      ↓
Update Zammad Ticket
      ↓
Categorized Ticket
