<h1>Designed to Notify Car Registration to the Dealer Before Inspection Deadlines</h1>
<br/>

<h3>Moto: Helping Avoid Missed Inspections and Saving Money</h3>
<br/>

<p>
    I created this system based on my experience as a part-time used car salesperson, where I observed the recurring challenge of efficiently managing cars from personal dealers. Timely reminders can prevent costly penalties and missed inspections.
</p>

<h3>📌 Key Feature: Daily Automated Email Reminders</h3>

<p>
    This app sends automated email notifications 5 days before a car’s registration (inspection) date expires.
</p>

<ul>
    <li>Emails are sent once daily to the dealer/owner associated with the vehicle.</li>
    <li>The system checks inspection dates and triggers reminders exactly 5 days before expiry.</li>
</ul>

<h4>🔧 Required Database Fields:</h4>
<ul>
    <li><code>car_id</code></li>
    <li><code>owner_email</code></li>
    <li><code>mr_number</code></li>
    <li><code>inspection_date</code></li>
</ul>

<h4>⚙️ Daily Script Logic:</h4>
<ol>
    <li>Check today’s date.</li>
    <li>Query cars where <code>inspection_date = today + 5 days</code>.</li>
    <li>Send email notification to the respective <code>owner_email</code>.</li>
</ol>

<h4>📧 Sample Output Email:</h4>
<p>
    <img src="https://github.com/user-attachments/assets/a01ec5b9-adbe-458c-9330-3d4feaa88edf" alt="Sample Email Screenshot"/>
</p>

<h4>🛠 Tools & Services Used:</h4>
<ul>
    <li><strong>Email Service:</strong> Brave.com (Free Plan – 300 emails/day)</li>
    <li><strong>Automation:</strong> Windows Task Scheduler for daily execution</li>
    <li><strong>Logging:</strong> Log messages are stored in the <code>_internal</code> directory for each email sent</li>
</ul>

<h4>🛡️ Monitoring:</h4>
<p>
    If the script fails or doesn't run on a particular day, logs will help in quickly identifying and resolving issues.
</p>
