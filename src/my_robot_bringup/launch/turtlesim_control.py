from launch import LaunchDescription
from launch_ros.actions import Node
import rclpy


def generate_launch_description():
    ld= LaunchDescription()

    rclpy.init_node('infinite_loop_node')

    turtlesim_keybord_= input("gir:")

    while not rclpy.is_shutdown():
        turtlesim_keybord_= input("gir:")
        turtlesim_keybord_.append(Node(
            package="my_py_pkg",
            executable="turtlesim_keybord",
            parameters=[{"turtlesim_keybord": turtlesim_keybord_}] 


        ))


    for node in turtlesim_keybord_:
        ld.add_action(node)
    return ld