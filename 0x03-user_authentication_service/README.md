# User Authentication Service

## Description

This is a user authentication service that provides secure authentication and authorization functionalities for your application.

## Features

- User registration
- User login
- Password hashing and salting
- JSON Web Token (JWT) based authentication
- Role-based access control (RBAC)
- Password reset functionality
- Account activation via email

## Installation

1. Clone the repository: `git clone https://github.com/Romaric250/user-authentication-service.git`
2. Install dependencies: `npm install`
3. Configure the environment variables: Create a `.env` file and set the required variables.
4. Start the server: `npm start`

## Usage

1. Register a new user by sending a `POST` request to `/api/register` with the required user details.
2. Login with the registered user credentials by sending a `POST` request to `/api/login`.
3. Access protected routes by including the JWT token in the `Authorization` header of your requests.

## Contributing

Contributions are welcome! Please follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md) to contribute to this project.

## License

This project is licensed under the [MIT License](./LICENSE).

## Contact

For any inquiries or support, please contact us at [email protected]
