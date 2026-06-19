# CampusHub
### University Activity & Event Management System

CampusHub is a full-stack, web-based platform designed to centralize and streamline university event management, announcements, and campus communications. Built using the **MVC (Model-View-Controller)** architecture, it facilitates seamless interaction among students, instructors, and administrators.

---

## Features

###  Role-Based Access Control (RBAC)
*   **Students:** Browse available events, register/cancel registrations, view official announcements, and manage personal profiles.
*   **Instructors:** Create, update, and delete events, track student attendance, post announcements, and view lists of registered participants.
*   **Administrators:** Full system control, including user management, event moderation, log auditing, and system configuration.

###  Core Functionality
*   **Event Lifecycle Management:** Full CRUD operations for event coordination with real-time capacity and status tracking (Open, Full, Cancelled).
*   **Automated Notification Engine:** Integrated **SMTP** mail server to dispatch automated email confirmations upon registration, profile updates, or event modifications.
*   **Security & Session Control:** Enforced secure authentication with password hashing (SHA-256) and an automatic **5-minute inactivity session timeout**.
*   **Audit Logging & Analytics:** Administrative dashboard tracking user activity logs and generating participation statistics.
*   **Advanced Search:** Efficient querying capability for students to filter and discover campus activities.

---

## 🛠️ Tech Stack

*   **Backend:** Python (Flask Framework)
*   **Frontend:** HTML5, CSS3, JavaScript, Bootstrap / Tailwind CSS *(Responsive Design for Desktop, Tablet, & Mobile)*
*   **Database:** MySQL / PostgreSQL
*   **Protocols & Services:** RESTful APIs, SMTP (Email), HTTP/HTTPS with SSL/TLS encryption

---

##  Architecture & Design

The project is strictly compliant with the **Model-View-Controller (MVC)** software pattern to maximize maintainability, scalability, and separation of concerns.

*   **Authentication:** Managed via secure sessions and entry validation.
*   **Database Schema:** Normalization of relational tables mapping `User` (and subclasses), `Event`, `Registration`, `Announcement`, and `Notification` entities.

---

## Installation & Local Deployment

### Prerequisites
* Python 3.x
* MySQL Server

### Setup Steps
1. Clone the repository:
```bash
   git clone [https://github.com/s-ahmedabozaid-byte/CampusHub.git](https://github.com/s-ahmedabozaid-byte/CampusHub.git)
   cd CampusHub
