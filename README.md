# render_farm_v1
A simple LAN-based Blender render farm prototype that splits animation frames across multiple machines to render in parallel using a master–worker model.


# LAN Blender Render Farm (Prototype)

A lightweight **LAN-based distributed rendering system for Blender**.  
Multiple laptops on the same network collaborate to render an animation by **splitting frames** across machines.

This project is a **learning + prototype render farm**, not a replacement for commercial solutions.

---

## Features

- Master–Worker architecture
- Password-protected worker join
- Frame-level distribution
- Master also renders (no idle GPU)
- Blender CLI (headless rendering)
- LAN-only (no internet required)
- Simple Python-based implementation

---

## How It Works



1. One machine acts as the **Master (Server)**
2. Other machines act as **Workers (Clients)**
3. Workers join the master using:
   - IP address
   - Port
   - Passcode
4. The master divides animation frames between:
5. Each machine renders its assigned frame range
6. Workers send rendered frames back to the master
7. Master stitches all frames into the final video

---

##  Requirements

### All Machines
- Python 3.8+
- Blender (same version on all machines)
- Same render engine (Cycles / Eevee)
- Same GPU backend (CUDA / OptiX / HIP)
- `.blend` file with **packed textures**

### Master Only
- FFmpeg (for video stitching)

---

## Project Structure
render_farm/
├── master.py # Runs on master
├── worker.py # Runs on worker nodes
├── scene.blend
├── output/
│ ├── master/
│ ├── node1/
│ ├── node2/
...


---

##  Authentication

Workers must provide a **passcode** to join the master server.  
Connections with an incorrect passcode are rejected.

---

##  Frame Distribution Logic

Example:
Total frames: 240
Workers: 4
Master: 1
Total renderers: 5

Frames per renderer = 240 / 5 = 48


---

##  Usage

### Prepare the Blender File
- Open Blender
- Pack all external assets:
File → External Data → Pack Resources
- Save as `scene.blend`

---

### Start the Master Server

On the master machine:
```bash
python master.py
```

Expected output:
Master listening...

Start Worker Nodes

On each worker machine:
```bash
python worker.py
```
Workers will:
Authenticate with the master
Receive a frame range
Render frames automatically
Send rendered frames back

### Stitcing the video
ffmpeg -framerate 24 -i frame_%04d.png final.mp4



