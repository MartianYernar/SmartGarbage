# SmartGarbage (KokysGet) — vision-based automatic waste sorter

An AI-powered bin that **sees a piece of waste and sorts it into the right
compartment automatically.** A camera streams the item to a computer-vision
model, and a servo rotates the bin to drop it into one of four streams:
**organic, glass, plastic, paper.**

Built end-to-end (hardware + ML + firmware) and demonstrated as a full-sized
working unit.

🏆 **National BECO Hackathon 2025 — 1st place · Infomatrix Asia 2025 — Bronze**

📊 Pitch deck: [Canva](https://www.canva.com/design/DAGXf8WjhZ8/ha59mwm8Vow3WQkOa94uDQ/view)

## How it works

```
 ESP32 camera  ──WiFi (HTTP JPEG)──▶  host (Raspberry Pi)         microcontroller ──▶ servo
 streams frames                       runs YOLOv8 on each frame    rotates bin to
                                       detects the waste class ──serial(angle)──▶ the matching stream
```

1. **`WifiCam.ino` / `WifiCam.hpp`** — ESP32 camera firmware; serves the live
   frame as a JPEG over WiFi.
2. **`main.py`** — on the host: grabs the frame, runs the YOLOv8 model
   (`best.pt`), reads the detected class, and sends the target servo angle
   (organic → 0°, glass → 90°, plastic → 180°, paper → 270°) over serial.
3. **`garbage_can_serial.ino` / `handlers.cpp`** — microcontroller firmware that
   receives the angle and drives the sorting servo.

## The model

- **YOLOv8** (Ultralytics) object detector, **trained on a self-labeled waste
  dataset of ~800 annotated images** across the four classes.
- Training pipeline in **`Waste_detection_AI.ipynb`**; trained weights in
  **`best.pt`**.

## Hardware

- ESP32 camera module (WiFi frame streaming)
- Raspberry Pi (host running inference)
- Microcontroller-driven sorting **servo**
- **3D-printed chassis** (STL parts)

## Repository layout

| File | Purpose |
|------|---------|
| `main.py` | Host inference loop: capture → YOLOv8 → serial servo command |
| `Waste_detection_AI.ipynb` | YOLOv8 training on the custom waste dataset |
| `best.pt` | Trained YOLOv8 weights |
| `WifiCam.ino`, `WifiCam.hpp` | ESP32 camera firmware |
| `garbage_can_serial.ino`, `handlers.cpp` | Servo / sorting controller firmware |
| `IBests team _ Smart Garbage Can_pdf.pdf` | Project presentation |

## Running it

```bash
pip install ultralytics opencv-python pyserial numpy
# 1) flash WifiCam.ino to the ESP32 camera; note its IP address
# 2) flash garbage_can_serial.ino to the servo controller
# 3) set the camera URL and serial COM port at the top of main.py
python main.py
```

## Status & notes

Demonstrated as a working full-sized unit (school pilot, ~10–20 items/day).
Some experimental scripts and the full training dataset are kept out of this
repo to keep it lightweight; the trained model and core code are included.

## Author

Yernar Mars — [github.com/MartianYernar](https://github.com/MartianYernar)
