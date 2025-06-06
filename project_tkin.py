import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# User credentials (for demonstration)
users = {
    "saran": {"password": "123456", "email": "saranyaraj070996@gmail.com", "profile_pic": r"c:\Users\welcome\Downloads\Tree.jpg"},
}

# Store the generated OTP
otp_code = None

# Function to generate a 6-digit OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to send OTP via email
def send_otp_email(recipient_email, otp):
    sender_email = "saranyaraj070996@gmail.com"
    sender_password = "aecp rijs hute gkyc"  # Use your actual password

    # Create the email content
    subject = "Your OTP Code"
    body = f"Your OTP code is: {otp}"
    
    # Setting up MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure the connection
        server.login('saranyaraj070996@gmail.com','aecp rijs hute gkyc')  # Login to the email account
        text = msg.as_string()
        server.sendmail('saranyaraj070996@gmail.com','saranyaraj070996@gmail.com', text)  # Send the email
        server.quit()  # Terminate the SMTP session
        print(f"OTP sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to verify OTP
def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == str(otp_code):
        messagebox.showinfo("Login Success", f"Welcome, {username_entry.get()}!")
        otp_window.destroy()  # Close the OTP window
        show_profile_picture()
    else:
        messagebox.showerror("Invalid OTP", "The OTP entered is incorrect.")

# Function to upload profile picture
def upload_profile_picture():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        users[username_entry.get()]["profile_pic"] = file_path
        show_profile_picture()

# Function to display profile picture
def show_profile_picture():
    user = username_entry.get()
    if users[user]["profile_pic"]:
        img_path = users[user]["profile_pic"]
        img = Image.open(img_path)
        img = img.resize((100, 100))  # Resize the image
        img_tk = ImageTk.PhotoImage(img)
        
        profile_label.config(image=img_tk)
        profile_label.image = img_tk  # Keep a reference to avoid garbage collection
    else:
        messagebox.showwarning("No Profile Picture", "No profile picture uploaded.")

# Function to handle login
def login():
    global otp_code
    
    username = username_entry.get()
    password = password_entry.get()
    
    if username in users and users[username]["password"] == password:
        otp_code = generate_otp()
        recipient_email = users[username]["email"]
        send_otp_email(recipient_email, otp_code)  # Send OTP via email
        
        # Open a new window for OTP entry
        global otp_window, otp_entry
        otp_window = tk.Toplevel(root)
        otp_window.title("Enter OTP")
        otp_window.geometry("300x200")
        
        tk.Label(otp_window, text="Enter OTP sent to your email:").pack(pady=10)
        otp_entry = tk.Entry(otp_window)
        otp_entry.pack(pady=10)
        
        tk.Button(otp_window, text="Verify OTP", command=verify_otp).pack(pady=10)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Create the main window
root = tk.Tk()
root.title("Login Page")
root.geometry("300x300")

# Username label and entry
tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

# Password label and entry
tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

# Login button
login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=20)

# Profile Picture Section
tk.Label(root, text="Upload Profile Picture:").pack(pady=5)
upload_button = tk.Button(root, text="Choose File", command=upload_profile_picture)
upload_button.pack(pady=5)

profile_label = tk.Label(root)  # Label to show profile picture
profile_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()