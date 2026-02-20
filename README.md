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
