# LUSAS API (LPI) EXAMPLES
# (https://github.com/LUSAS-Software/LUSAS-API-Examples/)
#
# Example:      505 Output Monitoring.py
# Author:       Finite Element Analysis Ltd
# Description: Convert a log file into a graphical visualisation
    # Users are required to specify the log file location.
    # Additional related parameters may be modified as required.
    # This file can be executed prior to or following execution of LUSAS Modeller.
#######################################################################

# Libraries:
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from pathlib import Path

# ============= CONFIGURATION =============
LOG_FILE = r'path to log file' # User needs to provide log file path.

UPDATE_INTERVAL = 2000  # milliseconds
AUTO_DELETE_OLD_LOG = False
MONITOR_NEW_ONLY = False
# =========================================

# Delete old log file if requested
if AUTO_DELETE_OLD_LOG and Path(LOG_FILE).exists():
    try:
        Path(LOG_FILE).unlink()
        print(f"Deleted old log file")
    except Exception as e:
        print(f"Could not delete: {e}")

# Track file position
if MONITOR_NEW_ONLY and Path(LOG_FILE).exists():
    try:
        with open(LOG_FILE, 'rb') as f:
            f.seek(0, 2)
            last_position = f.tell()
        print(f"Monitoring only NEW data (skipping {last_position} bytes)")
    except:
        last_position = 0
else:
    last_position = 0

# Data storage
increment = []
iteration = []
MAR = []
RMS = []
ENGY = []
PLWRK = []
TLMDA = []
converged = []

def read_and_parse():
    """Read new data from log file and parse it"""
    global last_position # This allows the function to resume reading where it left off
    
    try:
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'ascii']:
            try:
                with open(LOG_FILE, 'r', encoding=encoding, errors='ignore') as f:
                    f.seek(last_position)
                    new_data = f.read()
                    last_position = f.tell()
                    
                    if new_data:
                        parse_data(new_data)
                        return True
                break
            except UnicodeDecodeError:
                continue
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    return False

def parse_data(text):
    """Parse LUSAS log data"""
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        if 'INCREMENT' in line and 'ITERATION' in line:
            parts = line.split()
            try:
                inc_idx = parts.index('INCREMENT') + 1
                iter_idx = parts.index('ITERATION') + 1
                inc = int(parts[inc_idx])
                it = int(parts[iter_idx])
                
                # Check if converged
                conv = False
                for j in range(i, min(i + 20, len(lines))):
                    if '***INCREMENT HAS CONVERGED***' in lines[j]:
                        conv = True
                        break
                
                # Extract metrics
                mar_val = np.nan
                rms_val = np.nan
                engy_val = np.nan
                plwrk_val = np.nan
                tlmda_val = np.nan
                
                for j in range(i + 1, min(i + 15, len(lines))):
                    if 'MAR' in lines[j]:
                        vals = re.findall(r'[-+]?\d*\.\d+E[-+]\d+|\d+\.\d+', lines[j])
                        if len(vals) >= 2:
                            mar_val = float(vals[0])
                            rms_val = float(vals[1])
                    if 'ENGY' in lines[j]:
                        vals = re.findall(r'[-+]?\d*\.\d+E[-+]\d+|\d+\.\d+', lines[j])
                        if len(vals) >= 2:
                            engy_val = float(vals[0])
                            plwrk_val = float(vals[1])
                    if 'TLMDA' in lines[j]:
                        match = re.search(r'TLMDA\s+([-+]?\d*\.\d+)', lines[j])
                        if match:
                            tlmda_val = float(match.group(1))
                
                if not all(np.isnan([mar_val, rms_val, engy_val, plwrk_val, tlmda_val])):
                    increment.append(inc)
                    iteration.append(it)
                    MAR.append(mar_val)
                    RMS.append(rms_val)
                    ENGY.append(engy_val)
                    PLWRK.append(plwrk_val)
                    TLMDA.append(tlmda_val)
                    converged.append(conv)
                    
            except (ValueError, IndexError):
                continue

# Create plots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle('LUSAS Nonlinear Analysis Progress (LIVE)', fontsize=16, fontweight='bold')

# Initialize lines
line_mar, = axes[0, 0].plot([], [], 'o-', color='steelblue', linewidth=2, markersize=4)
line_rms, = axes[0, 1].plot([], [], 'o-', color='coral', linewidth=2, markersize=4)
line_tlmda, = axes[0, 2].plot([], [], 'o-', color='green', linewidth=2, markersize=4)
line_engy, = axes[1, 0].plot([], [], 'o-', color='purple', linewidth=2, markersize=4)
line_plwrk, = axes[1, 1].plot([], [], 'o-', color='darkred', linewidth=2, markersize=4)

# Setup axes
axes[0, 0].set_title('Maximum Absolute Residual')
axes[0, 0].set_ylabel('MAR (log scale)', fontweight='bold')
axes[0, 0].set_xlabel('Analysis Step')
axes[0, 0].set_yscale('log')
axes[0, 0].grid(True, alpha=0.3)

axes[0, 1].set_title('Root Mean Square Residual')
axes[0, 1].set_ylabel('RMS (log scale)', fontweight='bold')
axes[0, 1].set_xlabel('Analysis Step')
axes[0, 1].set_yscale('log')
axes[0, 1].grid(True, alpha=0.3)

axes[0, 2].set_title('Total Load Factor (TLMDA)')
axes[0, 2].set_ylabel('Load Factor', fontweight='bold')
axes[0, 2].set_xlabel('Analysis Step')
axes[0, 2].grid(True, alpha=0.3)

axes[1, 0].set_title('Total Strain Energy')
axes[1, 0].set_ylabel('Energy', fontweight='bold')
axes[1, 0].set_xlabel('Analysis Step')
axes[1, 0].grid(True, alpha=0.3)

axes[1, 1].set_title('Total Plastic Work')
axes[1, 1].set_ylabel('Plastic Work', fontweight='bold')
axes[1, 1].set_xlabel('Analysis Step')
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].set_title('Iterations per Increment')
axes[1, 2].set_ylabel('Max Iterations', fontweight='bold')
axes[1, 2].set_xlabel('Increment Number')
axes[1, 2].grid(True, alpha=0.3, axis='y')

status_text = fig.text(0.02, 0.02, 'Status: Waiting for data...', fontsize=10,
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Store zoomed windows
zoom_windows = []

def create_zoom_window(plot_type):
    """Create a zoomed window for a specific plot"""
    zoom_fig, zoom_ax = plt.subplots(figsize=(12, 8))
    
    if plot_type == 'MAR':
        zoom_ax.set_title('Maximum Absolute Residual (MAR) - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('MAR (log scale)', fontweight='bold', fontsize=12)
        zoom_ax.set_yscale('log')
        zoom_line, = zoom_ax.plot([], [], 'o-', color='steelblue', linewidth=2, markersize=6)
    elif plot_type == 'RMS':
        zoom_ax.set_title('Root Mean Square Residual (RMS) - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('RMS (log scale)', fontweight='bold', fontsize=12)
        zoom_ax.set_yscale('log')
        zoom_line, = zoom_ax.plot([], [], 'o-', color='coral', linewidth=2, markersize=6)
    elif plot_type == 'TLMDA':
        zoom_ax.set_title('Total Load Factor (TLMDA) - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('Load Factor', fontweight='bold', fontsize=12)
        zoom_line, = zoom_ax.plot([], [], 'o-', color='green', linewidth=2, markersize=6)
    elif plot_type == 'ENGY':
        zoom_ax.set_title('Total Strain Energy (ENGY) - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('Energy', fontweight='bold', fontsize=12)
        zoom_line, = zoom_ax.plot([], [], 'o-', color='purple', linewidth=2, markersize=6)
    elif plot_type == 'PLWRK':
        zoom_ax.set_title('Total Plastic Work (PLWRK) - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('Plastic Work', fontweight='bold', fontsize=12)
        zoom_line, = zoom_ax.plot([], [], 'o-', color='darkred', linewidth=2, markersize=6)
    elif plot_type == 'ITER':
        zoom_ax.set_title('Iterations per Increment - ZOOMED', fontsize=14, fontweight='bold')
        zoom_ax.set_ylabel('Max Iterations', fontweight='bold', fontsize=12)
        zoom_line = None
    
    zoom_ax.set_xlabel('Analysis Step', fontsize=12)
    zoom_ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show(block=False)
    
    zoom_windows.append({'fig': zoom_fig, 'ax': zoom_ax, 'line': zoom_line, 'type': plot_type})

def on_double_click(event):
    """Handle double-click to zoom"""
    if event.dblclick and event.inaxes:
        if event.inaxes == axes[0, 0]:
            create_zoom_window('MAR')
        elif event.inaxes == axes[0, 1]:
            create_zoom_window('RMS')
        elif event.inaxes == axes[0, 2]:
            create_zoom_window('TLMDA')
        elif event.inaxes == axes[1, 0]:
            create_zoom_window('ENGY')
        elif event.inaxes == axes[1, 1]:
            create_zoom_window('PLWRK')
        elif event.inaxes == axes[1, 2]:
            create_zoom_window('ITER')

fig.canvas.mpl_connect('button_press_event', on_double_click)

def update(frame):
    """Update plots"""
    has_new = read_and_parse()
    
    if len(increment) > 0:
        x = np.arange(len(increment))
        
        # Update MAR
        valid = [(i, v) for i, v in zip(x, MAR) if not np.isnan(v) and v > 0]
        if valid:
            x_val, y_val = zip(*valid)
            line_mar.set_data(x_val, y_val)
            axes[0, 0].relim()
            axes[0, 0].autoscale_view()
        
        # Update RMS
        valid = [(i, v) for i, v in zip(x, RMS) if not np.isnan(v) and v > 0]
        if valid:
            x_val, y_val = zip(*valid)
            line_rms.set_data(x_val, y_val)
            axes[0, 1].relim()
            axes[0, 1].autoscale_view()
        
        # Update TLMDA
        valid = [(i, v) for i, v in zip(x, TLMDA) if not np.isnan(v)]
        if valid:
            x_val, y_val = zip(*valid)
            line_tlmda.set_data(x_val, y_val)
            axes[0, 2].relim()
            axes[0, 2].autoscale_view()
        
        # Update ENGY
        valid = [(i, v) for i, v in zip(x, ENGY) if not np.isnan(v)]
        if valid:
            x_val, y_val = zip(*valid)
            line_engy.set_data(x_val, y_val)
            axes[1, 0].relim()
            axes[1, 0].autoscale_view()
        
        # Update PLWRK
        valid = [(i, v) for i, v in zip(x, PLWRK) if not np.isnan(v)]
        if valid:
            x_val, y_val = zip(*valid)
            line_plwrk.set_data(x_val, y_val)
            axes[1, 1].relim()
            axes[1, 1].autoscale_view()
        
        # Update iterations bar plot
        axes[1, 2].clear()
        incs = []
        max_its = []
        curr_inc = increment[0]
        curr_max = 0
        
        for inc, it in zip(increment, iteration):
            if inc != curr_inc:
                incs.append(curr_inc)
                max_its.append(curr_max)
                curr_inc = inc
                curr_max = it
            else:
                curr_max = max(curr_max, it)
        
        incs.append(curr_inc)
        max_its.append(curr_max)
        
        axes[1, 2].bar(incs, max_its, color='teal', alpha=0.7)
        axes[1, 2].set_ylabel('Max Iterations', fontweight='bold')
        axes[1, 2].set_xlabel('Increment Number')
        axes[1, 2].set_title('Iterations per Increment')
        axes[1, 2].grid(True, alpha=0.3, axis='y')
        
        # Update zoomed windows
        for zoom in zoom_windows:
            if not plt.fignum_exists(zoom['fig'].number):
                continue
            
            if zoom['type'] == 'MAR':
                valid = [(i, v) for i, v in zip(x, MAR) if not np.isnan(v) and v > 0]
                if valid and zoom['line']:
                    x_val, y_val = zip(*valid)
                    zoom['line'].set_data(x_val, y_val)
                    zoom['ax'].relim()
                    zoom['ax'].autoscale_view()
                    zoom['fig'].canvas.draw_idle()
            
            elif zoom['type'] == 'RMS':
                valid = [(i, v) for i, v in zip(x, RMS) if not np.isnan(v) and v > 0]
                if valid and zoom['line']:
                    x_val, y_val = zip(*valid)
                    zoom['line'].set_data(x_val, y_val)
                    zoom['ax'].relim()
                    zoom['ax'].autoscale_view()
                    zoom['fig'].canvas.draw_idle()
            
            elif zoom['type'] == 'TLMDA':
                valid = [(i, v) for i, v in zip(x, TLMDA) if not np.isnan(v)]
                if valid and zoom['line']:
                    x_val, y_val = zip(*valid)
                    zoom['line'].set_data(x_val, y_val)
                    zoom['ax'].relim()
                    zoom['ax'].autoscale_view()
                    zoom['fig'].canvas.draw_idle()
            
            elif zoom['type'] == 'ENGY':
                valid = [(i, v) for i, v in zip(x, ENGY) if not np.isnan(v)]
                if valid and zoom['line']:
                    x_val, y_val = zip(*valid)
                    zoom['line'].set_data(x_val, y_val)
                    zoom['ax'].relim()
                    zoom['ax'].autoscale_view()
                    zoom['fig'].canvas.draw_idle()
            
            elif zoom['type'] == 'PLWRK':
                valid = [(i, v) for i, v in zip(x, PLWRK) if not np.isnan(v)]
                if valid and zoom['line']:
                    x_val, y_val = zip(*valid)
                    zoom['line'].set_data(x_val, y_val)
                    zoom['ax'].relim()
                    zoom['ax'].autoscale_view()
                    zoom['fig'].canvas.draw_idle()
            
            elif zoom['type'] == 'ITER':
                zoom['ax'].clear()
                zoom['ax'].bar(incs, max_its, color='teal', alpha=0.7)
                zoom['ax'].set_ylabel('Max Iterations', fontweight='bold', fontsize=12)
                zoom['ax'].set_xlabel('Increment Number', fontsize=12)
                zoom['ax'].set_title('Iterations per Increment - ZOOMED', fontsize=14, fontweight='bold')
                zoom['ax'].grid(True, alpha=0.3, axis='y')
                zoom['fig'].canvas.draw_idle()
        
        # Update status
        status = f"Status: Running | Steps: {len(increment)} | Inc: {increment[-1]} | Load: {TLMDA[-1]:.4f}"
        if has_new:
            status += " | NEW"
        status_text.set_text(status)
    
    return [line_mar, line_rms, line_tlmda, line_engy, line_plwrk, status_text]

# Start animation
anim = FuncAnimation(fig, update, interval=UPDATE_INTERVAL, blit=False, cache_frame_data=False)

plt.tight_layout()
plt.subplots_adjust(bottom=0.08)

print("="*60)
print("LUSAS LIVE MONITOR")
print("="*60)
print(f"Monitoring: {LOG_FILE}")
print(f"Update interval: {UPDATE_INTERVAL/1000} seconds")
print("TIP: Double-click any plot to zoom in!")
print("="*60)

plt.show()

# Final summary
if len(increment) > 0:
    print("\n" + "="*60)
    print("FINAL SUMMARY")
    print("="*60)
    print(f"Total Increments: {max(increment)}")
    print(f"Total Steps: {len(increment)}")
    print(f"Final Load Factor: {TLMDA[-1]:.5f}")
    print(f"Final Energy: {ENGY[-1]:.3f}")
    print(f"Final Plastic Work: {PLWRK[-1]:.5f}")
    print(f"Converged Increments: {sum(converged)}")
    print("="*60)
