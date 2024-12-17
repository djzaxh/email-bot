import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import threading

# Define a function that sends an email
def send_email(to_email, subject, body, from_email, password):
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS
        server.login(from_email, password)

        # Send the email
        server.send_message(msg)
        server.quit()

        print(f"Email sent to {to_email}")

    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

# Function to handle sending emails concurrently
def send_emails_concurrently(email_list, subject, body, from_email, password, number_of_sends):
    threads = []  # To store all the threads

    for index, row in email_list.iterrows():
        for _ in range(number_of_sends):
            to_email = row['email']

            # Create a thread for each email to be sent
            thread = threading.Thread(target=send_email, args=(to_email, subject, body, from_email, password))
            thread.start()

            threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    # Load your email list from a CSV file
    email_list = pd.read_csv('clients.csv')  # Ensure this file has an 'email' column

    # Get user inputs for email details
    subject = input("Enter the subject of the email: ")
    body = input("Enter the body of the email: ")
    number_of_sends = int(input("How many times would you like to send the email? "))

    # Your email and password
    from_email = "hello.noresponse.zach.got.you@gmail.com"
    password = "lmhq wdwt sosa tqmh"  # Use an App Password if 2FA is enabled

    # Send emails concurrently
    send_emails_concurrently(email_list, subject, body, from_email, password, number_of_sends)