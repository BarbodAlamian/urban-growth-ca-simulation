# Urban Growth Cellular Automata Simulation

## Computational Intelligence - Assignment 1
**Student:** Barbad Alamian  
**University:** K. N. Toosi University of Technology  
**Course:** Computational Intelligence  
**TA:** Yasin Mohammadi

## 📋 Project Description
Simulation of urban growth using Cellular Automata with real-world GIS constraints:
- Digital Elevation Model (DEM) limitations
- Distance to road networks influence  
- Circular neighborhood interactions
- Urban cell persistence

## 🗺️ Input Data
1. **Digital Elevation Model (DEM)** - Elevation constraints
2. **Road Distance Raster** - Proximity to transportation networks
3. **Initial Urban Seed** - Starting urban configuration

## ⚙️ Simulation Parameters
- Neighborhood radius: 5 cells (~140 meters)
- Minimum urban neighbors: 8 cells
- Maximum elevation: 700 meters
- Maximum road distance: 1000 meters
- Simulation steps: 20 iterations

## 📊 Output Files
1. `01_initial_state.png` - Initial conditions visualization
2. `02_final_results.png` - Final state and growth analysis
3. `03_urban_growth.gif` - Animation of urban growth over time
4. `simulation_data.npz` - Numerical simulation data

## 📈 Results Summary
- Initial urban cells: [مقدار]
- Final urban cells: [مقدار]
- Total growth: [مقدار] cells
- Growth percentage: [درصد]%

## 🚀 How to Run
```bash
# Install required packages
pip install numpy matplotlib scipy pillow

# Run simulation (if Python code included)
python urban_growth_ca.py