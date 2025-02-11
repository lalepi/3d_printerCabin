# 3D Printer Cabin

This project is designed to monitor and control the environment inside a 3D printer (Prusa MK3S) cabin using Arduino and Raspberry Pi. The system measures temperature and humidity at different points inside the cabin and displays the data on an LCD screen. It also communicates with a Python script running on a Raspberry Pi to fetch external temperature data and send it to the Arduino.

## Project Structure

### Files and Directories

- **3d_printerCabin/docker-compose.yml**: Docker Compose configuration file to set up the services.
- **3d_printerCabin/Dockerfile**: Dockerfile to build the Python environment.
- **3d_printerCabin/measurements/arduinoSide/arduinoSide.ino**: Arduino sketch for measuring temperature and humidity.
- **3d_printerCabin/measurements/readMeasurements.py**: Python script to read measurements from the Arduino and fetch external temperature data.
- **3d_printerCabin/measurements/requirements.txt**: Python dependencies for the project.
- **.env**: Environment variables file (not included in version control).
- **devicenames.txt**: Device names file (not included in version control).
- **test.ipynb**: Jupyter notebook for testing purposes.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Arduino IDE
- Python 3.x

### Installation

Raspberry side

1. **Clone the repository:**

   ```sh
   git clone https://github.com/lalepi/3d_printerCabin.git
   cd 3d_printerCabin
   ```

2. **Build and run the Docker containers:**

   ```sh
   docker-compose up --build
   ```

3. **Set up environment variables:**

   - Create a [.env] file in the root directory with the following content:

   ```env
   APIkey=your_openweathermap_api_key
   city=your_city_name
   ```

4. **Install Python dependencies:**

   ```sh
   pip install -r 3d_printerCabin/measurements/requirements.txt
   ```

Arduino side:

1. **Upload the Arduino sketch:**

   - Open [arduinoSide.ino] in the Arduino IDE.
   - Select the correct board and port.
   - Upload the sketch to the Arduino.

## Usage

- The Arduino will measure temperature and humidity and display the data on the LCD screen.
- The Python script will fetch external temperature data from OpenWeatherMap and send it to the Arduino.
- The data will be displayed on the LCD screen in different modes, which can be toggled using a button.

### Running the Python Script

```sh
python 3d_printerCabin/measurements/readMeasurements.py
```
