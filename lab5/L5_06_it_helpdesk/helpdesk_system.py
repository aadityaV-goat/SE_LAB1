"""Manage helpdesk tickets with basic security checks and audit logging."""

import json
import os
import socket
from datetime import datetime

tickets = {}
ticket_counter = 100
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket and record its creation in the audit trail."""
    global ticket_counter

    if audit_trail is None:
        audit_trail = []

    priority = int(urgency)
    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    ticket_counter += 1
    tickets[ticket_counter] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }
    audit_trail.append(
        f"{user} raised #{ticket_counter} at {datetime.now()}"
    )
    return ticket_counter


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in tickets:
        return False

    tickets[ticket_id]["tech"] = technician
    return True


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in tickets:
        return False

    tickets[ticket_id]["notes"].append(note)
    return True


def close_ticket(ticket_id, password):
    """Close a ticket after verifying the administrator password."""
    if ticket_id not in tickets:
        return False

    if ADMIN_PASSWORD and password == ADMIN_PASSWORD:
        del tickets[ticket_id]
        return True

    return False


def unresolved_high_priority():
    """Return IDs of unassigned tickets with high priority."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Check whether a hostname resolves to an IP address."""
    if not hostname or hostname.startswith("-"):
        return 1

    try:
        socket.getaddrinfo(hostname, None)
        return 0
    except (socket.gaierror, OSError):
        return 1


def save_tickets(file="tickets.json"):
    """Save the current tickets as JSON."""
    with open(file, "w", encoding="utf-8") as ticket_file:
        json.dump(tickets, ticket_file, indent=2)


def main():
    """Run a small demonstration of the helpdesk system."""
    first_ticket = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    third_ticket = raise_ticket("joe", "vpn", "4")

    assign_ticket(first_ticket, "Tech-Kiran")
    add_note(first_ticket, "Called user")

    print("Unassigned high priority:", unresolved_high_priority())

    level = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ) or "3"

    try:
        raise_ticket("sana", "laptop", level)
    except ValueError:
        print("Invalid urgency. Please enter a number from 1 to 5.")
        return

    admin_password = os.environ.get("HELPDESK_ADMIN_PASSWORD", "")
    close_ticket(third_ticket, admin_password)
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
