# Step 1: Define the Abstraction Interface
class Notification:
    def __init__(self, sender):
        self.sender = sender
    
    def send(self, message):
        pass

# Step 2: Create Refined Abstractions
class AlertNotification(Notification):
    def send(self, message):
        print("Alert Notification:")
        self.sender.send_message(f"Alert: {message}")

class ReminderNotification(Notification):
    def send(self, message):
        print("Reminder Notification:")
        self.sender.send_message(f"Reminder: {message}")

# Step 3: Define the Implementor Interface
class MessageSender:
    def send_message(self, message):
        pass

# Step 4: Create Concrete Implementors
class EmailSender(MessageSender):
    def send_message(self, message):
        print(f"Sending Email with message: {message}")

class SMSSender(MessageSender):
    def send_message(self, message):
        print(f"Sending SMS with message: {message}")

# Step 5: Bridge the Abstraction and Implementor
# Create instances of message senders
email_sender = EmailSender()
sms_sender = SMSSender()

# Create instances of notifications with different message senders
alert_notification_with_email = AlertNotification(email_sender)
reminder_notification_with_sms = ReminderNotification(sms_sender)

# Send notifications
alert_notification_with_email.send("Server is down!")  # Output: Alert Notification: Sending Email with message: Alert: Server is down!
reminder_notification_with_sms.send("Meeting at 10 AM")  # Output: Reminder Notification: Sending SMS with message: Reminder: Meeting at 10 AM
