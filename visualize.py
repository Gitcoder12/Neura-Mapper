import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from neuro_router import NeuroMapper

def plot_3d_path(mapper, path, start, end):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Separate zones by color
    safe_zones, warning_zones, critical_zones = [], [], []
    for coord, zone in mapper.zones.items():
        if zone == 0: safe_zones.append(coord)
        elif zone == 1: warning_zones.append(coord)
        elif zone == 2: critical_zones.append(coord)

    # Plot Zones
    if safe_zones:
        sx, sy, sz = zip(*safe_zones)
        ax.scatter(sx, sy, sz, c='green', alpha=0.1, label='Safe Zone')
    if warning_zones:
        wx, wy, wz = zip(*warning_zones)
        ax.scatter(wx, wy, wz, c='yellow', marker='^', s=80, alpha=0.6, label='Warning Zone (High Risk)')
    if critical_zones:
        cx, cy, cz = zip(*critical_zones)
        ax.scatter(cx, cy, cz, c='red', marker='s', s=100, alpha=0.8, label='Critical (No-Go)')

    # Plot Start and End
    ax.scatter(*start, c='blue', marker='o', s=150, label='Start (Entry)')
    ax.scatter(*end, c='purple', marker='*', s=250, label='End (Target)')

    # Plot Path
    if path:
        px, py, pz = zip(*path)
        ax.plot(px, py, pz, c='black', linewidth=3, label='Optimized Path')

    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')
    ax.set_zlabel('Z Axis')
    ax.set_title('Neura-Mapper: Area Classifier & 3D Routing')
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    mapper = NeuroMapper(grid_size=(10, 10, 10))
    
    # Simulate Medical Data (Area Classification)
    # Create a critical red zone (e.g., a tumor/artery)
    for x in range(4, 7):
        for y in range(4, 7):
            for z in range(4, 7):
                mapper.classify_region((x, y, z), 2)
                
    # Create a warning yellow zone (e.g., sensitive nerves) around the critical zone
    for x in range(3, 8):
        for y in range(3, 8):
            mapper.classify_region((x, y, 3), 1) # Nerve layer below

    start = (0, 0, 0)
    end = (9, 9, 9)
    path = mapper.find_safest_path(start, end)
    
    print(f"Path Length: {len(path) if path else 0} steps")
    print(f"Path navigated around critical zones and minimized time in warning zones.")
    plot_3d_path(mapper, path, start, end)
