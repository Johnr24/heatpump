# Heat Pump Map Project

This project visualizes heat pump locations and their coefficients of performance (COP) on a map. It fetches data from heatpumpmointor.org and displays it using the folium library.


## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd heatpump-map-project
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the data fetching script to get heat pump data:
   ```
   python src/heatpumpmap.py
   ```

2. Plot the heat pump locations on a map:
   ```
   python src/plot_map.py
   ```

## Dependencies

- requests
- folium (or any other mapping library used)

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.