# Star Attendance App - Backend

A Django REST Framework backend for managing attendance tracking using QR codes and manual entry. Built for committee-based organizations with role-based access control.

## 🌟 Features

- **JWT Authentication**: Secure token-based authentication using SimpleJWT
- **QR Code Attendance**: Generate encrypted, time-limited QR codes for contactless attendance logging
- **Manual Attendance Entry**: Admins can manually log attendance using member identifiers
- **Committee-Based Access Control**: Users are organized by committees with appropriate permissions
- **Session Management**: Create and manage committee sessions with time-based validation
- **Attendance History**: Track and view attendance records with status (present, late, absent)
- **Role-Based Permissions**:  Separate admin and member roles with different access levels
- **Automated Status Detection**: Automatic late status assignment based on configurable time thresholds

## 📋 Database Schema

The application uses three main models:

### User
- Custom user model with committee assignment
- Roles: `admin` | `member`
- Committee types: `front` | `back` | `mobile` | `ai` | etc.
- Fields: username, email, phone_number, password, role, committee

### Session
- Committee-specific sessions with time bounds
- Fields: name, committee, start_time, end_time, location, instructor, manual_code
- Manual codes for offline attendance tracking

### AttendanceRecord
- Tracks member attendance for each session
- Status types: `present` | `late` | `absent`
- Automatic timestamp on check-in
- Unique constraint on (user, session) to prevent duplicate records

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Django 6.0
- SQLite (default) or your preferred database

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kiro0oz/Star_AttendanceApp_Backend.git
   cd Star_AttendanceApp_Backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install django djangorestframework djangorestframework-simplejwt cryptography
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.  Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Endpoints

- `POST /api/auth/token/` - Obtain access and refresh tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/token/logout/` - Logout (blacklist refresh token)

**Token Lifetime:**
- Access Token: 60 minutes
- Refresh Token:  7 days

## 📡 API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - User login
- `POST /api/auth/token/` - Obtain JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token

### Sessions (`/api/sessions/`)
- `GET /api/sessions/` - List all sessions (filtered by user's committee)
- `POST /api/sessions/` - Create new session (admin only)
- `GET /api/sessions/{id}/` - Get session details
- `PUT/PATCH /api/sessions/{id}/` - Update session (admin only)
- `DELETE /api/sessions/{id}/` - Delete session (admin only)

### Attendance (`/api/attendance/`)
- `POST /api/attendance/generate-qr/{session_id}/` - Generate encrypted QR code for attendance
- `POST /api/attendance/scan/` - Scan QR code or manual entry to log attendance (admin only)
- `GET /api/attendance/history/` - View member's attendance history

## 🎯 QR Code Workflow

### For Members (Generating QR Code):

1. **Member authenticates** and requests QR code for a specific session
2. **Validates**:  
   - Session exists
   - Member belongs to session's committee
   - Session has started but not ended
3. **Returns**:  Encrypted QR data with 90-second lifetime

**Endpoint**: `POST /api/attendance/generate-qr/{session_id}/`

**Response**:
```json
{
  "encrypted_qr_data": "encrypted_string_here",
  "qr_lifetime_seconds": 90,
  "session_manual_code": "ABC123"
}
```

### For Admins (Scanning QR Code):

1. **Admin scans** the member's QR code or enters manual data
2. **Validates**: 
   - QR data is valid and not expired
   - QR belongs to current session
   - Member belongs to session's committee
3. **Determines status**:
   - `present`: Checked in within 30 minutes of session start
   - `late`: Checked in after 30 minutes
4. **Records** attendance (or updates if already exists)

**Endpoint**: `POST /api/attendance/scan/`

**Request** (QR Code):
```json
{
  "encrypted_data": "encrypted_qr_data",
  "session_id": 1
}
```

**Request** (Manual Entry):
```json
{
  "manual_code": "ABC123",
  "member_identifier": "username_or_phone",
  "session_id": 1
}
```

## 🛡️ Permissions

### Custom Permissions

- **IsCommitteeAdmin**:  Restricts access to users with `admin` role in the same committee
- **IsAuthenticated**: Requires valid JWT token

### Access Control

- **Members** can: 
  - Generate QR codes for their sessions
  - View their attendance history
  - View sessions in their committee

- **Admins** can: 
  - All member permissions
  - Create, update, delete sessions
  - Scan QR codes and log attendance
  - Manually enter attendance records

## 🏗️ Project Structure

```
Star_AttendanceApp_Backend/
├── Auth/                          # Custom user authentication app
│   ├── models.py                  # Custom User model
│   ├── views.py                   # Auth views
│   ├── permissions.py             # Custom permissions
│   └── urls.py                    # Auth routes
├── attendance/                    # Attendance management app
│   ├── models. py                  # AttendanceRecord model
│   ├── views.py                   # QR generation & scanning views
│   ├── utils.py                   # Encryption/decryption utilities
│   ├── serializers.py             # DRF serializers
│   └── urls.py                    # Attendance routes
├── committee_sessions/            # Session management app
│   ├── models.py                  # Session model
│   ├── views. py                   # Session CRUD views
│   └── urls.py                    # Session routes
├── star_attendanceApp_core/       # Django project settings
│   ├── settings.py                # Project configuration
│   ├── urls.py                    # Root URL configuration
│   └── wsgi.py                    # WSGI configuration
├── manage.py                      # Django management script
├── db.sqlite3                     # SQLite database
└── ERD.mmd                        # Entity Relationship Diagram
```

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication with automatic expiration
- **Encrypted QR Codes**: QR data encrypted using Fernet symmetric encryption
- **Time-Limited QR Codes**: QR codes expire after 90 seconds
- **Committee Isolation**: Users can only access data from their assigned committee
- **Role-Based Access**: Separate permissions for admin and member roles
- **Token Blacklisting**: Logout functionality blacklists refresh tokens


## 📝 Development Notes

- **QR Code Generation**: Uses Fernet encryption with base64 encoding
- **Time Validation**: All times are stored in UTC
- **Unique Constraints**: One attendance record per user per session
- **Update or Create**: Re-scanning updates existing attendance record

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is private.  Please contact the repository owner for licensing information.

## 👤 Author

**Kiro0oz**
- GitHub: [@Kiro0oz](https://github.com/Kiro0oz)

