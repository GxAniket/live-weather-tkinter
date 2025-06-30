# By Aniket ❤️
import threading
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from io import BytesIO
from PIL import Image, ImageTk

# ─────────────────────────────────────────────
# 🔐 1. API Key
# ─────────────────────────────────────────────
API_KEY = ""  # Add your OpenWeatherMap API key here

# ─────────────────────────────────────────────
# 🌐 2. API Function
# ─────────────────────────────────────────────
def fetch_weather(city: str) -> dict:
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

# ─────────────────────────────────────────────
# 🖼️ 3. Update UI
# ─────────────────────────────────────────────
def update_ui(payload: dict) -> None:
    if "error" in payload:
        result_lbl.config(text=payload["error"])
        icon_lbl.config(image=""); icon_lbl.image = None
        return

    if payload.get("cod") == 200:
        city = payload["name"]
        temp = payload["main"]["temp"]
        desc = payload["weather"][0]["description"].title()
        result_lbl.config(text=f"{city}: {temp:.1f}°C, {desc}")

        icon_id = payload["weather"][0]["icon"]
        icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
        try:
            img_data = requests.get(icon_url, timeout=3).content
            img = Image.open(BytesIO(img_data)).resize((64, 64), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            icon_lbl.config(image=photo); icon_lbl.image = photo
        except Exception:
            icon_lbl.config(image=""); icon_lbl.image = None

    elif payload.get("cod") == "404":
        result_lbl.config(text="City not found.")
        icon_lbl.config(image=""); icon_lbl.image = None
    else:
        result_lbl.config(text=f"API error: {payload.get('message', 'Unknown error')}")
        icon_lbl.config(image=""); icon_lbl.image = None

# ─────────────────────────────────────────────
# 📥 4. Search Handler
# ─────────────────────────────────────────────
def on_get_weather() -> None:
    city = city_var.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    result_lbl.config(text="Fetching...")
    icon_lbl.config(image=""); icon_lbl.image = None

    threading.Thread(
        target=lambda: root.after(0, update_ui, fetch_weather(city)),
        daemon=True
    ).start()

# ─────────────────────────────────────────────
# 🧱 5. GUI Setup (Dark Mode)
# ─────────────────────────────────────────────
root = tk.Tk()
root.title("Weather Now – Dark Mode by Aniket ❤️")
root.geometry("480x460")
root.resizable(False, False)
root.configure(bg="#1e1e2f")  # Dark background

# 🛠️ ttk Styles
style = ttk.Style(root)
style.theme_use("clam")

# Custom dark mode colors
DARK_BG = "#2b2b3d"  # Dark background for cards
LIGHT_TEXT = "#f2f2f2" # Light text color
ACCENT = "#4db8ff" # Accent color for highlights

# Style configuration
style.configure("Card.TFrame", background=DARK_BG, relief="solid", borderwidth=2)
style.configure("Card.TLabel", background=DARK_BG, foreground=LIGHT_TEXT, font=("Segoe UI", 11))
style.configure("Title.TLabel", background=DARK_BG, foreground=ACCENT, font=("Segoe UI", 14, "bold"))
style.configure("Card.TButton", font=("Segoe UI", 11), padding=6, background=DARK_BG, foreground=LIGHT_TEXT)
style.configure("Result.TFrame", background="#33394d", relief="solid", borderwidth=1)
style.configure("Result.TLabel", background="#33394d", foreground="white", font=("Segoe UI", 12, "bold"))

# Main Card Frame
card = ttk.Frame(root, padding=25, style="Card.TFrame")
card.place(relx=0.5, rely=0.5, anchor="center")

# Title
ttk.Label(card, text="🌙 Weather Now", style="Title.TLabel") \
    .grid(row=0, column=0, columnspan=2, pady=(0, 15))

# Input field
ttk.Label(card, text="Enter City:", style="Card.TLabel") \
    .grid(row=1, column=0, sticky="w")
city_var = tk.StringVar()
city_ent = ttk.Entry(card, textvariable=city_var, width=25)
city_ent.grid(row=2, column=0, padx=(0, 12), pady=(4, 15))
city_ent.focus()

# Get Weather Button
get_btn = ttk.Button(card, text="Get Weather", style="Card.TButton", command=on_get_weather)
get_btn.grid(row=2, column=1, pady=(4, 15))

# Weather Result Frame
result_frame = ttk.Frame(card, style="Result.TFrame", padding=10)
result_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

icon_lbl = ttk.Label(result_frame, style="Result.TLabel")
result_lbl = ttk.Label(result_frame, text="", style="Result.TLabel", wraplength=260)

icon_lbl.grid(row=0, column=0, padx=(0, 10))
result_lbl.grid(row=0, column=1, sticky="w")

# Footer Credit
footer = tk.Label(root, text="Created by Aniket ❤️",
                  font=("Segoe UI", 9), bg="#1e1e2f", fg="#aaaaaa")
footer.pack(side="bottom", pady=5)

# Bind Enter key
root.bind("<Return>", lambda e: on_get_weather())

# Start the app
root.mainloop()