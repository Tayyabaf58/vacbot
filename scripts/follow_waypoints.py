#!/usr/bin/env python3
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

def create_pose(navigator, x, y, yaw_z=0.0, yaw_w=1.0):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = yaw_z
    pose.pose.orientation.w = yaw_w
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()

    print("Waiting for Nav2 to activate...")
    navigator.waitUntilNav2Active()
    print("Nav2 active! Starting patrol sequence.")

    # 4 patrol corners around the room
    waypoints = [
        create_pose(navigator, 1.2, 0.0),
        create_pose(navigator, 1.2, 1.2),
        create_pose(navigator, -0.5, 1.2),
        create_pose(navigator, 0.0, 0.0)
    ]

    navigator.followWaypoints(waypoints)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            print(f"Heading to waypoint: {feedback.current_waypoint + 1}/{len(waypoints)}")

    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print("Cleaning mission complete! All waypoints reached.")
    else:
        print(f"Mission finished with status: {result}")

    navigator.lifecycleShutdown()
    rclpy.shutdown()

if __name__ == '__main__':
    main()