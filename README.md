<h1>Designed to notify Dealer  before inspection deadlines for car registration.</h1>
</br>
<h3> Moto: helping avoid missed inspections and saving money.</h3>

</br>

<p> created it because of my experience as a part-time used car salesperson, where I noticed the challenge of managing cars from personal dealers efficiently.


 Sending an automated daily email reminder 5 days before a car’s registation date expires is a valuable feature for your Car Dealer Management app. Here’s how you can implement it:

 -> Send an email reminder once a day to the relevant person 5 days before the inspection expiry date of each car.
 
 -> Make sure your database has these fields for each car: 
             - car_id
            - owner_email
            - mr_number
            - inspection_date
-> Every day, run a script to:

-> Check today’s date.

-> Find cars with inspection_date = today + 3 days.

-> Send email notifications to the owner_email.

</p>

<p> Output email looks like this:

![image](https://github.com/user-attachments/assets/50cc17c9-02b2-48ea-8386-52f0109322cb)


</p>

<p> I used Brave account which gives 300 mail per day as free plan for the automation</p>
