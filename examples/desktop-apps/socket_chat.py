import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import socket
import threading
import time
from datetime import datetime

class SocketChatApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Socket Desktop Chat")
        self.window.geometry("600x700")
        self.window.resizable(True, True)
        self.window.configure(bg="#2c3e50")
        
        # Application state
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
        
        self.setup_ui()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.window,
            text="SOCKET DESKTOP CHAT",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=10)
        
        # Connection frame
        connection_frame = tk.Frame(self.window, bg="#2c3e50")
        connection_frame.pack(pady=10, padx=20, fill="x")
        
        # Mode selection
        mode_frame = tk.Frame(connection_frame, bg="#2c3e50")
        mode_frame.pack(pady=5, fill="x")
        
        self.mode_var = tk.StringVar(value="client")
        
        server_radio = tk.Radiobutton(
            mode_frame,
            text="Start Server",
            variable=self.mode_var,
            value="server",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1",
            selectcolor="#34495e",
            activebackground="#2c3e50",
            activeforeground="#ecf0f1",
            command=self.on_mode_change
        )
        server_radio.pack(side=tk.LEFT, padx=10)
        
        client_radio = tk.Radiobutton(
            mode_frame,
            text="Connect to Server",
            variable=self.mode_var,
            value="client",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#ecf0f1",
            selectcolor="#34495e",
            activebackground="#2c3e50",
            activeforeground="#ecf0f1",
            command=self.on_mode_change
        )
        client_radio.pack(side=tk.LEFT, padx=10)
        
        # Connection settings
        settings_frame = tk.Frame(connection_frame, bg="#2c3e50")
        settings_frame.pack(pady=5, fill="x")
        
        tk.Label(settings_frame, text="Host:", font=("Arial", 10), 
                bg="#2c3e50", fg="#ecf0f1").pack(side=tk.LEFT)
        
        self.host_entry = tk.Entry(settings_frame, font=("Arial", 10), width=15)
        self.host_entry.pack(side=tk.LEFT, padx=5)
        self.host_entry.insert(0, self.host)
        
        tk.Label(settings_frame, text="Port:", font=("Arial", 10), 
                bg="#2c3e50", fg="#ecf0f1").pack(side=tk.LEFT, padx=(10, 0))
        
        self.port_entry = tk.Entry(settings_frame, font=("Arial", 10), width=8)
        self.port_entry.pack(side=tk.LEFT, padx=5)
        self.port_entry.insert(0, str(self.port))
        
        # Connection button
        self.connect_button = tk.Button(
            connection_frame,
            text="Start Server",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            activeforeground="white",
            width=15,
            height=1,
            command=self.toggle_connection
        )
        self.connect_button.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(
            self.window,
            text="Status: Disconnected",
            font=("Arial", 12),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.status_label.pack(pady=5)
        
        # Chat display area
        chat_frame = tk.Frame(self.window, bg="#2c3e50")
        chat_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(chat_frame, text="Chat Messages:", font=("Arial", 12, "bold"), 
                bg="#2c3e50", fg="#ecf0f1").pack(anchor="w")
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=70,
            height=20,
            font=("Arial", 10),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            state=tk.DISABLED
        )
        self.chat_display.pack(fill="both", expand=True, pady=5)
        
        # Message input area
        input_frame = tk.Frame(self.window, bg="#2c3e50")
        input_frame.pack(pady=10, padx=20, fill="x")
        
        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#34495e",
            fg="#ecf0f1",
            insertbackground="#ecf0f1",
            state=tk.DISABLED
        )
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            width=8,
            command=self.send_message,
            state=tk.DISABLED
        )
        self.send_button.pack(side=tk.RIGHT)
        
        # Online users area (for server mode)
        self.users_frame = tk.Frame(self.window, bg="#2c3e50")
        self.users_label = tk.Label(
            self.users_frame,
            text="Online Users: 0",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        self.users_label.pack(pady=5)
    
    def on_mode_change(self):
        """Handle mode change between server and client"""
        mode = self.mode_var.get()
        if mode == "server":
            self.connect_button.config(text="Start Server")
            self.host_entry.config(state=tk.DISABLED)
        else:
            self.connect_button.config(text="Connect to Server")
            self.host_entry.config(state=tk.NORMAL)
    
    def toggle_connection(self):
        """Toggle between connect and disconnect"""
        if not self.is_connected:
            self.start_connection()
        else:
            self.stop_connection()
    
    def start_connection(self):
        """Start server or client connection"""
        try:
            self.host = self.host_entry.get().strip()
            self.port = int(self.port_entry.get().strip())
            
            if self.mode_var.get() == "server":
                self.start_server()
            else:
                self.start_client()
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid port number")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {str(e)}")
    
    def start_server(self):
        """Start the chat server"""
        try:
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_obj.bind((self.host, self.port))
            self.socket_obj.listen(5)
            
            self.is_server = True
            self.is_connected = True
            self.username = "Server"
            
            self.update_ui_connected()
            self.add_message("System", f"Server started on {self.host}:{self.port}")
            
            # Start server thread
            self.server_thread = threading.Thread(target=self.server_loop, daemon=True)
            self.server_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.is_connected = False
    
    def start_client(self):
        """Start the chat client"""
        # Get username
        username = simpledialog.askstring("Username", "Enter your username:", parent=self.window)
        if not username:
            return
            
        self.username = username.strip()
        
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            
            # Send username to server
            self.client_socket.send(self.username.encode('utf-8'))
            
            self.is_connected = True
            self.update_ui_connected()
            self.add_message("System", f"Connected to server at {self.host}:{self.port}")
            
            # Start client thread
            self.client_thread = threading.Thread(target=self.client_loop, daemon=True)
            self.client_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
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
                self.update_users_count()
                
                self.add_message("System", f"{username} joined the chat")
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
                    self.add_message("System", f"Server error: {str(e)}")
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
                    
                self.add_message(username, message)
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
                    self.add_message(username, msg)
                else:
                    self.add_message("System", message)
                    
            except Exception as e:
                if self.is_connected:
                    self.add_message("System", f"Connection error: {str(e)}")
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
            
            self.add_message("System", f"{username} left the chat")
            self.broadcast_message("System", f"{username} left the chat")
            self.update_users_count()
    
    def send_message(self, event=None):
        """Send a message"""
        message = self.message_entry.get().strip()
        if not message:
            return
            
        self.message_entry.delete(0, tk.END)
        
        if self.is_server:
            # Server sending message
            self.add_message(self.username, message)
            self.broadcast_message(self.username, message)
        else:
            # Client sending message
            try:
                self.client_socket.send(message.encode('utf-8'))
                self.add_message(self.username, message)
            except Exception as e:
                self.add_message("System", f"Failed to send message: {str(e)}")
    
    def add_message(self, username, message):
        """Add a message to the chat display"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        self.chat_display.config(state=tk.NORMAL)
        
        if username == "System":
            self.chat_display.insert(tk.END, f"[{timestamp}] System: {message}\n")
            self.chat_display.tag_add("system", "end-2l linestart", "end-1l linestart")
            self.chat_display.tag_config("system", foreground="#95a5a6")
        elif username == self.username:
            self.chat_display.insert(tk.END, f"[{timestamp}] You: {message}\n")
            self.chat_display.tag_add("self", "end-2l linestart", "end-1l linestart")
            self.chat_display.tag_config("self", foreground="#3498db")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] {username}: {message}\n")
            self.chat_display.tag_add("other", "end-2l linestart", "end-1l linestart")
            self.chat_display.tag_config("other", foreground="#e74c3c")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def update_ui_connected(self):
        """Update UI when connected"""
        self.connect_button.config(text="Disconnect", bg="#e74c3c", activebackground="#c0392b")
        self.status_label.config(
            text=f"Status: Connected ({'Server' if self.is_server else 'Client'})",
            fg="#27ae60"
        )
        self.message_entry.config(state=tk.NORMAL)
        self.send_button.config(state=tk.NORMAL)
        self.host_entry.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.DISABLED)
        
        # Show users frame for server
        if self.is_server:
            self.users_frame.pack(pady=5)
    
    def update_ui_disconnected(self):
        """Update UI when disconnected"""
        self.connect_button.config(
            text="Start Server" if self.mode_var.get() == "server" else "Connect to Server",
            bg="#27ae60", 
            activebackground="#229954"
        )
        self.status_label.config(text="Status: Disconnected", fg="#e74c3c")
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.port_entry.config(state=tk.NORMAL)
        
        if self.mode_var.get() == "client":
            self.host_entry.config(state=tk.NORMAL)
        
        # Hide users frame
        self.users_frame.pack_forget()
    
    def update_users_count(self):
        """Update the online users count"""
        if self.is_server:
            count = len(self.clients)
            self.users_label.config(text=f"Online Users: {count}")
    
    def stop_connection(self):
        """Stop the connection"""
        self.is_connected = False
        
        if self.is_server:
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
            # Close client socket
            if self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
        
        self.is_server = False
        self.update_ui_disconnected()
        self.add_message("System", "Disconnected")
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_connected:
            self.stop_connection()
        self.window.destroy()
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Create and run the chat application
if __name__ == "__main__":
    app = SocketChatApp()
    app.run()