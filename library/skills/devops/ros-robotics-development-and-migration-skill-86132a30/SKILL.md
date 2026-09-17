---
name: "ros-robotics"
description: "Skill for ROS 1/ROS 2 robot development, migration, and integration covering build systems, launch, URDF, navigation, control, simulation, Docker, CI/CD, and micro-ROS."
---

# ROS Robotics

## When to Use

Use this skill when the user request involves any of the following topics:

- `catkin_ws`, `colcon_ws`, `src/CMakeLists.txt`, `package.xml`, `setup.py`
- Creating, migrating, building, testing, or debugging ROS 1 / ROS 2 packages
- `launch` / `launch.py`, parameter YAML, `URDF/Xacro`, RViz, TF
- `topic` / `service` / `action` / `msg` / `srv` / `QoS`
- Chassis, IMU, LiDAR, camera, localization, SLAM, Navigation2, `ros2_control`
- Gazebo / Ignition simulation, sensor simulation, `ros_gz_bridge`
- Docker containerized ROS development, `docker-compose` multi‑node orchestration
- Lifecycle nodes, `rclcpp_components` componentization, intra‑process communication
- `rosbag2` recording/playback, `mcap`, offline diagnostics
- SLAM mapping (Cartographer, SLAM Toolbox, ORB‑SLAM)
- DDS / QoS configuration, `ROS_DOMAIN_ID`, RMW selection, multi‑machine networking
- Custom `msg` / `srv` / `action` interface definition and generation
- Multi‑robot systems, namespace isolation, cross‑machine communication
- MoveIt 2 motion planning, SRDF, kinematics plugins
- ROS 2 CI/CD (GitHub Actions, colcon test, ament lint)
- Foxglove Studio / PlotJuggler data visualization and offline analysis
- MCU / RTOS / UART / CAN / `micro-ROS` collaborative development

## Initial Steps

### 1. Detect the workspace
```bash
python scripts/detect_ros_workspace.py <workspace-path>
```

### 2. Perform consistency check
```bash
python scripts/check_ros_workspace_consistency.py <workspace-path>
```

### 3. Load the minimal required documentation
- ROS 1: `references/ros1-catkin.md`
- ROS 2: `references/ros2-colcon.md`
- Mixed / Migration: `references/interop-and-migration.md`
- Model / TF: `references/robot-description-and-tf.md`
- Navigation: `references/navigation2.md`
- Control: `references/ros2-control.md`
- Embedded: `references/micro-ros-and-embedded.md`
- Simulation: `references/gazebo-simulation.md`
- Lifecycle / Components: `references/lifecycle-and-components.md`
- DDS / QoS / Networking: `references/dds-qos-networking.md`
- Recording / Diagnostics: `references/rosbag-diagnostics.md`
- SLAM / Mapping: `references/slam-mapping.md`
- Docker: `references/docker-ros.md`
- Custom Interfaces: `references/custom-interfaces.md`
- Multi‑robot: `references/multi-robot.md`
- MoveIt 2: `references/moveit2.md`
- CI/CD: `references/ros2-cicd.md`
- Visualization: `references/foxglove-visualization.md`
- Troubleshooting: `references/debug-playbooks.md`
- Review Checklist: `references/review-checklist.md`

## Mandatory Principles

- Identify the build system before modifying code.
- Ensure `package.xml` and `CMakeLists.txt` consistency before refactoring.
- Verify TF, timestamps, frames, and units before blaming algorithms.
- Keep an evidence chain: build output, topics, TF, parameters, logs must be verifiable.
- For ROS 1 → ROS 2 migration, bridge or layer first; avoid a complete rewrite.
- For MCU / `micro-ROS`, confirm the need to join the ROS graph before adding complexity.

## Common Task Workflows

### Adding or Fixing a Package
- Determine package type: `catkin`, `ament_cmake`, or `ament_python`.
- Add missing dependencies, then adjust build logic, then update install rules.
- For custom `msg` / `srv` / `action`, verify generation order and dependency closure (see `references/custom-interfaces.md`).

### Build Failures
1. Run `rosdep`.
2. Check `package.xml` against build scripts.
3. Ensure the environment is correctly sourced.
4. Verify system dependencies, ABI compatibility, and distro support.

### Robot Behaves Unexpectedly
1. Inspect launch files, namespaces, remappings, and parameters.
2. Check topic names, frequencies, timestamps, units, and `frame_id`.
3. Examine TF tree for single‑root consistency; differentiate static vs dynamic transforms.
4. Only then question the algorithm.

### Navigation2 / `ros2_control`
- Nav2: prioritize `/cmd_vel` link, localization quality, control frequency, and chassis units.
- `ros2_control`: prioritize hardware interface type, controller YAML, read/write cycles, and active state.

### MCU / `micro-ROS`
- Determine if a Linux bridge node suffices.
- If MCU must join ROS 2 graph, consider `micro-ROS`.
- Rigorously check byte order, checksums, timeouts, reconnection logic, time source, and loss‑of‑connection protection.

## Anti‑Patterns
- Mixing `catkin` and `ament` in the same package.
- Modifying only `CMakeLists.txt` without updating `package.xml`.
- Ignoring TF, timestamps, units, or coordinate‑frame definitions.
- Packing drivers, protocols, filtering, control, and diagnostics into a single monolithic node.
- Migrating ROS 1 → ROS 2 by only swapping APIs without system verification.

## Output Requirements
When using this skill, prioritize the following sections in the response:

1. Current workspace and package type determination.
2. Key evidence and assumptions.
3. Modification points and rationale.
4. Minimal build / test / run commands.
5. Risk areas and regression‑check points.
