# 🤖 VacBot: Autonomous Vacuum Cleaning Robot Simulation

[![ROS 2](https://img.shields.io/badge/ROS_2-Humble-3498DB?logo=ros)](https://docs.ros.org/en/humble/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Simulation-orange?logo=gazebo)](https://gazebosim.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Language: C++ / Python](https://img.shields.io/badge/Language-C++%20%7C%20Python-blue)](https://github.com/Tayyabaf58/vacbot)

An autonomous indoor differential-drive service robot built in **ROS 2 Humble**. The project models a complete digital twin featuring planar LiDAR, IMU sensors, tuned dynamic physics in **Gazebo**, and real-time indoor mapping via **SLAM Toolbox**.

---

<!-- Tip: Drop a 5-10 second demo GIF or screenshot inside docs/media/demo.gif -->
![VacBot Simulation Overview](docs/media/demo.gif)

---

## 📌 Project Overview & System Architecture

Autonomous indoor service robots demand tight synchronization between low-level kinematic transforms and high-level spatial estimation. VacBot implements a complete differential-drive pipeline:

- **Kinematics & Inertia:** Parametric URDF/Xacro base with calibrated center of mass, wheel separation, and friction-tuned caster dynamics to prevent odometry slip.
- **Transform Architecture:** Validated coordinate frame tree ensuring unbroken spatial transforms:  
  `map` ➔ `odom` ➔ `base_footprint` ➔ `base_link` ➔ `laser_frame`
- **Spatial Perception:** 360° Planar 2D LiDAR ray tracing combined with continuous odometry feedback.
- **Mapping:** Asynchronous lifelong mapping using **SLAM Toolbox** for drift-minimized occupancy grids.

---

## 🗂 Package Structure

```text
vacbot/
├── config/               # SLAM Toolbox & Nav2 configurations
│   ├── mapper_params_online_async.yaml
│   └── nav2_params.yaml
├── launch/               # System launch files
│   ├── rsp.launch.py     # Robot State Publisher
│   ├── sim.launch.py     # Gazebo world spawn
│   └── slam.launch.py    # SLAM Toolbox & RViz pipeline
├── description/          # Robot description (URDF/Xacro)
│   ├── robot.urdf.xacro
│   ├── robot_core.xacro
│   ├── gazebo_control.xacro
│   └── lidar.xacro
├── worlds/               # Gazebo simulation environments
│   └── indoor_house.world
├── rviz/                 # Default RViz display configurations
│   └── view_robot.rviz
├── CMakeLists.txt
└── package.xml
