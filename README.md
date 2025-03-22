# Password Manager

## Overview
This is a secure password manager built using **Tkinter** for the GUI and **SQLite** for local storage. It allows users to generate strong passwords, store them securely using **AES encryption (Fernet)**, and retrieve them when needed.

## Features
- **Generate Strong Passwords** based on user-defined constraints (uppercase, lowercase, length, special characters).
- **Secure Storage** using AES encryption (Fernet) - passwords are never stored in plaintext.
- **Retrieve Passwords Securely** by clicking on the application name (password is decrypted on demand).
- **Search Functionality** to quickly find saved passwords.
- **Delete Passwords** when no longer needed.
- **User-friendly Interface** built with Tkinter.

## Technologies Used
- **Python** (Tkinter for GUI, SQLite for database)
- **cryptography.fernet** (AES encryption for password security)
- **SQLite3** (Local database for password storage)

## Installation
### Prerequisites
Ensure you have Python installed. Then, install the required dependencies:
```bash
pip install cryptography
```

## How to Use
1. **Run the Application**
   ```bash
   python password_manager.py
   ```
2. **Generate a Password**
   - Enter the application name.
   - Choose password criteria (uppercase, lowercase, special characters, length).
   - Click **Generate Password**.
   - The password will be displayed.
   - Click **Save Password** to securely store it.
3. **View Saved Passwords**
   - Navigate to the "View Saved Applications" tab.
   - Search for an application name if needed.
   - Click on an application name to decrypt and display the password.
4. **Delete a Password**
   - Select an application from the list.
   - Click **Delete Selected** to remove it from the database.

## Security Considerations
- **AES Encryption** ensures that stored passwords are secure.
- **No Plaintext Storage** - passwords are only decrypted when requested.
- **Unique Encryption Key** is generated and stored securely in a `secret.key` file.

## Future Enhancements
- Implement a master password for additional security.
- Add export/import functionality for backups.

## License
This project is open-source and available for modification and distribution.

