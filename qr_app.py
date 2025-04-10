import qrcode
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import sys

# ---------- Helper Function for Resource Path ----------
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS  # When bundled by PyInstaller
    except Exception:
        base_path = os.path.abspath(".")  # When running as script
    return os.path.join(base_path, relative_path)

# ---------- Splash Screen ----------
splash_root = tk.Tk()
splash_root.overrideredirect(True)  # No title bar
splash_root.iconbitmap(resource_path("qr.ico"))  # Custom icon

# Splash screen dimensions
splash_width = 800
splash_height = 500
screen_width = splash_root.winfo_screenwidth()
screen_height = splash_root.winfo_screenheight()
x_pos = (screen_width // 2) - (splash_width // 2)
y_pos = (screen_height // 2) - (splash_height // 2)
splash_root.geometry(f"{splash_width}x{splash_height}+{x_pos}+{y_pos}")

# Create a canvas to display splash image without border
canvas = tk.Canvas(splash_root, width=splash_width, height=splash_height, bd=0, highlightthickness=0)
canvas.pack()

# Load splash image
splash_img = Image.open(resource_path("heisen_cover.png"))
splash_img = splash_img.resize((splash_width, splash_height))
splash_photo = ImageTk.PhotoImage(splash_img)
splash_label = tk.Label(canvas, image=splash_photo)
splash_label.pack()

# Close splash screen after 2.5 seconds
splash_root.after(2500, splash_root.destroy)
splash_root.mainloop()

# ---------- Main App ----------
def generate_qr():
    name = name_entry.get()
    designation = designation_entry.get()
    phone = phone_entry.get()
    company = company_entry.get()
    email = email_entry.get()

    if not name or not designation or not phone or not company or not email:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Constructing vCard data with name, company, designation, phone, and email
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TITLE;CHARSET=UTF-8:{designation}
ORG;CHARSET=UTF-8:{company}
TEL;TYPE=cell:{phone}
EMAIL;TYPE=work:{email}
END:VCARD"""



    img = qrcode.make(vcard_data)
    img = img.resize((150, 150))

    preview_img = ImageTk.PhotoImage(img)
    qr_preview_label.config(image=preview_img)
    qr_preview_label.image = preview_img

def save_qr():
    name = name_entry.get()
    designation = designation_entry.get()
    phone = phone_entry.get()
    company = company_entry.get()
    email = email_entry.get()

    if not name or not designation or not phone or not company or not email:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    # Constructing vCard data with name, company, designation, phone, and email
    vcard_data = f"""BEGIN:VCARD
VERSION:3.0
FN:{name}
TITLE;CHARSET=UTF-8:{designation}
ORG;CHARSET=UTF-8:{company}
TEL;TYPE=cell:{phone}
EMAIL;TYPE=work:{email}
END:VCARD"""



    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    if not file_path:
        return

    img = qrcode.make(vcard_data)
    img.save(file_path)
    messagebox.showinfo("Success", f"QR Code saved to:\n{file_path}")

# Main window
root = tk.Tk()
root.title("Heisencorp's QR Code Generator")
root.iconbitmap(resource_path("qr.ico"))

main_width = 700
main_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_main = (screen_width // 2) - (main_width // 2)
y_main = (screen_height // 2) - (main_height // 2)
root.geometry(f"{main_width}x{main_height}+{x_main}+{y_main}")

# Frame setup
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

# Left form section
form_frame = tk.Frame(frame)
form_frame.grid(row=0, column=0, padx=20)

tk.Label(form_frame, text="Name:", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky="w")
name_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
name_entry.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Designation:", font=("Arial", 12)).grid(row=1, column=0, pady=5, sticky="w")
designation_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
designation_entry.grid(row=1, column=1, pady=5)

tk.Label(form_frame, text="Phone:", font=("Arial", 12)).grid(row=2, column=0, pady=5, sticky="w")
phone_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
phone_entry.grid(row=2, column=1, pady=5)

tk.Label(form_frame, text="Company:", font=("Arial", 12)).grid(row=3, column=0, pady=5, sticky="w")
company_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
company_entry.grid(row=3, column=1, pady=5)

tk.Label(form_frame, text="Email:", font=("Arial", 12)).grid(row=4, column=0, pady=5, sticky="w")
email_entry = tk.Entry(form_frame, width=40, font=("Arial", 11))
email_entry.grid(row=4, column=1, pady=5)

# Right preview section
preview_frame = tk.Frame(frame, width=150, height=150, bg="lightgray")
preview_frame.grid(row=0, column=1, padx=20)
preview_frame.pack_propagate(False)

qr_preview_label = tk.Label(preview_frame, bg="lightgray")
qr_preview_label.pack(expand=True)

# Buttons
generate_button = tk.Button(root, text="Generate QR Code", font=("Arial", 12), command=generate_qr, bg="#1d9371", fg="white")
generate_button.pack(pady=(20, 5))

save_button = tk.Button(root, text="Save QR Code", font=("Arial", 12), command=save_qr)
save_button.pack(pady=10)

root.mainloop()
