import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('my_robot_sim')
    gz_pkg = get_package_share_directory('ros_gz_sim')

    world = os.path.join(pkg, 'worlds', 'worlds.sdf')
    urdf = os.path.join(pkg, 'urdf', 'vacbot.urdf')
    with open(urdf) as f:
        robot_desc = f.read()

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gz_pkg, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items())

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_desc,
                     'use_sim_time': True}])

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'vacbot',
                   '-z', '0.05'])
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p', f'config_file:={os.path.join(pkg, "config", "config.yaml")}',
        ],
        output='screen'
    )
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg, 'rviz', 'vacbot.rviz')],
        parameters=[{'use_sim_time': True}],
        output='screen')
    
    return LaunchDescription([gz_sim, rsp, spawn, bridge, rviz])