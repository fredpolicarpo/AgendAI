# Product Specification: AgendAI
 - **Version:** 1.0 
 - **Date:** May 17, 2025 
 - **Author:** Frederico Policarpo Martins Boaventura 

## 1. Introduction

AgendAI is an intelligent virtual assistant, based on chatbot technology, designed to simplify and automate the appointment scheduling process for independent professionals and their clients. Using generative artificial intelligence for natural communication and integrations with Google tools (Calendar, Sheets, Gmail), AgendAI aims to optimize time management, reduce no-shows, and improve the scheduling experience for both parties. Interaction with AgendAI can be conducted through both text and voice.

## 2. Overview and Problem

Independent professionals (doctors, lawyers, consultants, therapists, etc.) often spend considerable time on manual schedule management, handling appointment requests, confirmations, cancellations, and rescheduling. This process can be inefficient, error-prone, and consume time that could be devoted to their core activity. For clients, the traditional scheduling process can sometimes be time-consuming and inflexible.

AgendAI solves these problems by offering a centralized and automated platform that:

* Allows clients to request and manage their appointments autonomously via chatbot.
* Enables professionals to configure their availability and manage appointment requests through a conversational interface.
* Automates notifications, reminders, and the appointment confirmation flow, including cancellation policies.
* Records all interactions for future reference and reporting.

## 3. Objectives

* **For Professionals:**
    * Reduce time spent on manual appointment management.
    * Minimize scheduling errors.
    * Decrease the rate of no-shows through reminders and confirmations.
    * Offer a clear and updated view of their schedule, with visual distinction for appointment status.
    * Allow configuration of cancellation policies (time limits and fees).
    * Improve operational efficiency.
* **For Clients (Requesters):**
    * Provide a quick, easy scheduling process available 24/7.
    * Be clearly informed about the professional's cancellation policies.
    * Offer flexibility to manage their own appointments (cancel, request rescheduling) aware of the conditions.
    * Improve the overall experience of interaction with the professional/service.
* **General Product Objectives:**
    * Be a reference solution for intelligent scheduling via chatbot.
    * Ensure high accuracy in voice recognition and natural language processing.
    * Maintain a formal, polite, friendly tone with light enthusiasm in all interactions.

## 4. Target Audience

* **Independent Professionals and Small Businesses:** Lawyers, doctors, dentists, therapists, consultants, coaches, personal trainers, beauty salons, studios, etc., who manage their own appointments or have a small team for this purpose.
* **Clients/Patients/Requesters:** Individuals seeking to schedule services with the professionals above.

## 5. Functional Requirements (User Stories and Features)

All interactions should be possible via **text and voice**. The chatbot's tone of voice will be **formal, polite, friendly, and with light enthusiasm**.

### P1: Essential MVP – The Complete Cycle via Chatbot

1.  **Initial Availability Configuration by the Professional:**
    * **User Story (Professional):** "As a professional, I want to be able to inform AgendAI of my standard service days and hours, including breaks, so that the system knows when I am available."
    * **Feature:** The professional, via chat (text/voice), informs the AgendAI of their service days, times, and breaks. The system configures this as "Busy Time" in Google Calendar, with text in the description indicating "Blocked: Not Available" and a customized color (e.g., dark gray).
        * **Dialogue Example:**
            * **Professional:** "I'd like to set my service hours."
            * **AgendAI:** "Great! I'll help you configure your availability. What days of the week do you provide service?"
            * **Professional:** "Monday to Friday."
            * **AgendAI:** "Perfect. And what are your service hours on these days?"
            * **Professional:** "From 9 AM to 6 PM."
            * **AgendAI:** "I understand. Do you have any breaks or lunch hour during the day?"
            * **Professional:** "Yes, from 12 PM to 1 PM for lunch."
            * **AgendAI:** "Got it. Let me recap: You are available Monday to Friday, from 9 AM to 12 PM and from 1 PM to 6 PM. Is this information correct?"
            * **Professional:** "Correct."
            * **AgendAI:** "Great! Your availability has been configured. ✨"
    * **Acceptance:** The professional can define their availability through a guided dialogue; the chatbot confirms the configuration; the professional's Google Calendar reflects this base availability.

2.  **Cancellation Policy Configuration by the Professional:**
    * **User Story (Professional):** "As a professional, I want to be able to define a time limit for free cancellation (e.g., 2 hours before) and the amount of a cancellation fee if the client cancels after this limit or doesn't show up, so that AgendAI can inform and apply this policy."
    * **Feature:** The professional, via chat (text/voice), defines the advance time limit for free cancellation (e.g., "2 hours before", "24 hours before") and the cancellation fee amount (e.g., "$50.00"). AgendAI stores this policy.
        * **Dialogue Example:**
            * **Professional:** "I want to set my cancellation policy."
            * **AgendAI:** "I'll help you with that. How many hours in advance should a client cancel to avoid any fees?"
            * **Professional:** "At least 24 hours before."
            * **AgendAI:** "Understood. And what fee should be applied for cancellations made with less than 24 hours' notice or no-shows?"
            * **Professional:** "$50.00"
            * **AgendAI:** "Let me confirm: Clients need to cancel at least 24 hours in advance to avoid a fee. Cancellations with less notice or no-shows will incur a $50.00 fee. Is this correct?"
            * **Professional:** "Correct."
    * **Acceptance:** The professional can define the time limit for free cancellation and the fee amount; the chatbot confirms the policy configuration.

3.  **Pre-Appointment Request by Client:**
    * **User Story (Client):** "As a client, I want to be able to inform the chatbot of my general day or period preferences (morning, afternoon, evening) before seeing specific times, so that the options are more relevant to me, and I want to be informed about the cancellation policy when scheduling."
    * **Feature:**
        1.  The client interacts with the chatbot (text/voice) to initiate a scheduling (e.g., "I'd like to schedule an appointment").
        2.  The chatbot asks about general day/period preferences (e.g., "Do you have a preference for a specific day or period? For example, mornings, afternoons, evenings?").
        3.  The client indicates preferences (e.g., "Preferably on Monday afternoon").
        4.  The chatbot checks available slots (based on the professional's configured availability and existing appointments) and offers specific options matching the preferences.
        5.  Before presenting options, the chatbot informs about the cancellation policy: "Please note that [Professional's Name] has a cancellation policy: cancellations must be made at least [time limit] in advance to avoid a [fee amount] fee."
        6.  The client chooses a time.
        7.  The chatbot creates a pre-appointment in the professional's Google Calendar.
            * **Event Title:** "[Pending] - [Professional Name] Appointment - [Client Name]"
            * **Description:** Contains all relevant information: client name, contact, specific service if applicable.
            * **Event Color:** Orange.
        9.  The chatbot informs the client: "Excellent! Your request for [chosen date/time] has been sent to [Professional's Name] and awaits confirmation. We'll notify you as soon as we have a response, okay?"
    * **Acceptance:** The client can provide general day/period preferences; the chatbot presents valid preference options; the chatbot offers filtered specific times; the client is informed about the cancellation policy before the pre-appointment is created; an event is created in the professional's Google Calendar with the title "[Pending] - Event Name", orange color; the request is registered as a pre-appointment.

4.  **Notification and Pre-Appointment Management by the Professional:**
    * **User Story (Professional):** "As a professional, I want to be notified when a client requests an appointment and be able to confirm or reject the request through the chatbot."
    * **Feature:** The professional receives a notification about the pre-appointment request via chatbot. They can confirm or reject the request with a simple interaction. Both the confirmation and rejection can include an optional message to the client.
    * **Acceptance:** The professional is notified; can confirm or reject the request; the action is recorded.

5.  **Schedule Update and Result Notification to the Client:**
    * **User Story (Client):** "As a client, I want to be notified by AgendAI if my appointment request was confirmed or rejected by the professional."
    * **Feature:**
        1.  If CONFIRMED by the professional:
            * The chatbot notifies the client: "Good news! [Professional's Name] confirmed your appointment for [date/time]. We look forward to seeing you!"
            * The Google Calendar event is updated:
                * **Title:** From "[Pending]" to "[Confirmed]"
                * **Event Color:** Green
        2.  If REJECTED by the professional:
            * The chatbot notifies the client: "Unfortunately, [Professional's Name] was unable to confirm your appointment for [date/time]. [Optional message from professional]. Would you like to try an alternative date/time?"
            * The event is deleted from the Google Calendar.
            * The chatbot can assist in finding an alternative (returning to step 3).
    * **Acceptance:** The client is notified of the confirmation or rejection; the Google Calendar is updated accordingly; in case of rejection, the client can request an alternative.

6.  **Simple Schedule Query by the Professional:**
    * **User Story (Professional):** "As a professional, I want to be able to quickly check my upcoming appointments through the chatbot to stay organized."
    * **Feature:** The professional can ask the chatbot about their schedule for a specific day, week, or time period. The chatbot consults Google Calendar and presents the information in a clear, organized manner.
    * **Acceptance:** The professional can query their schedule; the chatbot provides an accurate and organized view of appointments.

7.  **Time Blocking/Unblocking by the Professional:**
    * **User Story (Professional):** "As a professional, I want to be able to temporarily block specific times or days when I won't be available, even if they are within my standard service hours."
    * **Feature:** The professional informs the chatbot about specific times they want to block (e.g., "I will be unavailable next Monday from 2 PM to 4 PM"). The chatbot creates a blocking event in Google Calendar (with title "Blocked by [Professional's Name]", dark gray color). The professional can also request to unblock previously blocked times.
    * **Acceptance:** The professional can block/unblock times; Google Calendar reflects the changes.

8.  **Cancellation of Confirmed Appointment by the Client (with Cancellation Policy):**
    * **User Story (Client):** "As a client, I want to be able to cancel a confirmed appointment through the chatbot, being informed about possible fees if the cancellation is outside the time limit."
    * **Feature:**
        1.  The client informs the chatbot of their desire to cancel an appointment.
        2.  The chatbot locates the confirmed appointment.
        3.  The chatbot calculates whether the cancellation is within or outside the free cancellation period.
            * If within the period: "You're canceling with [time] notice, which is within the free cancellation period. There will be no fee. Would you like to proceed with the cancellation?"
            * If outside the period: "You're canceling with [time] notice, which is less than the required [time limit] notice. According to [Professional's Name]'s policy, a cancellation fee of [fee amount] will apply. Would you like to proceed with the cancellation? [Yes, proceed with cancellation] [No, keep appointment]"
        4.  The client decides whether to proceed:
            * If the client chooses "Yes, proceed with cancellation": The appointment is canceled, the Google Calendar event is deleted (or marked as "Canceled" and colored red), and if applicable, the cancellation fee is registered in a Google Sheet for the professional's records. The chatbot confirms: "Your appointment for [date/time] has been canceled. [If applicable: A cancellation fee of (fee amount) has been registered in accordance with the cancellation policy.]"
            * If the client chooses "No, keep appointment": The appointment is maintained and the chatbot confirms: "Understood. Your appointment for [date/time] is maintained."
    * **Acceptance:** The client can request cancellation; if the cancellation is outside the time limit, the client is informed about the fee and can decide whether to proceed; Google Calendar is updated according to the decision; the professional is notified; the possible fee charge is registered in Google Sheets.

9.  **Cancellation Notification (made by the Client) to the Professional:**
    * **User Story (Professional):** "As a professional, I want to be immediately notified by AgendAI when a client cancels an appointment, including if a cancellation fee is applicable."
    * **Feature:** The chatbot notifies the professional about the cancellation made by the client, indicating whether the cancellation occurred within or outside the time limit and if the cancellation fee is applicable.
    * **Acceptance:** The professional receives the cancellation notification in a timely manner with information about the cancellation policy.

### P3: Advanced Features – Keeping the Chatbot as the Sole Interface

10. **Automatic Reminders and Attendance Confirmation Request (Client and Professional):**
    * **User Story (Professional):** "As a professional, I want to be able to configure AgendAI to send automatic reminders to clients X hours/days before the appointment, requesting attendance confirmation and reminding them of the cancellation policy."
    * **User Story (Client):** "As a client, I want to receive a reminder of my appointment, be able to confirm my attendance or indicate the need to reschedule/cancel, and be reminded of the cancellation policy."
    * **Feature:** The professional configures the reminder policy via chat. AgendAI automatically sends messages (via chatbot) to clients before appointments (only for confirmed ones - green), requesting confirmation. **The reminder message will include a note about the cancellation policy:** "Hello, [Client's Name]! Just reminding you of your appointment with [Professional's Name] on [date] at [time]. Do you confirm your attendance? [Yes, I confirm] [I Need to Reschedule/Cancel]. Remember that cancellations must be made with at least [configured time limit] notice to avoid the [configured fee amount] fee."
        The client's response is recorded and may notify the professional. (The cancellation/rescheduling interaction here will follow the cancellation policy).
    * **Acceptance:** Reminders are sent as configured for confirmed events, including the note about the cancellation policy; clients can confirm/indicate absence; the system records the response.

11. **Basic Reports for the Professional (based on GSheets):**
    * **User Story (Professional):** "As a professional, I want to be able to request simple reports from AgendAI, such as the number of confirmed appointments in a week, the cancellation rate in the last month, and the total amount of cancellation fees applied."
    * **Feature:** The professional requests basic reports via chat (text/voice). AgendAI consults the data logged in Google Sheets (including cancellation fee records) and presents the summaries.
    * **Acceptance:** The professional can obtain basic statistical data about their appointments and fees.

## 6. Non-Functional Requirements

* **Usability:** Intuitive conversational interface; quick responses; clarity; consistent tone of voice.
* **Performance:**
    * Chatbot response time under 5 seconds for most interactions.
    * Capacity for 150 active clients per month, with an average of 12 appointments per day.
    * Efficient voice command processing.
* **Reliability:**
    * High accuracy in scheduling and availability management (avoiding overbooking or errors).
    * System availability of 99.5%.
    * Logs of all important transactions for auditing and recovery.
* **Security:** Data protection (GDPR/LGPD); secure authentication for the professional.
* **Maintainability:** Documented and modular code; easy updates.
* **Accessibility:** Support for text and voice; (Future) WCAG.
* **STT/NLP Accuracy:** High accuracy in Brazilian Portuguese; understanding of intentions; handling ambiguities.

## 7. Integrations

* **Google Calendar:** Reading availability; CRUD of events (titles, participants, colors).
* **Google Sheets:** Logging (requests, confirmations, cancellations, configurations, errors, applicable fees). Source for reports.
* **Google Cloud Speech-to-Text (STT):** Voice-to-text conversion.
* **(Optional/Future) Google Cloud Text-to-Speech (TTS):** Voice responses from the chatbot.
* **(Optional/Future) Gmail API:** Complementary email notifications.
* **Chatbot Platform:** To be defined (Dialogflow, etc.).

## 8. Technical Considerations

* **Generative AI/NLP Engine:** Flexibility and understanding of intentions.
* **Conversation State Management:** Maintaining context.
* **Professional Authentication:** Secure mechanism.
* **Chatbot Interface:** Support for text, STT, quick response buttons.
* **Availability Logic and Cancellation Policy:** Robust for cross-referencing data and applying rules.
* **Scalability:** Architecture designed to support a volume of 150 active clients/month and an average of 12 appointments/day, ensuring a response time of up to 5s.
* **Google Calendar API:** Use of features for event management.

## 9. Success Metrics

* **Adoption:** Number of active professionals; Number of clients using.
* **Engagement:** Number of appointments/period; Frequency of use by professionals.
* **Efficiency:** Reduction in average scheduling time; Chatbot success rate; Voice usage rate.
* **Satisfaction:** Qualitative feedback; Reduction of no-shows; Cancellation rate within/outside the time limit.
* **Technical:** STT/NLP accuracy; Uptime according to 99.5% SLA; System response time within SLA.

## 10. Future Scope / Out of Scope (Initial MVP)

* Integrated payments (including automatic charging of cancellation fees).
* Management of multiple professionals/locations.
* Integration with other calendars.
* Advanced reports.
* Advanced chatbot customization.
* Voice responses (TTS).
* Marketing campaign.
* Dedicated mobile app.