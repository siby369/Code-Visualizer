# Web Authentication Application

This project is a web application that provides user authentication functionality using a MongoDB database. It allows users to sign up and log in, ensuring that only registered users can access certain features.

## Project Structure

```
web-auth-app
├── src
│   ├── server.js            # Entry point of the application
│   ├── db
│   │   └── mongo.js         # MongoDB connection handling
│   ├── routes
│   │   ├── auth.js          # Authentication routes
│   ├── controllers
│   │   ├── authController.js # Logic for authentication
│   ├── models
│   │   └── user.js          # User model schema
│   └── views
│       ├── index.html       # Main landing page
│       ├── login.html       # User login form
│       └── signup.html      # User signup form
├── package.json              # npm configuration file
└── README.md                 # Project documentation
```

## Technologies Used

- Node.js
- Express.js
- MongoDB
- Mongoose

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd web-auth-app
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Set up MongoDB:**
   Ensure that MongoDB is running on your localhost. You can use MongoDB Compass to manage your database.

4. **Run the application:**
   ```
   node src/server.js
   ```

5. **Access the application:**
   Open your web browser and navigate to `http://localhost:3000` to view the application.

## Usage

- Click the "Login" button on the main page to access the login form.
- If you are a new user, click on the "Sign Up" link to create a new account.
- Enter your email and password to log in. If your email is not registered, you will be prompted to sign up first.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or features you would like to add.