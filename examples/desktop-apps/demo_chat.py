#!/usr/bin/env python3
"""
Demo script for the Socket Desktop Chat application

This script demonstrates the chat functionality by simulating 
server and client interactions.
"""
import socket
import threading
import time
from datetime import datetime

def demo_chat():
    """Demonstrate the socket chat functionality"""
    print("=== Socket Desktop Chat Demo ===")
    print()
    
    # Configuration
    host = 'localhost'
    port = 12348
    
    # Server setup
    print("1. Starting chat server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(2)
    print(f"   Server listening on {host}:{port}")
    
    clients = []
    
    def handle_client(client_socket, username):
        """Handle messages from a client"""
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                broadcast_msg = f"[{timestamp}] {username}: {message}"
                print(f"   Server received: {broadcast_msg}")
                
                # Broadcast to other clients
                for other_client, other_name in clients:
                    if other_client != client_socket:
                        try:
                            other_client.send(broadcast_msg.encode('utf-8'))
                        except:
                            pass
                            
            except Exception as e:
                print(f"   Error handling client {username}: {e}")
                break
        
        # Remove client
        for client_info in clients[:]:
            if client_info[0] == client_socket:
                clients.remove(client_info)
                break
        
        try:
            client_socket.close()
        except:
            pass
        
        print(f"   Client {username} disconnected")
    
    def server_loop():
        """Accept client connections"""
        while True:
            try:
                client_socket, addr = server_socket.accept()
                
                # Get username
                username = client_socket.recv(1024).decode('utf-8')
                clients.append((client_socket, username))
                
                print(f"   Client '{username}' connected from {addr}")
                
                # Start handler thread
                client_thread = threading.Thread(
                    target=handle_client, 
                    args=(client_socket, username),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                print(f"   Server error: {e}")
                break
    
    # Start server thread
    server_thread = threading.Thread(target=server_loop, daemon=True)
    server_thread.start()
    
    time.sleep(0.5)
    
    # Simulate clients
    print("\n2. Simulating client connections...")
    
    def simulate_client(username, messages, delay=1):
        """Simulate a chat client"""
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((host, port))
            
            # Send username
            client.send(username.encode('utf-8'))
            print(f"   {username} connected")
            
            # Start receiving thread
            def receive_messages():
                while True:
                    try:
                        message = client.recv(1024).decode('utf-8')
                        if message:
                            print(f"   {username} received: {message}")
                    except:
                        break
            
            receive_thread = threading.Thread(target=receive_messages, daemon=True)
            receive_thread.start()
            
            # Send messages
            for message in messages:
                time.sleep(delay)
                client.send(message.encode('utf-8'))
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"   {username} sent: [{timestamp}] {username}: {message}")
            
            time.sleep(2)  # Keep connection open for a bit
            client.close()
            print(f"   {username} disconnected")
            
        except Exception as e:
            print(f"   Error with client {username}: {e}")
    
    # Start client simulations
    client1_messages = [
        "Hello everyone!",
        "How is everyone doing?",
        "This chat app is working great!"
    ]
    
    client2_messages = [
        "Hi there!",
        "I'm doing well, thanks!",
        "Yes, the socket communication is smooth!"
    ]
    
    client1_thread = threading.Thread(
        target=simulate_client, 
        args=("Alice", client1_messages, 1.5),
        daemon=True
    )
    
    client2_thread = threading.Thread(
        target=simulate_client, 
        args=("Bob", client2_messages, 2),
        daemon=True
    )
    
    client1_thread.start()
    time.sleep(0.5)  # Stagger client connections
    client2_thread.start()
    
    # Wait for clients to finish
    client1_thread.join(timeout=10)
    client2_thread.join(timeout=10)
    
    print("\n3. Demo completed!")
    print("   Both GUI and CLI versions of the chat app are ready to use.")
    print("   Key features demonstrated:")
    print("   - Socket server/client architecture")
    print("   - Multi-client support with threading")
    print("   - Real-time message broadcasting")
    print("   - Connection management")
    print("   - Error handling")
    
    # Cleanup
    try:
        server_socket.close()
    except:
        pass
    
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_chat()