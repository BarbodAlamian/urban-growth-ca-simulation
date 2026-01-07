# Urban Growth Cellular Automata Simulation

## Computational Intelligence - Assignment 1
**Student:** Barbad Alamian  
**University:** K. N. Toosi University of Technology  
**Course:** Computational Intelligence  
**TA:** Yasin Mohammadi

## 📋 Project Description
Simulation of urban growth in Babol region using Cellular Automata with real GIS data:
- Digital Elevation Model (DEM) constraints
- Distance to road networks influence
- Circular neighborhood interactions
- Urban cell persistence

## 🗺️ Study Area & Data
- **Location:** Babol, Mazandaran Province, Iran
- **DEM Source:** USGS SRTM 1 arc-second (~30m resolution)
- **Road Data:** OpenStreetMap (filtered main roads)
- **Urban Seed:** Residential areas from landuse data
- **Study Area:** 554×709 cells (≈15.5×19.8 km)

## ⚙️ CA Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| Neighborhood radius | 5 cells (~140m) | Circular neighborhood |
| Minimum urban neighbors | 8 cells | Growth threshold |
| Maximum elevation | 700 m | Height constraint |
| Maximum road distance | 1000 m | Proximity to roads |
| Simulation steps | 20 iterations | Time steps |
| Cell size | 27.89 m | Spatial resolution |

## 📈 Results Summary
- **Initial urban cells:** 46,423
- **Final urban cells:** 78,439
- **Total growth:** 32,016 cells
- **Growth percentage:** 69.0%
- **Average growth/step:** 1,601 cells
- **Urban coverage increase:** 15.4% to 26.1%

## 📊 Output Files
1. `01_initial_state.png` - Initial DEM with urban seed
2. `02_final_results.png` - Final urban pattern and analysis
3. `03_urban_growth.gif` - Animation of urban expansion
4. `simulation_data.npz` - Numerical simulation data
5. `urban_growth_ca.py` - Python simulation code

## 🔍 Key Findings & Analysis
### 1. **Road Influence**
- Strong growth concentration along main roads
- 85% of new urban cells within 500m of roads
- Road proximity was the dominant growth factor

### 2. **Elevation Constraints**
- Limited development above 700m elevation
- Growth primarily in low-lying areas (<500m)
- DEM effectively constrained unrealistic mountain development

### 3. **Spatial Patterns**
- Radial expansion from initial urban cores
- Circular neighborhood created realistic clustering
- Edge effects minimal due to study area mask

### 4. **Model Performance**
- Realistic urban growth patterns
- Computationally efficient (20 steps in <2 minutes)
- Scalable to larger regions

## 🚀 How to Reproduce
```bash
# 1. Install dependencies
pip install numpy matplotlib scipy pillow rasterio

# 2. Clone repository
git clone https://github.com/BarbodAlamian/urban-growth-ca-simulation.git

# 3. Run simulation
cd urban-growth-ca-simulation
python urban_growth_ca.py
```

## 📁 Repository Structure
```
urban-growth-ca-simulation/
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── 01_initial_state.png     # Initial conditions
├── 02_final_results.png     # Final results & analysis
├── 03_urban_growth.gif      # Growth animation
├── simulation_data.npz      # Numerical data
└── urban_growth_ca.py       # Python simulation code
```

## 🏗️ Model Limitations & Future Work
- **Limitations:**
  - Simplified growth rules (4 constraints only)
  - Static road network (no new roads)
  - No socio-economic factors considered
  
- **Improvements:**
  - Incorporate population density
  - Add land value/pricing
  - Include zoning regulations
  - Dynamic road network growth

## 📚 References
1. TA Course Materials - Session 2-3: Cellular Automata
2. USGS EarthExplorer - SRTM Data
3. OpenStreetMap - Road Network Data

## 📄 License
Educational use - K. N. Toosi University of Technology
