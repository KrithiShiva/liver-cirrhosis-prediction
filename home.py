import customtkinter as ctk
from PIL import Image, ImageTk
import os

try:
    import admin_login  # Import the admin module
except ImportError:
    print("Error: admin_login module not found. Make sure admin_login.py exists in the same directory.")

try:
    from user_login import show_user_login
except ImportError:
    print("Error: user_login module not found. Make sure user_login.py exists in the same directory.")

# Initialize the main window
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


app = ctk.CTk()
app.title("Liver Guard")
app.geometry("1000x1080")
app.state("zoomed")  # Make window fullscreen

# Load Background Image or Default Gradient Background
def load_background():
    bg_image_path = "background.jpeg"
    if os.path.exists(bg_image_path):
        try:
            bg_image = Image.open(bg_image_path)
            bg_image = bg_image.resize((app.winfo_screenwidth(), app.winfo_screenheight()))
            bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = ctk.CTkLabel(app, image=bg_photo, text="", fg_color="transparent")
            bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
            bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")
            apply_gradient_background()
    else:
        apply_gradient_background()

# Function to Apply Gradient Background
def apply_gradient_background():
    canvas = ctk.CTkCanvas(app, width=app.winfo_screenwidth(), height=app.winfo_screenheight(), highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)

    gradient = canvas.create_rectangle(0, 0, app.winfo_screenwidth(), app.winfo_screenheight(), 
                                        fill="", outline="")
    canvas.tag_lower(gradient)
    canvas.bind("<Configure>", lambda event: draw_gradient(canvas))

# Draw Gradient Background
def draw_gradient(canvas):
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    color1 = "#d3d3d3"  # Light grey
    color2 = "#808080"  # Dark grey

    for i in range(height):
        color = canvas.winfo_rgb(color1)
        r1, g1, b1 = [x >> 8 for x in color]

        color = canvas.winfo_rgb(color2)
        r2, g2, b2 = [x >> 8 for x in color]

        factor = i / height
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        canvas.create_line(0, i, width, i, fill=hex_color)

load_background()

# Function for smooth page transitions
def smooth_transition(new_frame):
    global current_frame
    current_frame.place_forget()
    new_frame.place(relwidth=1, relheight=1)
    current_frame = new_frame

# Logout Function with Animated Popup
def logout():
    logout_frame = ctk.CTkFrame(app, fg_color="#1E1E1E", corner_radius=20)
    logout_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.2)

    message_label = ctk.CTkLabel(
        logout_frame, text="Logging out...", font=("Arial", 20, "bold"), text_color="white"
    )
    message_label.pack(expand=True)

    # Automatically return to home after 5 seconds
    def return_home():
        logout_frame.place_forget()
        smooth_transition(home_frame)

    app.after(5000, return_home)

# About Us Page
def show_about():
    global current_frame
    about_frame = ctk.CTkFrame(app, fg_color="#1E1E1E")

    # Back Button
    back_btn = ctk.CTkButton(
        about_frame, text="\u2190 Back", fg_color="#333333", text_color="white",
        corner_radius=10, font=("Arial", 20), command=lambda: smooth_transition(home_frame)
    )
    back_btn.pack(pady=20, padx=20, anchor="nw")

    # Image Slider
    image_paths = ["image1.jpg", "image2.jpg", "image3.jpg"]
    images = []
    for path in image_paths:
        if os.path.exists(path):
            images.append(ctk.CTkImage(light_image=Image.open(path).resize((270, 270)), size=(270, 270)))
        else:
            print(f"Warning: {path} not found. Skipping this image.")

    if images:
        img_label = ctk.CTkLabel(about_frame, image=images[0], text="", fg_color="transparent")
        img_label.pack(pady=20)

        def next_image(index=0):
            if img_label.winfo_exists() and images:
                img_label.configure(image=images[index])
                app.after(3000, next_image, (index + 1) % len(images))

        next_image()

    text_box = ctk.CTkFrame(
        about_frame, fg_color="#2E2E2E", border_color="#555555", border_width=2, corner_radius=10
    )
    text_box.pack(pady=20, padx=20)

    about_title = ctk.CTkLabel(
        text_box, text="ABOUT US", font=("Arial", 40, "bold"), text_color="#007BFF"
    )
    about_title.pack(pady=10)

    about_text = (
        "Liver Guard is an AI-based liver disease prediction system. "
        "It helps users analyze symptoms and predict the likelihood of liver cirrhosis based on medical data. "
        "Additionally, it provides hepatitis prediction for users unaware of their hepatitis status. "
        "Liver cirrhosis is a progressive and life-threatening condition characterized by irreversible liver damage "
        "that often remains undiagnosed until its advanced stages. It is primarily caused by chronic hepatitis infections, "
        "excessive alcohol consumption, fatty liver disease, and metabolic disorders. "
        "Early diagnosis plays a crucial role in preventing severe complications such as liver failure and hepatocellular carcinoma (liver cancer)."
    )

    about_label = ctk.CTkLabel(
        text_box, text=about_text, font=("Arial", 20), text_color="white", wraplength=900, justify="center"
    )
    about_label.pack(pady=20, padx=20)

    smooth_transition(about_frame)

# Home Frame
home_frame = ctk.CTkFrame(app, fg_color="transparent")
home_frame.place(relwidth=1, relheight=1)

# Navigation Bar
nav_frame = ctk.CTkFrame(home_frame, fg_color="#1E1E1E", height=60)
nav_frame.pack(fill="x")

nav_title = ctk.CTkLabel(
    nav_frame, text="LIVER ", font=("Arial", 28, "bold"), text_color="#FF5733", fg_color="transparent"
)
nav_title.pack(side="left", padx=10, pady=10)
nav_title2 = ctk.CTkLabel(
    nav_frame, text="GUARD", font=("Arial", 28, "bold"), text_color="#007BFF", fg_color="transparent"
)
nav_title2.pack(side="left", pady=10)

nav_buttons_frame = ctk.CTkFrame(nav_frame, fg_color="#1E1E1E")
nav_buttons_frame.pack(side="right", padx=20)

home_btn = ctk.CTkButton(
    nav_buttons_frame, text="HOME", fg_color="#1E1E1E", hover_color="#333333", text_color="white", corner_radius=10
)
home_btn.pack(side="left", padx=10)

about_btn = ctk.CTkButton(
    nav_buttons_frame, text="ABOUT US", fg_color="#1E1E1E", hover_color="#333333", text_color="white", corner_radius=10, command=show_about
)
about_btn.pack(side="left", padx=10)

help_btn = ctk.CTkButton(
    nav_buttons_frame, text="HELP", fg_color="#1E1E1E", hover_color="#333333", text_color="white", corner_radius=10
)
help_btn.pack(side="left", padx=10)

logout_btn = ctk.CTkButton(
    nav_buttons_frame, text="LOGOUT", fg_color="#1E1E1E", hover_color="#333333", text_color="white", corner_radius=10, command=logout
)
logout_btn.pack(side="left", padx=10)

# User and Admin Login Buttons
user_login_btn = ctk.CTkButton(
    home_frame, text="USER LOGIN", fg_color="#007BFF", hover_color="#0056B3", text_color="white", corner_radius=15,
    font=("Arial", 18, "bold"), width=200, height=80, command=show_user_login if 'show_user_login' in globals() else None
)
user_login_btn.place(relx=0.4, rely=0.6, anchor="center")

def show_admin_login():
    if 'admin_login' in globals():
        admin_login.show_admin_login()
    else:
        print("Error: admin_login.show_admin_login() not available.")

admin_login_btn = ctk.CTkButton(
    home_frame, text="ADMIN LOGIN", fg_color="#007BFF", hover_color="#0056B3", text_color="white", corner_radius=15,
    font=("Arial", 18, "bold"), width=200, height=80, command=show_admin_login
)
admin_login_btn.place(relx=0.6, rely=0.6, anchor="center")

quote_label = ctk.CTkLabel(
    home_frame, text="ALTHOUGH THE WORLD IS FULL OF SUFFERING, IT IS ALSO FULL OF THE OVERCOMING OF IT",
    font=("Arial", 26, "bold"), text_color="#800000", fg_color="transparent"
)
quote_label.place(relx=0.5, rely=0.35, anchor="center")

predict_label = ctk.CTkLabel(
    home_frame, text="PREDICT THE FUTURE", font=("Arial", 22, "bold"), text_color="black", fg_color="transparent"
)
predict_label.place(relx=0.5, rely=0.45, anchor="center")

footer_label = ctk.CTkLabel(
    home_frame, text="\u00a9 2025 Liver Guard | All Rights Reserved", font=("Arial", 12, "bold"), text_color="white",
    fg_color="#1E1E1E", height=40
)
footer_label.pack(side="bottom", fill="x")

# Set the initial frame
current_frame = home_frame

app.mainloop()
