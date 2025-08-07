# Leaf Flow Animation: Navier-Stokes Visualization

## Overview

This Python program, `leaf_flow.py`, is an educational animation that simulates a leaf flowing through a pipe with a smooth (laminar) water flow, designed to illustrate concepts related to the **Navier-Stokes Existence and Smoothness problem**, one of the Clay Mathematics Institute’s Millennium Prize Problems. The animation visualizes:
- A **red line** representing the *predicted path* of the leaf, following an ideal laminar flow (parabolic velocity profile).
- A **green dot and line** representing the *actual path* of the leaf, with random perturbations to simulate real-world variability.
- Statistical analysis of the leaf’s deviation from the predicted path over 30 runs, displayed after completion.

The program uses **Pygame** in a **Pyodide**-compatible format to run in a browser, with physical units (meters and seconds) for realism. It includes titles, an x-y ruler, and deviation statistics to enhance learning about fluid dynamics and the Navier-Stokes challenge of determining whether fluid flow solutions remain smooth or develop singularities.

## Purpose

The animation serves as an educational tool to:
- Demonstrate the difference between an ideal fluid flow (smooth, deterministic) and a real-world flow with perturbations (random deviations).
- Quantify deviations using statistical metrics (average, maximum, and standard deviation).
- Provide a visual and interactive way to explore fluid dynamics concepts, such as laminar vs. turbulent flow, relevant to the Navier-Stokes problem.
- Allow users to experiment with parameters like velocity and perturbations to observe their impact on flow behavior.

Key features:
- **Physical Units**: Positions in meters, velocities in m/s, time in seconds.
- **30 Runs**: The leaf completes 30 trips across the pipe, then displays statistics.
- **Titles**: Explain the red line (predicted path) and green dot (floating leaf).
- **X-Y Ruler**: Shows scale in meters for spatial reference.
- **Statistics**: Average, maximum, and standard deviation of the leaf’s y-deviation from the predicted path.

## Prerequisites

To run `leaf_flow.py`, you need:
1. **Python 3.7+** (for local execution, though Pyodide is preferred for browser compatibility).
2. **Pygame**: A Python library for 2D graphics and animation.
   - Install via pip: `pip install pygame`
3. **Pyodide**: A Python runtime for the browser, required to run the code as intended.
   - Pyodide is typically embedded in an HTML file (see `index.html` example below).
   - No local installation is needed if using a web-based Pyodide environment.
4. **Web Browser**: Chrome, Firefox, or Edge for running the Pyodide-based HTML file.
5. **Optional: Web Server**: To serve the HTML file locally (e.g., Python’s `http.server`).
   - Run: `python -m http.server 8000` and access `http://localhost:8000/index.html`.

### Optional HTML File
To run the animation in a browser, create an `index.html` file in the same directory as `leaf_flow.py`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Leaf Flow Animation</title>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>
</head>
<body>
    <script>
        async function main() {
            let pyodide = await loadPyodide();
            await pyodide.loadPackage("pygame");
            let code = await (await fetch("leaf_flow.py")).text();
            await pyodide.runPythonAsync(code);
        }
        main();
    </script>
</body>
</html>
```

- Save as `index.html`.
- Serve via a web server (e.g., `python -m http.server`) and open in a browser.
- Pyodide automatically handles Pygame dependencies in the browser.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/montereytony/leaf-flow-animation.git
   cd leaf-flow-animation
   ```

2. **Install Pygame (Optional, for Local Execution)**:
   ```bash
   pip install pygame
   ```

3. **Run Locally (works in my MacBookPro)**:
   - Execute `python leaf_flow.py` to run in a local Pygame window.
   - Note: Local execution may not handle the async Pyodide structure perfectly.

4. **Run in Browser (Recommended)**:
   - Create `index.html` as shown above.
   - Serve the directory: `python -m http.server 8000`
   - Open `http://localhost:8000/index.html` in a browser.
   - Pyodide loads Pygame and runs the animation.

## Usage

- **Browser**: Open `index.html` in a browser via a web server. The animation starts automatically, showing a leaf (green dot) moving through a pipe (blue) with a red predicted path and green actual path.
- **Animation**: The leaf completes 30 runs (each ~11 seconds), displaying the current run number (e.g., “Run: 1/30”). After 30 runs, the animation pauses, showing deviation statistics.
- **Titles**: Explain the red line (“Predicted Path: Ideal Laminar Flow”) and green dot (“Floating Leaf: Actual Path with Perturbations”).
- **Ruler**: X-axis (0 to 6 m) below the pipe, y-axis (1.0 to 3.0 m) on the left, for scale.
- **Output**: After 30 runs, see:
  - Average deviation (m): Mean y-distance from `y=2.0 m`.
  - Maximum deviation (m): Largest y-distance.
  - Standard deviation (m): Variability of deviations.

## Variables

Below are the key variables in `leaf_flow.py`, their units, and their roles:

| **Variable**            | **Type/Value**         | **Units**         | **Description**                                                                 |
|-------------------------|------------------------|-------------------|---------------------------------------------------------------------------------|
| `WIDTH`, `HEIGHT`       | 6.0, 4.0              | Meters            | Window dimensions (6 m wide, 4 m tall), scaled to pixels for display.            |
| `PIXELS_PER_METER`      | 100                   | Pixels/meter      | Conversion factor (1 m = 100 pixels) for rendering.                              |
| `FPS`                   | 60                    | Frames/second     | Frame rate, controlling animation speed.                                         |
| `FRAME_TIME`            | 1/60 ≈ 0.0167         | Seconds           | Time per frame (1/FPS).                                                          |
| `PIPE_TOP`, `PIPE_BOTTOM` | 1.0, 3.0            | Meters            | Pipe boundaries (y=1.0 m to y=3.0 m), defining the flow channel.                 |
| `leaf_pos`              | [0.5, 2.0]            | Meters            | Leaf’s current position (x, y), starting at x=0.5 m, y=2.0 m (pipe center).      |
| `leaf_radius`           | 0.05                  | Meters            | Leaf radius (5 cm), used for boundary clamping and rendering.                    |
| `leaf_speed`            | 1.0                   | Dimensionless     | Scaling factor (set to 1 for physical units).                                    |
| `predicted_path`        | List of (x, y) tuples | Meters            | Red line path, computed deterministically using parabolic flow.                  |
| `actual_path`           | List of (x, y) tuples | Meters            | Green line path, tracking leaf’s actual position with perturbations.             |
| `run_count`             | Integer (0 to 29)     | None              | Current run number (out of 30).                                                  |
| `max_runs`              | 30                    | None              | Total number of runs before displaying stats.                                    |
| `all_deviations`        | List of lists         | Meters            | Y-deviations (`|actual_y - 2.0|`) for each run, used for statistics.             |
| `running`               | Boolean               | None              | True during animation, False when showing stats after 30 runs.                   |
| `max_vx` (in `get_flow_velocity`) | 0.5         | Meters/second     | Maximum x-velocity at pipe center (parabolic profile).                           |
| `vy` (in `get_flow_velocity`) | 0.0           | Meters/second     | Y-velocity (0 for laminar flow).                                                   |
| `perturbation`          | random.uniform(-0.5, 0.9) | Meters/second | Random velocity perturbation (±50–90 cm/s), causing actual path deviations.      |
| `repulsion`             | -0.3 * (distance/1.0)³ | Meters/second²   | Repulsive force to keep leaf from pipe walls, scaled by frame time.              |
| `dt` (in `predict_path`) | 0.1                  | Seconds           | Time step for predicted path calculation.                                        |

### Key Functions
- `get_flow_velocity(y)`: Returns parabolic velocity (m/s) at y-position, max 0.5 m/s at pipe center (`y=2.0 m`).
- `predict_path(start_x, start_y)`: Computes red line path using deterministic flow, up to `x=6.0 m`.
- `compute_stats(deviations)`: Calculates average, maximum, and standard deviation of y-deviations.
- `display_stats(avg_dev, max_dev, std_dev)`: Shows stats, titles, and ruler after 30 runs.
- `draw_ruler()`: Draws x-y axes with ticks (x: every 1 m, y: every 0.5 m) and labels in meters.
- `setup()`: Initializes leaf position, paths, and deviations for each run.
- `update_loop()`: Updates leaf position, draws animation, and tracks deviations.

## Navier-Stokes Connection

The Navier-Stokes Existence and Smoothness problem asks whether solutions to the Navier-Stokes equations (describing fluid motion) always exist and remain smooth in 3D, or if they can develop singularities (e.g., infinite velocities). This program:
- Simulates a simplified 2D laminar flow (parabolic profile, `vy=0`) to represent a smooth solution (red line).
- Adds random perturbations (±50–90 cm/s) to mimic real-world disturbances, causing the actual path (green line) to deviate.
- Quantifies deviations statistically, showing how disturbances affect flow stability, a key aspect of the Navier-Stokes question.
- Uses meters and seconds to align with physical fluid dynamics, with a Reynolds number (`Re ≈ 100,000` for water, pipe height 2 m, velocity 0.5 m/s) suggesting potential turbulence in reality, though enforced as laminar here.

## Customization

To experiment with the animation:
- **Velocity**: Change `max_vx` in `get_flow_velocity` (e.g., 1.0 m/s for faster runs).
- **Perturbations**: Adjust `random.uniform(-0.5, 0.9)` in `update_loop` (e.g., `(-0.3, 0.3)` for less deviation).
- **Runs**: Modify `max_runs` (e.g., 10 for quicker testing).
- **Pause**: Add a key listener (e.g., spacebar) to pause/resume (requires code modification).
- **Stats Plot**: Visualize deviations over x-position (needs additional plotting library or canvas).

## Limitations

- **Simplified Flow**: Uses a fixed parabolic velocity profile, not solving full Navier-Stokes equations (no pressure or viscosity).
- **2D Simulation**: Navier-Stokes problem is 3D; this is a 2D approximation for visualization.
- **Pyodide Constraints**: No file I/O or network calls; requires browser for Pyodide compatibility.
- **Runtime**: 30 runs at ~11 seconds each (~5.5 minutes) may be slow; adjust `max_vx` or `max_runs` for faster testing.

## Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Suggestions:
- Add pause/resume functionality.
- Implement a deviation plot.
- Extend to 3D flow visualization (requires significant changes).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- Built with **Pygame** and **Pyodide** for educational visualization.
- Inspired by the Navier-Stokes Existence and Smoothness problem, a Clay Millennium Prize Problem.
- Developed as a learning tool to explore fluid dynamics interactively.
