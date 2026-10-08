# AI Traffic Management System 🚦🤖

An intelligent, computer vision-driven traffic control system designed to optimize traffic signal management, manage rush-hour flow, and prioritize emergency vehicles in real time. By utilizing object detection and multi-signal coordination, the system dynamically adapts to live vehicle density to reduce congestion and clear critical routes.

---

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Computer Vision**: OpenCV
- **Object Detection**: YOLOv8 (Ultralytics)

---

## 🌟 Key Features

- **Density-Based Dynamic Timers**: Automatically calculates and adjusts traffic signal green light durations based on real-time vehicle counts instead of fixed timers.
- **Custom Peak-Hour Scheduling**: Applies customized timing parameters during peak office commute times (morning and evening) to accommodate heavy directional traffic flow.
- **Emergency Vehicle Detection & Lane Extension**: Detects emergency vehicles (e.g., ambulances, fire trucks, police cars) via YOLOv8 and automatically extends the green light timer for that specific lane.
- **Inter-Signal Emergency Alerts**: Forwards incoming emergency vehicle notifications from one signal to the next downstream traffic signal, giving commuters and operators advance warning to clear the route.
- **Vehicle Classification & Counting**: Tracks and counts cars, buses, trucks, motorcycles, and emergency vehicles across lanes.
- **Video Feed Analysis**: Processes pre-recorded traffic video feeds for testing, simulation, and validation before real-time deployment.

---

## 🚀 Future Roadmap

- [ ] **Live RTSP Stream Integration**: Transition from video files to live webcams and IP camera streams.
- [ ] **Grid-Wide Signal Syncing**: Expand downstream notifications across multi-intersection urban networks.
- [ ] **Digital Signage Integration**: Relay downstream emergency alerts to digital roadside displays for clear driver visibility.
