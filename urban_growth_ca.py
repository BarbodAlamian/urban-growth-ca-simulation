"""
Urban Growth CA with Real GIS Data
Fixed orientation and output directory issues
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# ============================================
# CONFIGURATION
# ============================================

# Paths to your .npy files
DATA_DIR = r"F:\BA.BA\Master\مسگری - هوش محاسباتی\Ta\npy_data"
DEM_FILE = os.path.join(DATA_DIR, "dem.npy")
ROAD_FILE = os.path.join(DATA_DIR, "road.npy")
URBAN_FILE = os.path.join(DATA_DIR, "urban.npy")

# Output directory - CORRECT PATH
OUTPUT_DIR = r"F:\BA.BA\Master\مسگری - هوش محاسباتی\Ta\ca_results2"

# ============================================
# DATA LOADING WITH ORIENTATION FIX
# ============================================

def load_data() -> tuple:
    """
    Load data and fix orientation if needed.
    """
    print("Loading data from .npy files...")
    
    dem = np.load(DEM_FILE)
    road_dist = np.load(ROAD_FILE)
    urban_init = np.load(URBAN_FILE)
    
    # Convert urban to binary (0 or 1)
    urban_init = (urban_init > 0).astype(int)
    
    # FIX ORIENTATION: Flip vertically if needed
    # ArcGIS stores data with origin at top-left, matplotlib expects bottom-left
    dem = np.flipud(dem)  # Flip vertically
    road_dist = np.flipud(road_dist)  # Flip vertically
    urban_init = np.flipud(urban_init)  # Flip vertically
    
    print(f"DEM shape: {dem.shape}, Elevation: {dem.min():.0f} to {dem.max():.0f} m")
    print(f"Road distance shape: {road_dist.shape}")
    print(f"Initial urban cells: {np.sum(urban_init == 1)}")
    
    return dem, road_dist, urban_init

# ============================================
# CA FUNCTIONS
# ============================================

def count_urban_neighbours(urban: np.ndarray) -> np.ndarray:
    """
    Count urban neighbours with zero padding.
    """
    from scipy.ndimage import convolve
    
    kernel = np.ones((3, 3))
    kernel[1, 1] = 0
    
    neighbours = convolve(urban.astype(float), kernel, 
                         mode='constant', cval=0.0)
    
    return neighbours.astype(int)

def step_city_growth(urban: np.ndarray, dem: np.ndarray, 
                    road_dist: np.ndarray, study_mask: np.ndarray) -> np.ndarray:
    """
    One CA step with constraints.
    """
    neighbours = count_urban_neighbours(urban)
    
    # Growth rules
    cond_high = (neighbours >= 8) & (dem < 700) & (road_dist < 1000)
    cond_medium = (neighbours >= 3) & (neighbours <= 7) & (dem < 500) & (road_dist < 1500)
    
    can_become_urban = (urban == 0) & study_mask
    new_urban_cells = can_become_urban & (cond_high | cond_medium)
    
    next_urban = urban.copy()
    next_urban[new_urban_cells] = 1
    next_urban[~study_mask] = 0
    
    return next_urban

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def show_initial_state(dem: np.ndarray, urban: np.ndarray, 
                      road_dist: np.ndarray, output_dir: str):
    """
    Show initial state.
    """
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    
    # DEM - NO origin='lower' for flipped data
    im_dem = axes[0].imshow(dem, cmap='terrain')
    axes[0].set_title("Digital Elevation Model")
    axes[0].set_xticks([])
    axes[0].set_yticks([])
    plt.colorbar(im_dem, ax=axes[0], fraction=0.046, pad=0.04, label="m")
    
    # Road distance
    im_road = axes[1].imshow(road_dist, cmap='viridis')
    axes[1].set_title("Distance to Roads")
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    plt.colorbar(im_road, ax=axes[1], fraction=0.046, pad=0.04, label="m")
    
    # Initial urban
    im_urban = axes[2].imshow(urban, cmap='gray_r', vmin=0, vmax=1)
    axes[2].set_title(f"Initial Urban Pattern\n({np.sum(urban==1)} cells)")
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    
    fig.tight_layout()
    
    # SAVE TO CORRECT DIRECTORY
    output_path = os.path.join(OUTPUT_DIR, "01_initial_state.png")
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Saved: {output_path}")
    plt.show()
    plt.close()

def run_simulation(dem: np.ndarray, road_dist: np.ndarray, 
                  initial_urban: np.ndarray, n_steps: int = 20):
    """
    Run simulation with live display.
    """
    # Create study area mask
    study_mask = ~np.isnan(dem)
    
    # Initialize
    urban = initial_urban.copy()
    urban_history = [urban.copy()]
    urban_counts = [np.sum(urban == 1)]
    
    # Setup figure for live display
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    
    # DEM display
    dem_display = dem.copy()
    dem_display[np.isnan(dem)] = np.nanmin(dem[~np.isnan(dem)])
    
    im1 = ax1.imshow(dem_display, cmap='terrain', alpha=0.7)
    urban_overlay = ax1.imshow(np.ma.masked_where(urban == 0, urban), 
                              cmap='Reds', alpha=0.7, vmin=0, vmax=1)
    ax1.set_title("Urban Growth on DEM")
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Growth progress
    ax2.set_xlim(0, n_steps)
    ax2.set_ylim(0, np.sum(study_mask) * 0.5)
    ax2.set_xlabel("Time Step")
    ax2.set_ylabel("Urban Cells")
    ax2.set_title("Growth Progress")
    ax2.grid(True, alpha=0.3)
    
    line, = ax2.plot([0], [urban_counts[0]], 'b-', linewidth=2)
    point = ax2.scatter([0], [urban_counts[0]], color='red', s=50)
    
    plt.tight_layout()
    plt.ion()
    plt.show()
    
    print(f"\nStarting simulation for {n_steps} steps...")
    
    # Run simulation
    for step in range(n_steps):
        urban = step_city_growth(urban, dem, road_dist, study_mask)
        urban_history.append(urban.copy())
        
        current_count = np.sum(urban == 1)
        urban_counts.append(current_count)
        
        # Update display
        urban_overlay.set_data(np.ma.masked_where(urban == 0, urban))
        ax1.set_title(f"Step {step + 1}/{n_steps}")
        
        line.set_data(range(step + 2), urban_counts)
        point.set_offsets([[step + 1, current_count]])
        
        fig.canvas.draw()
        fig.canvas.flush_events()
        
        print(f"Step {step + 1}: {current_count} urban cells "
              f"(+{current_count - urban_counts[step]})")
    
    plt.ioff()
    plt.close()
    
    return dem_display, urban_history, urban_counts, study_mask

def save_final_results(dem_display: np.ndarray, urban_history: list,
                      urban_counts: list, initial_urban: np.ndarray,
                      n_steps: int):
    """
    Save final results to output directory.
    """
    urban_final = urban_history[-1]
    
    # Create final comparison figure
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    
    # Final urban on DEM
    ax1.imshow(dem_display, cmap='terrain', alpha=0.7)
    ax1.imshow(np.ma.masked_where(urban_final == 0, urban_final), 
              cmap='Reds', alpha=0.7, vmin=0, vmax=1)
    ax1.set_title(f"Final State (Step {n_steps})")
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Growth areas only
    growth = urban_final - initial_urban
    growth[growth < 0] = 0
    im_growth = ax2.imshow(growth, cmap='YlOrRd', vmin=0, vmax=1)
    ax2.set_title(f"New Growth Areas\n{np.sum(growth == 1)} cells")
    ax2.set_xticks([])
    ax2.set_yticks([])
    
    # Growth curve
    ax3.plot(urban_counts, 'b-', linewidth=2)
    ax3.set_xlabel("Time Step")
    ax3.set_ylabel("Urban Cells")
    ax3.set_title("Growth Over Time")
    ax3.grid(True, alpha=0.3)
    
    plt.tight_layout()
    final_path = os.path.join(OUTPUT_DIR, "02_final_results.png")
    plt.savefig(final_path, dpi=150, bbox_inches='tight')
    plt.show()
    plt.close()
    print(f"✓ Saved: {final_path}")

def create_gif_animation(dem_display: np.ndarray, 
                        urban_history: list, 
                        n_steps: int):
    """
    Create GIF animation.
    """
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks([])
    ax.set_yticks([])
    
    ax.imshow(dem_display, cmap='terrain', alpha=0.7)
    
    urban_img = ax.imshow(np.ma.masked_where(urban_history[0] == 0, urban_history[0]), 
                         cmap='Reds', alpha=0.7, vmin=0, vmax=1)
    title = ax.set_title(f"Urban Growth - Step 0/{n_steps}")
    
    def update(frame: int):
        urban_img.set_data(np.ma.masked_where(urban_history[frame] == 0, 
                                            urban_history[frame]))
        title.set_text(f"Urban Growth - Step {frame}/{n_steps}")
        return [urban_img, title]
    
    anim = FuncAnimation(
        fig,
        update,
        frames=len(urban_history),
        interval=300,
        blit=True
    )
    
    gif_path = os.path.join(OUTPUT_DIR, "03_urban_growth.gif")
    anim.save(gif_path, writer='pillow', fps=5)
    print(f"✓ Saved: {gif_path}")
    
    plt.close()

# ============================================
# MAIN EXECUTION
# ============================================

def main():
    """
    Main function.
    """
    print("=" * 60)
    print("URBAN GROWTH CA SIMULATION")
    print("Fixed Orientation and Output")
    print("=" * 60)
    
    # 1. Create output directory if it doesn't exist
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")
    else:
        print(f"Using existing directory: {OUTPUT_DIR}")
    
    # 2. Load data with orientation fix
    try:
        dem, road_dist, initial_urban = load_data()
    except Exception as e:
        print(f"Error loading data: {e}")
        return
    
    # 3. Show initial state
    print("\n" + "-" * 60)
    print("SHOWING INITIAL STATE")
    print("-" * 60)
    show_initial_state(dem, initial_urban, road_dist, OUTPUT_DIR)
    
    # 4. Run simulation
    print("\n" + "-" * 60)
    print("RUNNING SIMULATION")
    print("-" * 60)
    n_steps = 20
    dem_display, urban_history, urban_counts, study_mask = run_simulation(
        dem, road_dist, initial_urban, n_steps
    )
    
    # 5. Save results
    print("\n" + "-" * 60)
    print("SAVING RESULTS")
    print("-" * 60)
    save_final_results(dem_display, urban_history, urban_counts, initial_urban, n_steps)
    create_gif_animation(dem_display, urban_history, n_steps)
    
    # 6. Save numerical data
    np.savez_compressed(
        os.path.join(OUTPUT_DIR, "simulation_data.npz"),
        dem=dem,
        road_dist=road_dist,
        initial_urban=initial_urban,
        final_urban=urban_history[-1],
        urban_history=urban_history,
        urban_counts=urban_counts,
        study_mask=study_mask
    )
    print(f"✓ Saved: {os.path.join(OUTPUT_DIR, 'simulation_data.npz')}")
    
    # 7. Summary
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
    print(f"Initial urban cells: {urban_counts[0]}")
    print(f"Final urban cells:   {urban_counts[-1]}")
    print(f"Total growth:        {urban_counts[-1] - urban_counts[0]}")
    
    print(f"\n📁 All results saved to: {OUTPUT_DIR}")
    print("  01_initial_state.png  - Initial conditions")
    print("  02_final_results.png  - Final state and growth analysis")
    print("  03_urban_growth.gif   - Growth animation")
    print("  simulation_data.npz   - Numerical data")
    
    # 8. Verify files were saved
    print("\nVerifying saved files:")
    for filename in ["01_initial_state.png", "02_final_results.png", 
                    "03_urban_growth.gif", "simulation_data.npz"]:
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath) / 1024  # KB
            print(f"  ✓ {filename} ({size:.1f} KB)")
        else:
            print(f"  ✗ {filename} (NOT SAVED!)")

# ============================================
# RUN
# ============================================

if __name__ == "__main__":
    # Install required packages
    try:
        from scipy.ndimage import convolve
    except ImportError:
        print("Installing scipy...")
        import subprocess
        subprocess.check_call(["pip", "install", "scipy", "pillow"])
        from scipy.ndimage import convolve
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()