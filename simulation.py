import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation as funi
from matplotlib.ticker import MultipleLocator as loc
from matplotlib.path import Path
import numpy as np


def make_plane_marker():
   
    verts_vertical = [
        ( 0.0,   0.8),   # nose tip
        ( 0.08,  0.3),   # right body upper
        ( 0.6,   0.0),   # right wing tip
        ( 0.12, -0.15),  # right wing root
        ( 0.12, -0.45),  # right tail upper
        ( 0.35, -0.6),   # right tail tip
        ( 0.08, -0.65),  # right tail base
        ( 0.0,  -0.5),   # tail center
        (-0.08, -0.65),  # left tail base
        (-0.35, -0.6),   # left tail tip
        (-0.12, -0.45),  # left tail upper
        (-0.12, -0.15),  # left wing root
        (-0.6,   0.0),   # left wing tip
        (-0.08,  0.3),   # left body upper
        ( 0.0,   0.8),   # close back to nose
    ]
    # Rotate 90 degrees clockwise: (x, y) -> (y, -x)
    verts = [(y, -x) for x, y in verts_vertical]
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes)


PLANE_MARKER = make_plane_marker()


def simulation(routes, drones, obstacles=None, pre_planned=False):
    if len(routes) != len(drones):
        print("Error: number of routes and drones don't match")
        return

    plt.style.use("grayscale")
    fig, ax = plt.subplots(layout="constrained", figsize=(14, 10))
    ax.set_facecolor("#f0f4f8")       # light blue-grey background
    fig.patch.set_facecolor("#e8edf2")
    ax.grid(color="white", linewidth=1.2)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_locator(loc(1))
    ax.xaxis.set_major_locator(loc(1))

    # Dynamic limits based on actual route data
    ax.set_xlim(-25,25)
    ax.set_ylim(-25,25)
  

    # Nice color palette — one color per drone
    palette = [
        "#e63946",  # red
        "#2a9d8f",  # teal
        "#e9c46a",  # yellow
        "#f4a261",  # orange
        "#457b9d",  # steel blue
        "#8338ec",  # purple
        "#06d6a0",  # mint
        "#fb5607",  # deep orange
        "#3a86ff",  # bright blue
        "#ff006e",  # pink
    ]

    # Create one aeroplane scatter per drone
    flying_shit = []
    for i in range(len(drones)):
        color = palette[i % len(palette)]
        scatter = ax.scatter(
            [], [],
            s=400,                   # size — large enough to see the shape
            marker=PLANE_MARKER,     # ✅ aeroplane shape
            color=color,
            edgecolors="black",
            linewidths=0.8,
            label=drones[i].drone_id,
            zorder=5
        )
        flying_shit.append({
            "drone": scatter,
            "done": False,
            "x": 0,
            "y": 0
        })

    # Build full routes
    step = 20
    full_routes = []
    for i in routes:
        if pre_planned:
            full_routes.append(np.array(i))
        else:
            full_routes.append(
                np.array([(0, 0)] + list(i) + list(reversed(i)) + [(0, 0)])
            )

    # Smooth interpolation between waypoints
    for drn in range(len(flying_shit)):
        x, y = [], []
        route_pts = full_routes[drn]
        for i in range(len(route_pts) - 1):
            x0, y0 = route_pts[i]
            x1, y1 = route_pts[i + 1]
            dist = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            steps = max(int(dist * step / 2), 2)
            x.extend(np.linspace(x0, x1, steps, endpoint=False))
            y.extend(np.linspace(y0, y1, steps, endpoint=False))
        x.append(route_pts[-1][0])
        y.append(route_pts[-1][1])
        flying_shit[drn]["x"] = np.array(x)
        flying_shit[drn]["y"] = np.array(y)

    max_frames = max(len(flying_shit[drn]["x"]) for drn in range(len(flying_shit)))

    def animate(frame):
        result = []
        for drn in range(len(flying_shit)):
            if not flying_shit[drn]["done"]:
                f = min(frame, len(flying_shit[drn]["x"]) - 1)  # clamp
                if frame != 0 and flying_shit[drn]["x"][f] == 0 and flying_shit[drn]["y"][f] == 0:
                    flying_shit[drn]["done"] = True
                    flying_shit[drn]["drone"].set_visible(False)
                else:
                    flying_shit[drn]["drone"].set_offsets(
                        (flying_shit[drn]["x"][f], flying_shit[drn]["y"][f])
                    )
            result.append(flying_shit[drn]["drone"])
        return result

    ani = funi(fig, animate, frames=max_frames, blit=True, interval=5)

    # No-fly zones as red squares
    if obstacles:
        xo, yo = zip(*[tuple(o) for o in obstacles])
        ax.scatter(xo, yo, color="#e63946", s=120, marker="s",
                   label="No Fly Zones", zorder=4, edgecolors="darkred", linewidths=1)

    # Base marker at (0,0)
    ax.scatter([0], [0], color="#2dc653", s=250, marker="*",
               label="Base (0,0)", zorder=6, edgecolors="darkgreen", linewidths=1)

    ax.set_title("✈  AeroPath — Drone Fleet Simulation", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("X Coordinate", fontsize=10)
    ax.set_ylabel("Y Coordinate", fontsize=10)
    plt.legend(loc="upper right", framealpha=0.9)
    plt.show()