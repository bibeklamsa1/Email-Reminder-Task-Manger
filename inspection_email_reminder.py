import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import sqlite3
import configparser
import os
# Step 1: Load config
config = configparser.ConfigParser()
config.read('config.txt')
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# Check if config file exists and is readable
if not config.read('config.txt'):
    raise FileNotFoundError("Missing 'config.txt' file or incorrect format")

try:
    DATABASE_PATH = config['DEFAULT']['DATABASE_PATH']
    SMTP_SERVER = config['DEFAULT']['SMTP_SERVER']
    SMTP_PORT = int(config['DEFAULT']['SMTP_PORT'])
    SMTP_USER = config['DEFAULT']['SMTP_USER']
    SMTP_PASS = config['DEFAULT']['SMTP_PASS']
    FROM_EMAIL = config['DEFAULT']['FROM_EMAIL']
    TO_EMAIL = config['DEFAULT']['TO_EMAIL']
except configparser.NoSectionError:
    raise configparser.NoSectionError("Missing 'DEFAULT' section in 'config.txt'")
except KeyError:
    raise KeyError("DATABASE_PATH key not found in 'config.txt'")
    






# Step 2: Prepare dynamic date range from today to today +5 days
today = datetime.today().date()
date_range = [today + timedelta(days=i) for i in range(6)]  # 6 days: today + next 5 days

# Check if Saturday and Sunday both fall in this date range
weekdays = [d.weekday() for d in date_range]  # Monday=0 ... Saturday=5, Sunday=6

if 5 in weekdays and 6 in weekdays:
    # Find Sunday index to get next Monday
    sunday_index = weekdays.index(6)
    monday = date_range[sunday_index] + timedelta(days=1)
    if monday not in date_range:
        date_range.append(monday)

# Convert to string list for SQL query
date_strs = [d.strftime('%Y-%m-%d') for d in sorted(set(date_range))]

# Step 3: Fetch upcoming inspections from DB for those dates
conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

placeholders = ', '.join(['?'] * len(date_strs))  # ?, ?, ... for SQL query
try:
    cursor.execute(f"""
    SELECT dealer, car_model, mr_number, inspection_date
    FROM cars
    WHERE inspection_date IN ({placeholders})
    order by inspection_date asc
    """, date_strs)

    cars = cursor.fetchall()
    conn.close()
except sqlite3.Error as e:
    conn.close()
    with open("email_log.txt", "a") as log_file:
        log_file.write(f"{datetime.now()} - Database error: {e}\n")
    raise sqlite3.Error(f"Database error: {e}")

# Step 4: If cars found, prepare and send email
if cars:
    subject = f"Upcoming Car Inspections - {len(cars)} car(s) due between {date_strs[0]} and {date_strs[-1]}"

    # Build HTML table rows
    table_rows = ""
    for dealer, car_model, mr_number, inspection_date in cars:
        table_rows += f"""
            <tr>
                <td>{dealer}</td>
                <td>{car_model}</td>
                <td>{mr_number}</td>
                <td>{inspection_date}</td>
                <td> {(datetime.strptime(inspection_date, '%Y-%m-%d').date() - today).days} days</td>
            </tr>
        """

    # HTML email body
    body = f"""
    <html>
        <body>
            <p>Hello Galleria Team,</p>
            <p>The following <strong>{len(cars)}</strong> car(s) have inspections due between <strong>{date_strs[0]}</strong> and <strong>{date_strs[-1]}</strong>:</p>

            <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
                <thead>
                    <tr>
                        <th>Dealer</th>
                        <th>Car Model</th>
                        <th>MR Number</th>
                        <th>Inspection Date</th>
                        <th>Days Remaining</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>

            <br>
            <p>Please make sure to get the car registration done on time.</p>

            <br>
            <p>Regards,</p>
            <p><strong>Car Dealer IT Support,<br>Bibek Lamsal (Ex. Software Engineer)</strong></p>

            <p style="font-size: small;">
                <i>Note: This is an automated email. Please do not reply.</i>
                <br><br>
                <i>Disclaimer: The information contained in this email is confidential and may be privileged. If you are not the intended recipient, please notify the sender and delete this email. Any unauthorized use, disclosure, or distribution of this email is prohibited.</i>
            </p>
        </body>
    </html>
    """

    # Prepare the email
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(body, "html"))

    # Send the email and log results
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

        with open("email_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Email sent to {TO_EMAIL} for {len(cars)} car(s) inspection reminder\n")
    except Exception as e:
        with open("email_log.txt", "a") as log_file:
            log_file.write(f"{datetime.now()} - Failed to send email to {TO_EMAIL}: {e}\n")
