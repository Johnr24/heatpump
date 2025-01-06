# Heat Pump Map Project

This project visualizes heat pump locations and their coefficients of performance (COP) on a map. It fetches data from a heat pump monitoring service and displays it using a mapping library.

## Project Structure

```
heatpump-map-project
├── src
│   ├── heatpumpmap.py       # Fetches and processes heat pump data
│   ├── plot_map.py          # Plots heat pump locations on a map
│   └── utils
│       └── __init__.py      # Contains utility functions for data processing
├── requirements.txt          # Lists project dependencies
└── README.md                 # Project documentation
```

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