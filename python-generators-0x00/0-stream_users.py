#!/usr/bin/env python3
"""
Module for streaming database rows using generators
"""

import mysql.connector
from mysql.connector import Error
import os
from typing import Generator, Dict, Any


def stream_users() -> Generator[Dict[str, Any], None, None]:
    """
    Generator function that streams rows from user_data table one by one.
    
    Yields:
        Dict[str, Any]: Dictionary containing user data from each row
    
    Raises:
        mysql.connector.Error: If database connection or query fails
    """
    connection = None
    cursor = None
    
    try:
        # Database configuration - modify these values for your setup
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'your_database'),
            'user': os.getenv('DB_USER', 'your_username'),
            'password': os.getenv('DB_PASSWORD', 'your_password'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': True
        }
        
        # Create database connection
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True, buffered=False)
            
            # Execute query to fetch all users
            query = "SELECT * FROM user_data"
            cursor.execute(query)
            
            # Yield rows one by one
            for row in cursor:
                yield row
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise
    
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def stream_users_with_limit(limit: int = None) -> Generator[Dict[str, Any], None, None]:
    """
    Generator function that streams limited rows from user_data table.
    
    Args:
        limit (int, optional): Maximum number of rows to fetch
    
    Yields:
        Dict[str, Any]: Dictionary containing user data from each row
    """
    connection = None
    cursor = None
    
    try:
        config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'database': os.getenv('DB_NAME', 'your_database'),
            'user': os.getenv('DB_USER', 'your_username'),
            'password': os.getenv('DB_PASSWORD', 'your_password'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'charset': 'utf8mb4',
            'use_unicode': True,
            'autocommit': True
        }
        
        connection = mysql.connector.connect(**config)
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True, buffered=False)
            
            # Build query with optional limit
            query = "SELECT * FROM user_data"
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query)
            
            # Yield rows one by one
            for row in cursor:
                yield row
                
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        raise
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# Example usage
if __name__ == "__main__":
    # Example 1: Stream all users
    print("Streaming all users:")
    try:
        for user in stream_users():
            print(f"User: {user}")
            # Process each user here
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Stream limited users
    print("\nStreaming first 10 users:")
    try:
        for user in stream_users_with_limit(10):
            print(f"User: {user}")
            
    except Exception as e:
        print(f"Error: {e}")