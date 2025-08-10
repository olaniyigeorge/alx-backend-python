
# Messaging App Postman Collection

## Overview

This Postman collection allows you to test the following features:
- Creating a conversation
- Sending messages
- Fetching conversations
- JWT authentication
- Unauthorized access prevention

## Steps to Use

1. Open Postman.
2. Import the `messaging_app.postman_collection.json` file.
3. Set the `jwt_token` variable:
   - Run the **User Login** request.
   - Copy the token from the response.
   - Go to the `Variables` tab in Postman and set `jwt_token`.
4. Run the **Create Conversation**, **Send Message**, and **Fetch Conversations** requests.
5. Test **Unauthorized Access** by running the request without the `Authorization` header.

## API Base URL

Update `http://localhost:8000` to match your API server address if it is different.

## Building and Running the App

From the root of your repository, build the Docker image:

```bash
docker build -t messaging_app:latest -f messaging_app/Dockerfile .
```

Run the container:

```bash
docker run -p 8000:8000 messaging_app:latest
```

Access the app in your browser at [http://localhost:8000](http://localhost:8000).

