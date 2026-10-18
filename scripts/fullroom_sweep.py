#!/usr/bin/env python3
import rclpy
import numpy as np
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def generate_coverage_path(x_min, x_max, y_min, y_max, step_y=0.35):
    """Generates back-and-forth boustrophedon sweep waypoints."""
    points = []
    y_coords = np.arange(y_min, y_max + step_y, step_y)
    moving_forward = True

    for y in y_coords:
        if moving_forward:
            points.append((x_min, float(y)))
            points.append((x_max, float(y)))
        else:
            points.append((x_max, float(y)))
            points.append((x_min, float(y)))
        moving_forward = not moving_forward

    return points

def create_pose(navigator, x, y):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.w = 1.0
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("Waiting for Nav2 lifecycle activation...")
    navigator.waitUntilNav2Active()
    print("Nav2 active! Generating sweep pattern.")

    # Safe room boundaries (staying clear of walls based on footprint)
    # Adjust min/max if your scanned room has different dimensions
    coords = generate_coverage_path(
        x_min=-2.4, 
        x_max=2.4, 
        y_min=-2.4, 
        y_max=2.4, 
        step_y=0.45
    )
    
    waypoints = [create_pose(navigator, x, y) for (x, y) in coords]

    print(f"Generated {len(waypoints)} sweep waypoints. Commencing floor sweep...")
    navigator.followWaypoints(waypoints)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            print(f"Sweeping line waypoint: {feedback.current_waypoint + 1}/{len(waypoints)}")

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("Floor coverage complete!")
    else:
        print(f"Sweep terminated with status: {result}")

    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()