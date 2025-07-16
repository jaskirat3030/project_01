import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    'Date': pd.date_range(start='2025-08-01', periods=10),
    'PM2.5': [35, 60, 110, 140, 190, 230, 65, 50, 175, 85],
    'PM10': [90, 140, 200, 170, 195, 280, 110, 85, 240, 150],
    'NO2': [55, 65, 80, 78, 88, 92, 45, 42, 79, 75]
}
df = pd.DataFrame(data)

thresholds = {'PM2.5': 100, 'PM10': 200, 'NO2': 80}

def calculate_aqi_pm25(pm25):
    if pm25 <= 50: return 1
    elif pm25 <= 100: return 2
    elif pm25 <= 150: return 3
    elif pm25 <= 200: return 4
    elif pm25 <= 300: return 5
    else: return 6

aqi_category = {
    1: "Good",
    2: "Moderate",
    3: "Unhealthy for Sensitive Groups",
    4: "Unhealthy",
    5: "Very Unhealthy",
    6: "Hazardous"
}

def check_alerts(row):
    alerts = []
    for pollutant, limit in thresholds.items():
        if row[pollutant] > limit:
            alerts.append(f"{pollutant} High")
    return ", ".join(alerts) if alerts else "Safe"

df['Alert'] = df.apply(check_alerts, axis=1)
df['AQI'] = df['PM2.5'].apply(calculate_aqi_pm25)
df['AQI Category'] = df['AQI'].map(aqi_category)

health_advice = {
    "Good": "Air quality is satisfactory. Enjoy your usual outdoor activities.",
    "Moderate": "Air quality is acceptable. Sensitive groups should take care.",
    "Unhealthy for Sensitive Groups": "Sensitive groups should reduce prolonged outdoor exertion.",
    "Unhealthy": "Everyone may begin to experience health effects. Limit outdoor activities.",
    "Very Unhealthy": "Health warnings of emergency conditions. Avoid outdoor activities.",
    "Hazardous": "Serious health effects. Stay indoors and keep windows closed."
}

class AirQualityApp:
    def __init__(self, root):
        self.root = root
        root.title("🌍 AQI SmartScope")
        root.geometry("760x520")
        root.configure(bg="#f0f8ff") 

        self.name_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="AQI SmartScope", font=("Helvetica", 20, "bold"),
                               bg="#f0f8ff", fg="#003366")
        title_label.pack(pady=15)

        input_frame = tk.Frame(self.root, bg="#f0f8ff")
        input_frame.pack()

        tk.Label(input_frame, text="Enter your name:", bg="#f0f8ff", font=("Helvetica", 14)).pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(input_frame, textvariable=self.name_var, font=("Helvetica", 14), width=25)
        self.name_entry.pack(side=tk.LEFT)
        self.name_entry.focus()

        frame = tk.Frame(self.root, bg="#f0f8ff")
        frame.pack(pady=25)

        btn_config = {
            "font": ("Helvetica", 14),
            "bg": "#cce7ff",
            "fg": "#003366",
            "activebackground": "#b3d9ff",
            "width": 28,
            "height": 2,
            "relief": "raised",
            "bd": 3
        }

        btn1 = tk.Button(frame, text="Check Air Quality by Date", command=self.check_by_date, **btn_config)
        btn2 = tk.Button(frame, text="Show Pollutant Stats", command=self.show_stats, **btn_config)
        btn3 = tk.Button(frame, text="Pollutant Comparison", command=self.pollutant_comparison, **btn_config)
        btn4 = tk.Button(frame, text="Show Summary", command=self.show_summary, **btn_config)
        btn5 = tk.Button(frame, text="Show Heatmap", command=self.show_heatmap, **btn_config)
        btn6 = tk.Button(frame, text="Exit", command=self.root.quit,
                         font=("Helvetica", 14), bg="#ff6666", fg="white",
                         activebackground="#ff4d4d", width=28, height=2, relief="raised", bd=3)

        btn1.grid(row=0, column=0, padx=10, pady=10)
        btn2.grid(row=0, column=1, padx=10, pady=10)
        btn3.grid(row=1, column=0, padx=10, pady=10)
        btn4.grid(row=1, column=1, padx=10, pady=10)
        btn5.grid(row=2, column=0, padx=10, pady=10)
        btn6.grid(row=2, column=1, padx=10, pady=10)

    def check_name(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter your name first.")
            return None
        return name.title()

    def check_by_date(self):
        name = self.check_name()
        if not name:
            return
        date_str = simpledialog.askstring("Input Date", f"{name}, enter date (YYYY-MM-DD):", parent=self.root)
        if not date_str:
            return

        try:
            date = pd.to_datetime(date_str).date()
        except:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return

        row = df[df['Date'].dt.date == date]
        if row.empty:
            messagebox.showinfo("No Data", f"No air quality data available for {date}.")
            return
        row = row.iloc[0]

        msg = (
            f"👋 Hello, {name}!\n\n"
            f"Date: {row['Date'].date()}\n"
            f"PM2.5: {row['PM2.5']} μg/m³\n"
            f"PM10: {row['PM10']} μg/m³\n"
            f"NO2: {row['NO2']} μg/m³\n"
            f"Alert Status: {row['Alert']}\n"
            f"AQI Category: {row['AQI Category']}"
        )
        messagebox.showinfo("Air Quality Data", msg)

    def show_stats(self):
        name = self.check_name()
        if not name:
            return

        mean_vals = df[['PM2.5', 'PM10', 'NO2']].mean()
        max_vals = df[['PM2.5', 'PM10', 'NO2']].max()
        min_vals = df[['PM2.5', 'PM10', 'NO2']].min()

        msg = (f"👋 Hello, {name}!\n\nPollutant Statistics Over All Dates:\n\n"
               f"Mean Levels:\nPM2.5: {mean_vals['PM2.5']:.1f}, PM10: {mean_vals['PM10']:.1f}, NO2: {mean_vals['NO2']:.1f}\n\n"
               f"Max Levels:\nPM2.5: {max_vals['PM2.5']}, PM10: {max_vals['PM10']}, NO2: {max_vals['NO2']}\n\n"
               f"Min Levels:\nPM2.5: {min_vals['PM2.5']}, PM10: {min_vals['PM10']}, NO2: {min_vals['NO2']}")
        messagebox.showinfo("Pollutant Stats", msg)

    def pollutant_comparison(self):
        name = self.check_name()
        if not name:
            return

        date_str = simpledialog.askstring("Input Date", f"{name}, enter date (YYYY-MM-DD) for pollutant comparison:", parent=self.root)
        if not date_str:
            return

        try:
            date = pd.to_datetime(date_str).date()
        except:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return

        row = df[df['Date'].dt.date == date]
        if row.empty:
            messagebox.showinfo("No Data", f"No air quality data available for {date}.")
            return
        row = row.iloc[0]

        pollutants = ['PM2.5', 'PM10', 'NO2']
        highest_pollutant = max(pollutants, key=lambda p: row[p])
        highest_value = row[highest_pollutant]

        msg = (f"👋 Hello, {name}!\n\nOn {date}, the highest pollutant level was:\n\n"
               f"{highest_pollutant}: {highest_value} μg/m³\n\n"
               f"Alert Status: {row['Alert']}\nAQI Category: {row['AQI Category']}")
        messagebox.showinfo("Pollutant Comparison", msg)

    def show_summary(self):
        name = self.check_name()
        if not name:
            return

        alerts_summary = df['Alert'].value_counts().to_string()
        aqi_summary = df['AQI Category'].value_counts().to_string()

        message = (f"👋 Hello, {name}!\n\n📋 Alerts Summary:\n{alerts_summary}"
                   f"\n\n📊 AQI Category Summary:\n{aqi_summary}")
        messagebox.showinfo("Summary Report", message)

    def show_heatmap(self):
        name = self.check_name()
        if not name:
            return

        fig, ax = plt.subplots(figsize=(6, 5))
        sns.heatmap(df[['PM2.5', 'PM10', 'NO2']].corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title(f"Pollutant Correlations for {name}")
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AirQualityApp(root)
    root.mainloop()
