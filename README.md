# ⚡ EV Charging Station Finder - Kerala

A modern desktop application for finding and registering EV charging stations in Kerala, India with provider registration features.

## 🌟 Features

- **🔍 Station Search**: Find nearby EV charging stations
- **📍 Live Location**: Auto-detect user location (Kochi default)
- **👤 Provider Registration**: Register your own charging station
- **🗺️ Interactive Maps**: Visualize stations on map
- **💰 Custom Pricing**: Set your own charging rates
- **⏰ Time Management**: Control charging time limits
- **🎨 Modern UI**: Dark theme with intuitive interface
- **📊 Real-time Availability**: Check station status

## 🚀 Quick Start
Perfect! You have a **Python-based EV Charging Station Finder desktop app** with Tkinter GUI and optional Folium maps. I’ll give a **step-by-step guide** on how anyone can download and run it on **any computer** (Windows, macOS, Linux). I’ll also explain optional features like maps and real API integration.

---

# **How to Run “EV Charging Station Finder – Kerala” on Another Computer**

## **Step 1: Install Python**

1. Check if Python is installed:

```bash
python --version
```

or

```bash
python3 --version
```

2. If not installed:

   * Go to [python.org/downloads](https://www.python.org/downloads/)
   * Download Python 3.7 or higher
   * Make sure to **check “Add Python to PATH”** during installation

> Tkinter comes pre-installed with Python, so you don’t need a separate install for GUI.

---

## **Step 2: Download the Project from GitHub**

**Option 1 – Using Git:**

```bash
git clone https://github.com/yourusername/ev-charging-kerala.git
cd ev-charging-kerala
```

**Option 2 – Without Git:**

1. Go to the GitHub repository URL.
2. Click **Code → Download ZIP**.
3. Extract the ZIP file to a folder on your computer.

---

## **Step 3: Install Required Dependencies**

Open a terminal or command prompt **inside the project folder**. Run:

```bash
pip install -r requirements.txt
```

**Dependencies include:**

* `tkinter` → GUI (comes with Python)
* `requests` → for API calls
* `folium` → for interactive maps (optional)
* `geopy` → for distance calculations (optional)

> ⚡ Tip: If you want to use virtual environments (recommended), run:

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

This keeps dependencies isolated.

---

## **Step 4: Run the Application**

There are **two main scripts** in the project:

1. **For general EV Charging Finder:**

```bash
python ev_charging_finder.py
```

2. **For Provider Registration & Full Features:**

```bash
python ev_charging_with_providers.py
```

* The app will **auto-detect your location** (default Kochi, Kerala).
* A **Tkinter window** will open with search, filters, and provider registration options.

---

## **Step 5: Using the App**

### **For EV Owners:**

1. Launch app – auto-locates to Kochi.
2. Enter search radius (1–50 km).
3. View nearby charging stations with:

   * Price per kWh
   * Available slots
   * Power types (Type 2, CCS, CHAdeMO)
4. Click stations to get directions or info.

### **For Charging Station Providers:**

1. Click **➕ REGISTER AS PROVIDER**.
2. Fill station details, pricing, time limits, and contact.
3. Submit – the station appears in searches immediately.
4. Update pricing/availability anytime.

---

## **Step 6: Optional – Map Visualization**

If you want to **view stations on an interactive map**:

1. Ensure `folium` is installed:

```bash
pip install folium
```

2. Run the script or call the method to generate HTML map:

```python
create_map(stations, user_lat, user_lon)
```

3. This will create `charging_stations_map.html`. Open it in any browser to see an interactive map.

* Green markers → Available stations
* Red markers → Full/Unavailable
* Purple markers → Registered provider stations

---

## **Step 7: Optional – Real-time API Integration**

If you want **real data from OpenChargeMap, PlugShare, etc.:**

1. Get an API key from the service.
2. Replace the `_generate_mock_data()` function with a real API call:

```python
import requests

def get_real_stations(self, lat, lon, radius):
    url = "https://api.openchargemap.io/v3/poi"
    params = {
        "latitude": lat,
        "longitude": lon,
        "distance": radius,
        "distanceunit": "KM",
        "key": self.api_key
    }
    response = requests.get(url, params=params)
    return response.json()
```

3. Update your app to use `get_real_stations()` instead of mock data.

---

## **Step 8: Keep Project Updated**

If you cloned via Git, you can fetch updates anytime:

```bash
git pull origin main
```

---

## **Step 9: Notes on Cross-Platform Compatibility**

* **Windows:** Double-check Python is added to PATH. Use `venv\Scripts\activate`.
* **macOS/Linux:** May need `python3` instead of `python`. Use `source venv/bin/activate`.
* **Tkinter GUI:** Works on all platforms.
* **Folium maps:** Open in any browser, platform-independent.

---


### Prerequisites
- Python 3.7 or higher
- Windows, macOS, or Linux

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ev-charging-kerala.git
   cd ev-charging-kerala
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python ev_charging_with_providers.py
   ```

## 📋 Requirements

```txt
tkinter
requests
folium
```

## 🎮 How to Use

### For EV Owners:
1. **Launch app** - Auto-detects your location (Kochi, Kerala)
2. **Search stations** - Find nearby charging points within 25km
3. **View details** - Check pricing, availability, power types
4. **Get directions** - Navigate to stations

### For Charging Station Providers:
1. **Click "➕ REGISTER AS PROVIDER"** - Orange button in top header
2. **Fill details** - Station info, pricing, time limits, contact
3. **Submit** - Your station appears in searches immediately
4. **Manage** - Update availability and pricing anytime

## 🌍 Coverage

Currently supports **Kerala, India** with stations in:
- **Kochi** (MG Road, Ernakulam)
- **Lulu Mall** (Edappally)
- **Cochin International Airport** (Nedumbassery)
- **Kalady Town** (Near Sree Sankara Temple)
- **And growing...** (Add your station!)

## 💡 Features Details

### 🔍 Search & Filters
- **Radius search** (1-50 km slider)
- **Access type** (Public, Private, Registered Providers)
- **Power type** (Type 2, CCS, CHAdeMO)
- **Real-time availability** checking
- **Distance-based sorting**

### 👤 Provider Features
- **Custom pricing models** (per kWh, per hour)
- **Time limit controls** (1 hour, 2 hours, etc.)
- **Operating hours** management
- **Contact information** display
- **Persistent storage** (JSON database)
- **Instant activation** after registration

### �️ Map Integration
- **Interactive Folium maps**
- **Color-coded stations** (Public=Green, Private=Orange, Provider=Purple)
- **Distance calculations** using Haversine formula
- **Browser-based viewing**

## �️ Technical Stack

- **Frontend**: Tkinter (Python GUI)
- **Maps**: Folium with OpenStreetMap
- **Location**: IP-based geolocation (ipinfo.io, ipapi.co)
- **Data**: JSON storage for providers
- **Distance**: Haversine formula
- **Threading**: Non-blocking operations

## 📱 Future Roadmap

- [ ] **Mobile app** (React Native)
- [ ] **Payment integration** (Razorpay, PayTM)
- [ ] **Booking system** (Reserve slots)
- [ ] **Rating system** (User reviews)
- [ ] **More cities** (Bangalore, Chennai, Mumbai)
- [ ] **Real-time data** (API integration)
- [ ] **AI recommendations** (Smart suggestions)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

- **Developer**: Your Name
- **Email**: your.email@example.com
- **GitHub**: https://github.com/yourusername

## 🎯 Quick Demo

1. **Run the app**: `python ev_charging_with_providers.py`
2. **Auto-locates** to Kochi, Kerala
3. **Shows 4 stations** automatically
4. **Register as provider** using top header button
5. **Search and filter** with left panel controls

---

⚡ **Powering Kerala's EV Revolution!** 🚗⚡
- 💰 Compare pricing information
- 📊 Real-time slot availability
- 🗺️ Mock data for demonstration (can be extended with real APIs)

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python ev_charging_finder.py
```

### Example Usage

```
🔋 EV Charging Station Finder
========================================

📍 Enter your location (press Enter for default NYC coordinates):
Latitude (default: 40.7128): 40.7580
Longitude (default: -74.0060): -73.9855

Search radius in km (default: 10): 5
Minimum available slots required (default: 1): 1

🔍 Searching for charging stations within 5.0 km...

🔋 Found 2 available charging stations:
============================================================

📍 Station 1: Tesla Supercharger - Downtown
   📍 Address: 123 Main St, City Center
   📏 Distance: 0.89 km
   🔌 Available Slots: 3/8
   ⚡ Power Types: Type 2, CCS, CHAdeMO
   💪 Max Power: 250 kW
   💰 Price: $0.28/kWh
   🟢 Status: OPEN
----------------------------------------

📍 Station 2: ChargePoint Station - Mall
   📍 Address: 456 Shopping Ave, West District
   📏 Distance: 1.23 km
   🔌 Available Slots: 2/4
   ⚡ Power Types: Type 2, CCS
   💪 Max Power: 150 kW
   💰 Price: $0.32/kWh
   🟢 Status: OPEN
----------------------------------------
```

## Code Structure

- `ev_charging_finder.py` - Main application with EVChargingFinder class
- `requirements.txt` - Python dependencies
- `README.md` - Documentation

## Key Methods

### EVChargingFinder Class

- `find_nearby_stations()` - Find stations within radius
- `calculate_distance()` - Calculate distance between coordinates
- `filter_by_power_type()` - Filter by connector type
- `filter_by_max_power()` - Filter by power requirements
- `display_stations()` - Format and display results

## Extending the Application

### Adding Real API Integration

To integrate with real charging station APIs (like OpenChargeMap, PlugShare, etc.):

1. Get an API key from the service
2. Replace the mock data in `_generate_mock_data()` with API calls
3. Update the `__init__` method to use the API key

Example:
```python
def get_real_stations(self, lat, lon, radius):
    url = f"https://api.openchargemap.io/v3/poi"
    params = {
        "latitude": lat,
        "longitude": lon,
        "distance": radius,
        "distanceunit": "KM",
        "key": self.api_key
    }
    response = requests.get(url, params=params)
    return response.json()
```

### Adding Map Visualization

Install additional dependencies:
```bash
pip install folium
```

Add a method to generate maps:
```python
def create_map(self, stations, user_lat, user_lon):
    import folium
    
    # Create map centered on user location
    m = folium.Map(location=[user_lat, user_lon], zoom_start=13)
    
    # Add user marker
    folium.Marker([user_lat, user_lon], 
                  popup="Your Location", 
                  icon=folium.Icon(color='blue')).add_to(m)
    
    # Add station markers
    for station in stations:
        color = 'green' if station['available_slots'] > 0 else 'red'
        folium.Marker([station['latitude'], station['longitude']], 
                      popup=station['name'],
                      icon=folium.Icon(color=color)).add_to(m)
    
    m.save('charging_stations_map.html')
```

## Dependencies

- `requests` - HTTP requests for API integration
- `geopy` - Advanced geocoding and distance calculations (optional)
- `folium` - Interactive maps (optional)

## License

This project is open source and available under the MIT License.
