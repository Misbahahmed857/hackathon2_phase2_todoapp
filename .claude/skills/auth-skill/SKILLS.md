---
name: auth-skill
description: Implement secure authentication including signup, signin, password hashing, JWT tokens, and Better Auth integration.
---

# Authentication Skill

## Instructions

1. **User Registration (Signup)**
   - Collect user credentials (email, password)
   - Validate input (email format, password strength)
   - Hash passwords before storing
   - Prevent duplicate accounts

2. **User Login (Signin)**
   - Verify user credentials
   - Compare hashed passwords securely
   - Handle invalid login attempts
   - Return authentication tokens on success

3. **Password Security**
   - Use strong hashing algorithms (bcrypt / argon2)
   - Never store plain-text passwords
   - Apply salting automatically
   - Support password reset flow

4. **JWT Authentication**
   - Generate access tokens on login
   - Include user claims in payload
   - Set token expiration
   - Verify tokens for protected routes

5. **Better Auth Integration**
   - Configure Better Auth provider
   - Use built-in session handling
   - Enable OAuth / email-password auth
   - Manage refresh tokens securely

## Best Practices
- Always hash passwords
- Use HTTPS for auth endpoints
- Keep JWT secrets private
- Short-lived access tokens
- Store tokens securely (HTTP-only cookies)
- Implement logout and token invalidation

## Example Structure
```ts
// Signup
await auth.signUp({
  email: "user@example.com",
  password: "StrongPassword123"
});

// Signin
const session = await auth.signIn({
  email: "user@example.com",
  password: "StrongPassword123"
});

// Protect Route
app.get("/dashboard", verifyJWT, (req, res) => {
  res.send("Authenticated User");
});
