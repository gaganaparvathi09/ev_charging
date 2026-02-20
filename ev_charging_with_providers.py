import tkinter as tk
from tkinter import ttk, messagebox, font
import requests
import math
from datetime import datetime
import threading
import webbrowser
from typing import List, Dict, Optional
import folium
import os
import tempfile
import json

class EVChargingWithProviders:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ EV Charging Station Finder - Kerala")
        self.root.geometry("1250x850")
        self.root.configure(bg='#1e1e1e')
        
        self.setup_styles()
        self.init_data()
        self.create_main_ui()
        self.load_all_stations()
        self.auto_detect_location()
    
    def setup_styles(self):
        self.colors = {
            'bg': '#1e1e1e', 'card': '#2d2d2d', 'accent': '#00ff88',
            'secondary': '#4a9eff', 'text': '#ffffff', 'text_secondary': '#b0b0b0',
            'success': '#00ff88', 'warning': '#ffaa00', 'error': '#ff4444', 'border': '#404040'
        }
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'), 'heading': ('Segoe UI', 16, 'bold'),
            'normal': ('Segoe UI', 11), 'small': ('Segoe UI', 9), 'button': ('Segoe UI', 10, 'bold')
        }
    
    def init_data(self):
        self.current_lat = None
        self.current_lon = None
        self.stations = []
        self.filtered_stations = []
        self.providers_file = 'providers.json'
        self.load_providers()
    
    def load_providers(self):
        try:
            if os.path.exists(self.providers_file):
                with open(self.providers_file, 'r') as f:
                    self.registered_providers = json.load(f)
            else:
                self.registered_providers = []
        except:
            self.registered_providers = []
    
    def save_providers(self):
        try:
            with open(self.providers_file, 'w') as f:
                json.dump(self.registered_providers, f, indent=2)
        except:
            pass
    
    def create_main_ui(self):
        self.create_header()
        self.create_main_container()
    
    def create_header(self):
        header = tk.Frame(self.root, bg='#0d1117', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="⚡ EV Charging Station Finder", 
                font=self.fonts['title'], fg=self.colors['accent'], bg='#0d1117').pack(side='left', padx=30, pady=20)
        
        # Add register button in header
        self.register_btn = tk.Button(header, text="➕ REGISTER AS PROVIDER", 
                                   font=('Segoe UI', 10, 'bold'), fg='#000000', bg='#ff6b35',
                                   activebackground='#e55a2b', activeforeground='#000000',
                                   relief='raised', bd=3, padx=15, pady=8,
                                   command=self.open_provider_registration)
        self.register_btn.pack(side='left', padx=(30, 10), pady=20)
        
        # Add map button in header
        self.map_btn = tk.Button(header, text="🗺️ SHOW MAP", 
                               font=('Segoe UI', 10, 'bold'), fg='#000000', bg='#00ff88',
                               activebackground='#00cc6a', activeforeground='#000000',
                               relief='raised', bd=3, padx=15, pady=8,
                               command=self.show_map)
        self.map_btn.pack(side='left', padx=(0, 20), pady=20)
        
        self.status_indicator = tk.Label(header, text="🟢 Online", 
                                      font=self.fonts['normal'], fg=self.colors['success'], bg='#0d1117')
        self.status_indicator.pack(side='right', padx=30, pady=20)
    
    def create_main_container(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Left panel
        left_panel = tk.Frame(main_container, bg=self.colors['card'], width=420)
        left_panel.pack(side='left', fill='y', padx=(0, 20))
        left_panel.pack_propagate(False)
        
        self.create_location_card(left_panel)
        self.create_filters_card(left_panel)
        self.create_action_buttons(left_panel)
        
        # Right panel
        right_panel = tk.Frame(main_container, bg=self.colors['card'])
        right_panel.pack(side='left', fill='both', expand=True)
        
        self.create_results_panel(right_panel)
        self.create_status_bar()
    
    def create_location_card(self, parent):
        location_frame = tk.LabelFrame(parent, text="📍 Location", 
                                    font=self.fonts['heading'], fg=self.colors['text'], 
                                    bg=self.colors['card'], borderwidth=1, relief='solid')
        location_frame.pack(fill='x', padx=20, pady=20)
        
        self.location_display = tk.Label(location_frame, text="Detecting location...", 
                                      font=self.fonts['normal'], fg=self.colors['text_secondary'], 
                                      bg=self.colors['card'], wraplength=350)
        self.location_display.pack(padx=15, pady=10)
        
        self.detect_btn = tk.Button(location_frame, text="🔄 Detect My Location", 
                                  font=self.fonts['button'], fg='#000000', bg=self.colors['accent'],
                                  command=self.detect_location)
        self.detect_btn.pack(padx=15, pady=10, fill='x')
        
        # Manual coordinates
        coord_frame = tk.Frame(location_frame, bg=self.colors['card'])
        coord_frame.pack(padx=15, pady=10)
        
        tk.Label(coord_frame, text="Manual Coordinates:", 
                font=self.fonts['small'], fg=self.colors['text_secondary'], bg=self.colors['card']).pack(anchor='w')
        
        coord_input = tk.Frame(coord_frame, bg=self.colors['card'])
        coord_input.pack(fill='x', pady=5)
        
        tk.Label(coord_input, text="Lat:", font=self.fonts['small'], 
                fg=self.colors['text'], bg=self.colors['card']).pack(side='left')
        self.lat_entry = tk.Entry(coord_input, font=self.fonts['small'], 
                                bg='#404040', fg=self.colors['text'])
        self.lat_entry.pack(side='left', padx=(5, 15))
        
        tk.Label(coord_input, text="Lon:", font=self.fonts['small'], 
                fg=self.colors['text'], bg=self.colors['card']).pack(side='left')
        self.lon_entry = tk.Entry(coord_input, font=self.fonts['small'], 
                                bg='#404040', fg=self.colors['text'])
        self.lon_entry.pack(side='left', padx=5)
    
    def create_filters_card(self, parent):
        filter_frame = tk.LabelFrame(parent, text="🔍 Search Filters", 
                                  font=self.fonts['heading'], fg=self.colors['text'], 
                                  bg=self.colors['card'], borderwidth=1, relief='solid')
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Radius
        tk.Label(filter_frame, text="Search Radius:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.radius_var = tk.DoubleVar(value=25.0)
        radius_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        radius_frame.pack(fill='x', padx=15, pady=5)
        
        self.radius_slider = tk.Scale(radius_frame, from_=1, to=50, orient='horizontal',
                                   variable=self.radius_var, bg=self.colors['card'], fg=self.colors['text'],
                                   troughcolor='#404040', activebackground=self.colors['accent'],
                                   highlightthickness=0, length=250)
        self.radius_slider.pack(side='left')
        
        self.radius_label = tk.Label(radius_frame, text="25 km", 
                                   font=self.fonts['normal'], fg=self.colors['accent'], bg=self.colors['card'])
        self.radius_label.pack(side='left', padx=10)
        
        def update_radius_label(val):
            self.radius_label.config(text=f"{float(val):.0f} km")
        self.radius_slider.config(command=update_radius_label)
        
        # Access type
        tk.Label(filter_frame, text="Access Type:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.access_var = tk.StringVar(value="all")
        access_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        access_frame.pack(fill='x', padx=15, pady=5)
        
        access_types = [("All Stations", "all"), ("🏢 Public", "public"), ("🏠 Private", "private"), ("👤 Registered Providers", "provider")]
        for text, value in access_types:
            rb = tk.Radiobutton(access_frame, text=text, variable=self.access_var, value=value,
                               font=self.fonts['small'], fg=self.colors['text'], bg=self.colors['card'],
                               selectcolor=self.colors['accent'])
            rb.pack(anchor='w')
        
        # Power type
        tk.Label(filter_frame, text="Power Type:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.power_var = tk.StringVar(value="all")
        power_combo = ttk.Combobox(filter_frame, textvariable=self.power_var, 
                                  values=["all", "Type 2", "CCS", "CHAdeMO"], 
                                  state="readonly", width=20)
        power_combo.pack(padx=15, pady=5, fill='x')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='#404040', background='#404040', 
                      foreground=self.colors['text'])
    
    def create_action_buttons(self, parent):
        button_frame = tk.Frame(parent, bg=self.colors['card'])
        button_frame.pack(fill='x', padx=12, pady=10)
        
        # Add instruction label for providers
        instruction_label = tk.Label(button_frame, text="👤 Want to register? Use button in top header!", 
                                 font=('Segoe UI', 8), fg=self.colors['text_secondary'], bg=self.colors['card'])
        instruction_label.pack(pady=(0, 8))
        
        # Separator line
        separator = tk.Frame(button_frame, height=1, bg=self.colors['border'])
        separator.pack(fill='x', pady=(0, 8))
        
        # Make search button the main action in left panel
        self.search_btn = tk.Button(button_frame, text="🔍 SEARCH STATIONS", 
                                  font=('Segoe UI', 12, 'bold'), fg='#000000', bg='#4a9eff',
                                  activebackground='#3a8eef', activeforeground='#000000',
                                  relief='raised', bd=3, padx=12, pady=12,
                                  command=self.search_stations)
        self.search_btn.pack(fill='x', pady=(0, 8))
        
        # Add note about map button
        map_note = tk.Label(button_frame, text="🗺️ Map button is available in top header", 
                          font=('Segoe UI', 8), fg=self.colors['text_secondary'], bg=self.colors['card'])
        map_note.pack(pady=(0, 8))
    
    def create_filters_card(self, parent):
        filter_frame = tk.LabelFrame(parent, text="🔍 Search Filters", 
                                  font=self.fonts['heading'], fg=self.colors['text'], 
                                  bg=self.colors['card'], borderwidth=1, relief='solid')
        filter_frame.pack(fill='x', padx=20, pady=10)
        
        # Radius
        tk.Label(filter_frame, text="Search Radius:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.radius_var = tk.DoubleVar(value=25.0)
        radius_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        radius_frame.pack(fill='x', padx=15, pady=5)
        
        self.radius_slider = tk.Scale(radius_frame, from_=1, to=50, orient='horizontal',
                                   variable=self.radius_var, bg=self.colors['card'], fg=self.colors['text'],
                                   troughcolor='#404040', activebackground=self.colors['accent'],
                                   highlightthickness=0, length=250)
        self.radius_slider.pack(side='left')
        
        self.radius_label = tk.Label(radius_frame, text="25 km", 
                                   font=self.fonts['normal'], fg=self.colors['accent'], bg=self.colors['card'])
        self.radius_label.pack(side='left', padx=10)
        
        # Access type
        tk.Label(filter_frame, text="Access Type:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.access_var = tk.StringVar(value="all")
        access_frame = tk.Frame(filter_frame, bg=self.colors['card'])
        access_frame.pack(fill='x', padx=15, pady=5)
        
        access_types = [("All Stations", "all"), ("🏢 Public", "public"), ("🏠 Private", "private"), ("👤 Registered Providers", "provider")]
        for text, value in access_types:
            rb = tk.Radiobutton(access_frame, text=text, variable=self.access_var, value=value,
                               font=self.fonts['small'], fg=self.colors['text'], bg=self.colors['card'],
                               selectcolor=self.colors['accent'])
            rb.pack(anchor='w')
        
        # Power type
        tk.Label(filter_frame, text="Power Type:", 
                font=self.fonts['normal'], fg=self.colors['text'], bg=self.colors['card']).pack(anchor='w', padx=15, pady=(15, 5))
        
        self.power_var = tk.StringVar(value="all")
        power_combo = ttk.Combobox(filter_frame, textvariable=self.power_var, 
                                  values=["all", "Type 2", "CCS", "CHAdeMO"], 
                                  state="readonly", width=20)
        power_combo.pack(padx=15, pady=5, fill='x')
        
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TCombobox', fieldbackground='#404040', background='#404040', 
                      foreground=self.colors['text'])
    
    def create_results_panel(self, parent):
        # Results header
        results_header = tk.Frame(parent, bg=self.colors['card'], height=60)
        results_header.pack(fill='x', padx=20, pady=(20, 10))
        results_header.pack_propagate(False)
        
        tk.Label(results_header, text="🔋 Charging Stations", 
                font=self.fonts['heading'], fg=self.colors['text'], bg=self.colors['card']).pack(side='left', pady=15)
        
        self.results_count = tk.Label(results_header, text="0 stations found", 
                                   font=self.fonts['normal'], fg=self.colors['text_secondary'], bg=self.colors['card'])
        self.results_count.pack(side='right', pady=15)
        
        # Results list
        canvas = tk.Canvas(parent, bg=self.colors['card'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        self.results_frame = tk.Frame(canvas, bg=self.colors['card'])
        
        self.results_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))
        
        self.show_empty_state()
    
    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="🚀 Initializing...", 
                                font=self.fonts['small'], fg=self.colors['text_secondary'], 
                                bg=self.colors['bg'], relief='flat', anchor='w')
        self.status_bar.pack(side='bottom', fill='x', padx=20, pady=(0, 10))
    
    def show_empty_state(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        empty_frame = tk.Frame(self.results_frame, bg=self.colors['card'])
        empty_frame.pack(expand=True, fill='both', pady=100)
        
        tk.Label(empty_frame, text="🔋", font=('Segoe UI', 48), 
                fg=self.colors['text_secondary'], bg=self.colors['card']).pack()
        tk.Label(empty_frame, text="No stations found", 
                font=self.fonts['heading'], fg=self.colors['text_secondary'], bg=self.colors['card']).pack(pady=10)
        tk.Label(empty_frame, text="Register as a provider or search for nearby stations", 
                font=self.fonts['normal'], fg=self.colors['text_secondary'], bg=self.colors['card']).pack()
    
    def load_all_stations(self):
        # Public stations
        public_stations = [
            {"id": 1, "name": "Tesla Supercharger - Kochi", "address": "MG Road, Ernakulam", 
             "latitude": 9.9312, "longitude": 76.2673, "total_slots": 8, "available_slots": 3, 
             "power_types": ["Type 2", "CCS", "CHAdeMO"], "max_power": 250, "price_per_kwh": 0.28, 
             "status": "open", "access_type": "public", "owner_type": "commercial", "operating_hours": "24/7"},
            
            {"id": 2, "name": "ChargePoint Station - Lulu Mall", "address": "Lulu Mall, Edappally, Kochi", 
             "latitude": 9.9836, "longitude": 76.2855, "total_slots": 4, "available_slots": 2, 
             "power_types": ["Type 2", "CCS"], "max_power": 150, "price_per_kwh": 0.32, 
             "status": "open", "access_type": "public", "owner_type": "commercial", "operating_hours": "10AM-10PM"},
            
            {"id": 3, "name": "EVgo Station - Cochin Airport", "address": "Cochin International Airport, Nedumbassery", 
             "latitude": 10.1518, "longitude": 76.4019, "total_slots": 6, "available_slots": 1, 
             "power_types": ["CCS", "CHAdeMO"], "max_power": 350, "price_per_kwh": 0.35, 
             "status": "open", "access_type": "public", "owner_type": "commercial", "operating_hours": "24/7"},
            
            {"id": 4, "name": "Public Charging - Kalady Town", "address": "Near Sree Sankara Temple, Kalady", 
             "latitude": 9.7480, "longitude": 76.4880, "total_slots": 4, "available_slots": 2, 
             "power_types": ["Type 2", "CCS"], "max_power": 50, "price_per_kwh": 0.22, 
             "status": "open", "access_type": "public", "owner_type": "commercial", "operating_hours": "8AM-8PM"}
        ]
        
        # Add registered providers
        provider_stations = []
        for provider in self.registered_providers:
            provider_stations.append({
                "id": provider["id"], 
                "name": provider["name"], 
                "address": provider["address"],
                "latitude": provider["latitude"], 
                "longitude": provider["longitude"],
                "total_slots": provider["total_slots"], 
                "available_slots": provider["available_slots"],
                "power_types": provider["power_types"], 
                "max_power": provider["max_power"],
                "price_per_kwh": provider["price_per_kwh"], 
                "status": provider["status"],
                "access_type": "provider", 
                "owner_type": "provider",
                "operating_hours": provider["operating_hours"],
                "contact_info": provider.get("contact_info", ""),
                "pricing_model": provider.get("pricing_model", "per_kwh"),
                "time_limits": provider.get("time_limits", "no_limit")
            })
        
        self.stations = public_stations + provider_stations
        self.status_bar.config(text=f"✅ Loaded {len(self.stations)} charging stations ({len(provider_stations)} from providers)")
        
        # Auto-search stations immediately after loading
        self.root.after(500, self.auto_search_stations)
    
    def auto_detect_location(self):
        # Set default location to Kerala immediately
        self.current_lat = 9.9312  # Kochi
        self.current_lon = 76.2673
        self.lat_entry.delete(0, tk.END)
        self.lat_entry.insert(0, str(self.current_lat))
        self.lon_entry.delete(0, tk.END)
        self.lon_entry.insert(0, str(self.current_lon))
        self.location_display.config(text="📍 Kochi, Kerala (Default)", fg=self.colors['success'])
        self.status_bar.config(text="✅ Using Kochi, Kerala as default location")
        
        # Auto-search stations
        threading.Thread(target=self.detect_location, daemon=True).start()
        
    def auto_search_stations(self):
        """Automatically search for stations using default location"""
        try:
            if self.current_lat and self.current_lon:
                radius = self.radius_var.get()
                
                nearby_stations = []
                for station in self.stations:
                    distance = self.calculate_distance(self.current_lat, self.current_lon, station['latitude'], station['longitude'])
                    if distance <= radius and station['available_slots'] > 0:
                        station_copy = station.copy()
                        station_copy['distance_km'] = round(distance, 2)
                        nearby_stations.append(station_copy)
                
                nearby_stations.sort(key=lambda x: x['distance_km'])
                self.filtered_stations = nearby_stations
                self.apply_filters()
                
                self.status_bar.config(text=f"🔍 Found {len(nearby_stations)} stations within {radius} km")
        except Exception as e:
            self.status_bar.config(text=f"❌ Auto-search failed: {str(e)}")
    
    def detect_location(self):
        def update_ui(text, color=None):
            if color:
                self.location_display.config(text=text, fg=color)
            else:
                self.location_display.config(text=text)
        
        update_ui("🔄 Detecting your location...", self.colors['warning'])
        self.detect_btn.config(text="🔄 Detecting...", state='disabled')
        
        def detect():
            try:
                services = ['https://ipinfo.io/json', 'https://ipapi.co/json/']
                location_data = None
                
                for service in services:
                    try:
                        response = requests.get(service, timeout=5)
                        if response.status_code == 200:
                            location_data = response.json()
                            break
                    except:
                        continue
                
                if location_data and 'loc' in location_data:
                    lat, lon = location_data['loc'].split(',')
                    self.current_lat = float(lat)
                    self.current_lon = float(lon)
                    city = location_data.get('city', 'Unknown')
                    country = location_data.get('country', 'Unknown')
                    
                    location_text = f"📍 {city}, {country}"
                    self.root.after(0, lambda: update_ui(location_text, self.colors['success']))
                    self.root.after(0, lambda: self.lat_entry.delete(0, tk.END))
                    self.root.after(0, lambda: self.lat_entry.insert(0, str(self.current_lat)))
                    self.root.after(0, lambda: self.lon_entry.delete(0, tk.END))
                    self.root.after(0, lambda: self.lon_entry.insert(0, str(self.current_lon)))
                    self.root.after(0, lambda: self.status_bar.config(text=f"✅ Location detected: {city}, {country}"))
                else:
                    raise Exception("No location data received")
                    
            except Exception as e:
                self.root.after(0, lambda: update_ui("❌ Location detection failed", self.colors['error']))
            
            self.root.after(0, lambda: self.detect_btn.config(text="🔄 Detect My Location", state='normal'))
        
        threading.Thread(target=detect, daemon=True).start()
    
    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
    
    def search_stations(self):
        try:
            lat = float(self.lat_entry.get()) if self.lat_entry.get() else self.current_lat
            lon = float(self.lon_entry.get()) if self.lon_entry.get() else self.current_lon
            
            if lat is None or lon is None:
                messagebox.showwarning("Location Required", "Please detect location or enter coordinates")
                return
            
            radius = self.radius_var.get()
            
            nearby_stations = []
            for station in self.stations:
                distance = self.calculate_distance(lat, lon, station['latitude'], station['longitude'])
                if distance <= radius and station['available_slots'] > 0:
                    station_copy = station.copy()
                    station_copy['distance_km'] = round(distance, 2)
                    nearby_stations.append(station_copy)
            
            nearby_stations.sort(key=lambda x: x['distance_km'])
            self.filtered_stations = nearby_stations
            self.apply_filters()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid coordinates")
    
    def apply_filters(self):
        filtered = self.filtered_stations.copy()
        
        access_type = self.access_var.get()
        if access_type != "all":
            filtered = [s for s in filtered if s.get('access_type') == access_type]
        
        power_type = self.power_var.get()
        if power_type != "all":
            filtered = [s for s in filtered if power_type in s.get('power_types', [])]
        
        self.display_results(filtered)
    
    def display_results(self, stations):
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        if not stations:
            self.show_empty_state()
            self.results_count.config(text="0 stations found")
            return
        
        self.results_count.config(text=f"{len(stations)} stations found")
        
        for i, station in enumerate(stations):
            self.create_station_card(station, i)
    
    def create_station_card(self, station, index):
        card = tk.Frame(self.results_frame, bg='#3a3a3a', relief='flat', borderwidth=1)
        card.pack(fill='x', padx=20, pady=10)
        
        header_frame = tk.Frame(card, bg='#3a3a3a')
        header_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        icon_map = {"public": "🏢", "private": "🏠", "provider": "👤"}
        icon = icon_map.get(station.get('access_type'), "🔋")
        
        name_label = tk.Label(header_frame, text=f"{icon} {station['name']}", 
                            font=self.fonts['heading'], fg=self.colors['text'], bg='#3a3a3a')
        name_label.pack(side='left')
        
        distance_badge = tk.Label(header_frame, text=f"{station['distance_km']} km", 
                                font=self.fonts['button'], fg='#000000', bg=self.colors['accent'],
                                relief='flat')
        distance_badge.pack(side='right')
        
        address_label = tk.Label(card, text=f"📍 {station['address']}", 
                               font=self.fonts['normal'], fg=self.colors['text_secondary'], bg='#3a3a3a')
        address_label.pack(anchor='w', padx=15, pady=(0, 5))
        
        details_frame = tk.Frame(card, bg='#3a3a3a')
        details_frame.pack(fill='x', padx=15, pady=(0, 10))
        
        row1 = tk.Frame(details_frame, bg='#3a3a3a')
        row1.pack(fill='x', pady=2)
        
        tk.Label(row1, text=f"🔌 {station['available_slots']}/{station['total_slots']} slots", 
                font=self.fonts['small'], fg=self.colors['success'], bg='#3a3a3a').pack(side='left', padx=(0, 20))
        tk.Label(row1, text=f"⚡ {station['max_power']} kW", 
                font=self.fonts['small'], fg=self.colors['text'], bg='#3a3a3a').pack(side='left', padx=(0, 20))
        tk.Label(row1, text=f"💰 ${station['price_per_kwh']}/kWh", 
                font=self.fonts['small'], fg=self.colors['text'], bg='#3a3a3a').pack(side='left')
        
        row2 = tk.Frame(details_frame, bg='#3a3a3a')
        row2.pack(fill='x', pady=2)
        
        tk.Label(row2, text=f"🔧 {', '.join(station['power_types'])}", 
                font=self.fonts['small'], fg=self.colors['text_secondary'], bg='#3a3a3a').pack(side='left', padx=(0, 20))
        tk.Label(row2, text=f"⏰ {station.get('operating_hours', 'Unknown')}", 
                font=self.fonts['small'], fg=self.colors['text_secondary'], bg='#3a3a3a').pack(side='left')
        
        # Provider specific info
        if station.get('access_type') == 'provider':
            provider_frame = tk.Frame(card, bg='#2a2a2a')
            provider_frame.pack(fill='x', padx=15, pady=(0, 15))
            
            tk.Label(provider_frame, text="👤 Registered Provider", 
                    font=self.fonts['small'], fg=self.colors['warning'], bg='#2a2a2a').pack(anchor='w')
            
            if station.get('contact_info'):
                tk.Label(provider_frame, text=f"📞 {station['contact_info']}", 
                        font=self.fonts['small'], fg=self.colors['text_secondary'], bg='#2a2a2a').pack(anchor='w')
            
            if station.get('pricing_model'):
                tk.Label(provider_frame, text=f"💳 Pricing: {station['pricing_model']}", 
                        font=self.fonts['small'], fg=self.colors['text_secondary'], bg='#2a2a2a').pack(anchor='w')
            
            if station.get('time_limits'):
                tk.Label(provider_frame, text=f"⏱️ Time Limit: {station['time_limits']}", 
                        font=self.fonts['small'], fg=self.colors['text_secondary'], bg='#2a2a2a').pack(anchor='w')
    
    def show_map(self):
        if not self.filtered_stations:
            messagebox.showinfo("No Stations", "Please search for stations first")
            return
        
        try:
            lat = self.current_lat or 9.9312
            lon = self.current_lon or 76.2673
            
            m = folium.Map(location=[lat, lon], zoom_start=12)
            
            folium.Marker([lat, lon], popup="Your Location",
                         icon=folium.Icon(color='blue', icon='user', prefix='fa')).add_to(m)
            
            for station in self.filtered_stations:
                color_map = {"public": "green", "private": "orange", "provider": "purple"}
                color = color_map.get(station.get('access_type'), "blue")
                
                popup_html = f"""
                <b>{station['name']}</b><br>
                {station['address']}<br>
                Distance: {station['distance_km']} km<br>
                Available: {station['available_slots']}/{station['total_slots']} slots<br>
                Power: {station['max_power']} kW<br>
                Price: ${station['price_per_kwh']}/kWh
                """
                
                folium.Marker([station['latitude'], station['longitude']],
                             popup=folium.Popup(popup_html, max_width=300),
                             icon=folium.Icon(color=color, icon='bolt', prefix='fa')).add_to(m)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html', mode='w') as f:
                m.save(f.name)
                webbrowser.open(f'file://{f.name}')
                self.status_bar.config(text="🗺️ Map opened in browser")
            
        except Exception as e:
            messagebox.showerror("Map Error", f"Failed to create map: {str(e)}")
    
    def open_provider_registration(self):
        ProviderRegistrationWindow(self.root, self)

class ProviderRegistrationWindow:
    def __init__(self, parent, main_app):
        self.main_app = main_app
        self.window = tk.Toplevel(parent)
        self.window.title("Register as EV Charging Provider")
        self.window.geometry("600x700")
        self.window.configure(bg='#1e1e1e')
        self.window.transient(parent)
        self.window.grab_set()
        
        self.create_registration_form()
    
    def create_registration_form(self):
        # Title
        title = tk.Label(self.window, text="👤 Register as EV Charging Provider", 
                        font=('Segoe UI', 18, 'bold'), fg='#00ff88', bg='#1e1e1e')
        title.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self.window, bg='#2d2d2d')
        form_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Basic Info
        self.create_form_section(form_frame, "Basic Information", [
            ("Station Name:", "name", "My Home Charging Station"),
            ("Address:", "address", "Enter your address"),
            ("Contact Info:", "contact_info", "Phone: +91 98765 43210"),
            ("Email:", "email", "provider@example.com")
        ])
        
        # Location
        self.create_form_section(form_frame, "Location", [
            ("Latitude:", "latitude", "9.9312"),
            ("Longitude:", "longitude", "76.2673")
        ])
        
        # Charging Specs
        self.create_form_section(form_frame, "Charging Specifications", [
            ("Total Slots:", "total_slots", "1"),
            ("Available Slots:", "available_slots", "1"),
            ("Max Power (kW):", "max_power", "22"),
            ("Power Types:", "power_types", "Type 2")
        ])
        
        # Pricing
        self.create_form_section(form_frame, "Pricing & Time", [
            ("Price per kWh ($):", "price_per_kwh", "0.15"),
            ("Pricing Model:", "pricing_model", "per_kwh"),
            ("Time Limits:", "time_limits", "2_hours"),
            ("Operating Hours:", "operating_hours", "6PM-10PM")
        ])
        
        # Buttons
        button_frame = tk.Frame(self.window, bg='#1e1e1e')
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="✅ Register Station", font=('Segoe UI', 12, 'bold'),
                 fg='#000000', bg='#00ff88', command=self.register_provider).pack(side='left', padx=10)
        
        tk.Button(button_frame, text="❌ Cancel", font=('Segoe UI', 12, 'bold'),
                 fg='#ffffff', bg='#ff4444', command=self.window.destroy).pack(side='left', padx=10)
    
    def create_form_section(self, parent, title, fields):
        section_frame = tk.LabelFrame(parent, text=title, font=('Segoe UI', 12, 'bold'),
                                   fg='#ffffff', bg='#2d2d2d', borderwidth=1, relief='solid')
        section_frame.pack(fill='x', padx=10, pady=10)
        
        self.entries = {}
        
        for label_text, key, default in fields:
            field_frame = tk.Frame(section_frame, bg='#2d2d2d')
            field_frame.pack(fill='x', padx=10, pady=5)
            
            tk.Label(field_frame, text=label_text, font=('Segoe UI', 10),
                    fg='#b0b0b0', bg='#2d2d2d', width=15, anchor='w').pack(side='left')
            
            entry = tk.Entry(field_frame, font=('Segoe UI', 10), bg='#404040', fg='#ffffff')
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
            entry.insert(0, default)
            
            self.entries[key] = entry
    
    def register_provider(self):
        try:
            provider_data = {
                "id": 1000 + len(self.main_app.registered_providers),
                "name": self.entries["name"].get(),
                "address": self.entries["address"].get(),
                "contact_info": self.entries["contact_info"].get(),
                "email": self.entries["email"].get(),
                "latitude": float(self.entries["latitude"].get()),
                "longitude": float(self.entries["longitude"].get()),
                "total_slots": int(self.entries["total_slots"].get()),
                "available_slots": int(self.entries["available_slots"].get()),
                "max_power": int(self.entries["max_power"].get()),
                "power_types": [self.entries["power_types"].get()],
                "price_per_kwh": float(self.entries["price_per_kwh"].get()),
                "pricing_model": self.entries["pricing_model"].get(),
                "time_limits": self.entries["time_limits"].get(),
                "operating_hours": self.entries["operating_hours"].get(),
                "status": "available",
                "registered_date": datetime.now().isoformat()
            }
            
            self.main_app.registered_providers.append(provider_data)
            self.main_app.save_providers()
            self.main_app.load_all_stations()
            
            messagebox.showinfo("Success", "Your charging station has been registered successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Registration Error", f"Failed to register: {str(e)}")

def main():
    root = tk.Tk()
    app = EVChargingWithProviders(root)
    root.mainloop()

if __name__ == "__main__":
    main()
