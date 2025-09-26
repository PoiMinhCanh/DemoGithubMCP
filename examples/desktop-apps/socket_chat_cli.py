#!/usr/bin/env python3
"""
Socket Desktop Chat - Command Line Interface Version

A command-line version of the socket chat application for headless environments
and testing purposes.
"""
import socket
import threading
import time
import sys
from datetime import datetime

class SocketChatCLI:
    def __init__(self):
        self.is_server = False
        self.is_connected = False
        self.socket_obj = None
        self.clients = []  # For server mode
        self.client_socket = None  # For client mode
        self.username = ""
        self.server_thread = None
        self.client_thread = None
        
        # Default connection settings
        self.host = "localhost"
        self.port = 12345
        
    def print_message(self, username, message):
        """Print a message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if username == "System":
            print(f"[{timestamp}] System: {message}")
        elif username == self.username:
            print(f"[{timestamp}] You: {message}")
        else:
            print(f"[{timestamp}] {username}: {message}")
    
    def start_server(self):
        """Start the chat server"""
        try:
            print(f"Starting server on {self.host}:{self.port}...")
            
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_obj.bind((self.host, self.port))
            self.socket_obj.listen(5)
            
            self.is_server = True
            self.is_connected = True
            self.username = "Server"
            
            self.print_message("System", f"Server started on {self.host}:{self.port}")
            self.print_message("System", "Waiting for clients to connect...")
            
            # Start server thread
            self.server_thread = threading.Thread(target=self.server_loop, daemon=True)
            self.server_thread.start()
            
            # Server input loop
            self.server_input_loop()
            
        except Exception as e:
            print(f"Failed to start server: {str(e)}")
            self.is_connected = False
    
    def start_client(self, username):
        """Start the chat client"""
        try:
            print(f"Connecting to server at {self.host}:{self.port}...")
            
            self.username = username
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            # Send username to server
            self.client_socket.send(self.username.encode('utf-8'))
            
            self.is_connected = True
            self.print_message("System", f"Connected to server at {self.host}:{self.port}")
            
            # Start client thread
            self.client_thread = threading.Thread(target=self.client_loop, daemon=True)
            self.client_thread.start()
            
            # Client input loop
            self.client_input_loop()
            
        except Exception as e:
            print(f"Failed to connect: {str(e)}")
            self.is_connected = False
    
    def server_loop(self):
        """Main server loop to accept clients"""
        while self.is_connected and self.socket_obj:
            try:
                client_socket, addr = self.socket_obj.accept()
                
                # Receive username
                username = client_socket.recv(1024).decode('utf-8')
                
                client_info = {
                    'socket': client_socket,
                    'username': username,
                    'address': addr
                }
                
                self.clients.append(client_info)
                
                self.print_message("System", f"{username} joined the chat (Users online: {len(self.clients)})")
                self.broadcast_message("System", f"{username} joined the chat", exclude_client=client_socket)
                
                # Start thread for this client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_info,), 
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.is_connected:
                    self.print_message("System", f"Server error: {str(e)}")
                break
    
    def handle_client(self, client_info):
        """Handle messages from a specific client"""
        client_socket = client_info['socket']
        username = client_info['username']
        
        while self.is_connected:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                self.print_message(username, message)
                self.broadcast_message(username, message, exclude_client=client_socket)
                
            except Exception:
                break
        
        # Client disconnected
        self.remove_client(client_info)
    
    def client_loop(self):
        """Main client loop to receive messages"""
        while self.is_connected and self.client_socket:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                    
                # Parse message (format: "username: message")
                if ": " in message:
                    username, msg = message.split(": ", 1)
                    self.print_message(username, msg)
                else:
                    self.print_message("System", message)
                    
            except Exception as e:
                if self.is_connected:
                    self.print_message("System", f"Connection error: {str(e)}")
                break
        
        self.stop_connection()
    
    def broadcast_message(self, username, message, exclude_client=None):
        """Broadcast message to all connected clients"""
        full_message = f"{username}: {message}"
        
        for client_info in self.clients[:]:  # Use slice to avoid modification during iteration
            if client_info['socket'] != exclude_client:
                try:
                    client_info['socket'].send(full_message.encode('utf-8'))
                except Exception:
                    self.remove_client(client_info)
    
    def remove_client(self, client_info):
        """Remove a disconnected client"""
        if client_info in self.clients:
            self.clients.remove(client_info)
            username = client_info['username']
            
            try:
                client_info['socket'].close()
            except:
                pass
            
            self.print_message("System", f"{username} left the chat (Users online: {len(self.clients)})")
            self.broadcast_message("System", f"{username} left the chat")
    
    def server_input_loop(self):
        """Handle server input"""
        print("\nServer is running. Type messages to broadcast to all clients.")
        print("Type '/quit' to stop the server, '/users' to see connected users.")
        
        while self.is_connected:
            try:
                message = input().strip()
                
                if message == '/quit':
                    break
                elif message == '/users':
                    print(f"Connected users ({len(self.clients)}): {', '.join([c['username'] for c in self.clients])}")
                elif message:
                    self.print_message(self.username, message)
                    self.broadcast_message(self.username, message)
                    
            except (KeyboardInterrupt, EOFError):
                break
        
        self.stop_connection()
    
    def client_input_loop(self):
        """Handle client input"""
        print(f"\nConnected as {self.username}. Start typing messages!")
        print("Type '/quit' to disconnect.")
        
        while self.is_connected:
            try:
                message = input().strip()
                
                if message == '/quit':
                    break
                elif message:
                    try:
                        self.client_socket.send(message.encode('utf-8'))
                        self.print_message(self.username, message)
                    except Exception as e:
                        self.print_message("System", f"Failed to send message: {str(e)}")
                        break
                        
            except (KeyboardInterrupt, EOFError):
                break
        
        self.stop_connection()
    
    def stop_connection(self):
        """Stop the connection"""
        self.is_connected = False
        
        if self.is_server:
            self.print_message("System", "Stopping server...")
            
            # Close all client connections
            for client_info in self.clients[:]:
                try:
                    client_info['socket'].close()
                except:
                    pass
            self.clients.clear()
            
            # Close server socket
            if self.socket_obj:
                try:
                    self.socket_obj.close()
                except:
                    pass
                self.socket_obj = None
        else:
            self.print_message("System", "Disconnecting from server...")
            
            # Close client socket
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
        
        self.is_server = False
        print("Disconnected.")

def main():
    """Main function to run the CLI chat application"""
    print("=== Socket Desktop Chat - CLI Version ===")
    print()
    
    chat = SocketChatCLI()
    
    # Get configuration
    try:
        mode = input("Choose mode (1: Server, 2: Client): ").strip()
        
        if mode == "1":
            # Server mode
            host = input(f"Host (default: {chat.host}): ").strip()
            if host:
                chat.host = host
                
            port = input(f"Port (default: {chat.port}): ").strip()
            if port:
                chat.port = int(port)
                
            chat.start_server()
            
        elif mode == "2":
            # Client mode
            host = input(f"Server host (default: {chat.host}): ").strip()
            if host:
                chat.host = host
                
            port = input(f"Server port (default: {chat.port}): ").strip()
            if port:
                chat.port = int(port)
                
            username = input("Your username: ").strip()
            if not username:
                username = "Anonymous"
                
            chat.start_client(username)
            
        else:
            print("Invalid mode selected.")
            
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")
    except ValueError:
        print("Invalid port number.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()