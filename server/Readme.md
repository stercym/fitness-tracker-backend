# Fitness Tracker Backend

This **backend API** for the **Fitness Tracker** project is built with **Flask**, **Flask-SQLAlchemy**, and **Flask-Migrate**, and uses **SerializerMixin** to handle object-to-JSON serialization.  


## Its Features
- User registration and authentication 
- CRUD operations for **Goals**, **Exercises**, and **Exercise Logs**  
- **SerializerMixin** for clean JSON responses without recursion issues  
- SQLite database by default (configurable to MySQL)  
- Migration support with **Flask-Migrate**  
- RESTful endpoints to integrate with the React frontend  


## Technlogies used
- **Python 3.x**  
- **Flask**  
- **Flask-SQLAlchemy**  
- **Flask-Migrate**  
- **sqlalchemy-serializer (SerializerMixin)**  
- **SQLite** (default DB)  


## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/fitness-tracker.git
cd fitness-tracker/backend
