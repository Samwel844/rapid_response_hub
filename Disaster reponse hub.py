import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import os
import folium
import webbrowser
import geocoder
from geopy.geocoders import Nominatim

def save_report():
    disaster = disaster_type.get().strip()
    location_text = location.get().strip()
    description_text = description.get("1.0", tk.END).strip()
    photo_path = selected_image_path.get()

    if not disaster or not location_text or not description_text:
        messagebox.showerror("Error", "Please fill in all fields.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = (
        f"Time: {now}\n"
        f"Disaster Type: {disaster}\n"
        f"Location: {location_text}\n"
        f"Description: {description_text}\n"
        f"Photo Path: {photo_path}\n\n"
    )

    with open("disaster_reports.txt", "a") as file:
        file.write(report)

    messagebox.showinfo("Success", "✅ Disaster report submitted!")

    # Clear form
    disaster_type.delete(0, tk.END)
    location.delete(0, tk.END)
    description.delete("1.0", tk.END)
    selected_image_path.set("")

    show_map(location_text)

def view_reports():
    if not os.path.exists("disaster_reports.txt"):
        messagebox.showinfo("No Reports", "No disaster reports found yet.")
        return

    with open("disaster_reports.txt", "r") as file:
        reports = file.read()

    report_window = tk.Toplevel(root)
    report_window.title("Past Disaster Reports")
    text_area = tk.Text(report_window, width=80, height=20)
    text_area.pack()
    text_area.insert(tk.END, reports)

def choose_photo():
    filepath = filedialog.askopenfilename(
        title="Select a Photo",
        filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp")]
    )
    if filepath:
        selected_image_path.set(filepath)
        messagebox.showinfo("Photo Selected", f"Selected: {filepath}")

def get_user_location():
    try:
        g = geocoder.ip('me')
        latlng = g.latlng
        if latlng:
            location.delete(0, tk.END)
            location.insert(0, f"{latlng[0]}, {latlng[1]}")
            messagebox.showinfo("Location Found", f"Your coordinates: {latlng[0]}, {latlng[1]}")
        else:
            messagebox.showerror("Error", "Could not determine your location via IP.")
    except Exception as e:
        messagebox.showerror("Error", f"Geolocation failed:\n{e}")

def show_map(location_name):
    # Try parsing coordinates
    coords = None
    parts = location_name.split(',')
    if len(parts) == 2:
        try:
            coords = (float(parts[0].strip()), float(parts[1].strip()))
        except ValueError:
            coords = None

    # If not coords, geocode name
    if not coords:
        geolocator = Nominatim(user_agent="disaster_app")
        try:
            loc = geolocator.geocode(location_name)
            if loc:
                coords = (loc.latitude, loc.longitude)
            else:
                messagebox.showerror("Map Error", "Location not found. Using default.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not geocode location:\n{e}")

    # Fallback default (Nairobi)
    if not coords:
        coords = (-1.286389, 36.817223)

    m = folium.Map(location=coords, zoom_start=13)
    folium.Marker(coords, tooltip="Reported Disaster", popup=location_name).add_to(m)
    map_path = "disaster_map.html"
    m.save(map_path)
    webbrowser.open(map_path)

# GUI Setup
root = tk.Tk()
root.title("Rapid Response Hub")
root.geometry("420x620")

selected_image_path = tk.StringVar()

# UI Layout
tk.Label(root, text="Rapid Response Hub", font=("Arial", 18, "bold")).pack(pady=10)

tk.Label(root, text="Disaster Type:").pack()
disaster_type = tk.Entry(root, width=40)
disaster_type.pack(pady=5)

tk.Label(root, text="Location:").pack()
location = tk.Entry(root, width=40)
location.pack(pady=5)
tk.Button(root, text="Use My Location", command=get_user_location).pack(pady=2)

tk.Label(root, text="Description:").pack()
description = tk.Text(root, height=5, width=40)
description.pack(pady=5)

tk.Button(root, text="Select Photo", command=choose_photo).pack(pady=5)

tk.Button(root, text="Submit Report", command=save_report, bg="green", fg="white").pack(pady=10)
tk.Button(root, text="View Past Reports", command=view_reports, bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white").pack(pady=10)

root.mainloop()

