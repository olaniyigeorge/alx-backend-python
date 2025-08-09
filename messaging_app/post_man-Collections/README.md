
# Messaging App Postman Collection

## Overview
This Postman collection tests:
- Creating a conversation
- Sending messages
- Fetching conversations
- JWT authentication
- Unauthorized access prevention

## Steps to Use
1. Open Postman.
2. Import `messaging_app.postman_collection.json`.
3. Set the `jwt_token` variable:
   - Run the **User Login** request.
   - Copy the token from the response.
   - Go to `Variables` tab in Postman and set `jwt_token`.
4. Run **Create Conversation**, **Send Message**, and **Fetch Conversations** requests.
5. Test **Unauthorized Access** by running the request without `Authorization` header.

## API Base URL
Change `http://localhost:8000` to your actual API server address if different.
