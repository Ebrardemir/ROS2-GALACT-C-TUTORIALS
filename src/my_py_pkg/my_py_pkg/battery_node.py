#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial

from my_robot_interfaces.srv import LedStateServer

class BatteryNode(Node):
    def __init__(self):
        super().__init__("battery_node")
        self.battery_state_= "full"
        self.last_time_battery_state_changed_=self.get_current_time_seconds()
        self.battery_timer_= self.create_timer(0.1,self.check_battery_state)
        self.get_logger().info("battery node has been started")

    def get_current_time_seconds(self):
        secs ,nsecs =self.get_clock().now().seconds_nanoseconds()
        return secs +nsecs /1000000000.0
    
    def check_battery_state(self):
        time_now=self.get_current_time_seconds()
        if self.battery_state_=="full":
            if time_now - self.last_time_battery_state_changed_ >4.0:
                self.battery_state_="empty"
                self.get_logger().info("battery is empty!!")
                self.last_time_battery_state_changed_ =time_now
                self.battery_node_client(3,1)

        else:
             if time_now - self.last_time_battery_state_changed_ >6.0:
                self.battery_state_="full"
                self.get_logger().info("battery is now full")
                self.last_time_battery_state_changed_ =time_now
                self.battery_node_client(3,0)


    def battery_node_client(self,led_number,state):
        client_=self.create_client(LedStateServer,"set_led")
        while not client_.wait_for_service(1.0):
            self.get_logger().warn("waiting the service...")

        request=LedStateServer.Request()
        request.led_number=led_number
        request.state=state

        future=client_.call_async(request)
        future.add_done_callback(partial(self.callback_call_led_panel_state,led_number=led_number,state=state))

    def callback_call_led_panel_state(self,future,led_number,state):
        try:
            response=future.result()
            self.get_logger().info(str(response.success))

        except Exception as e:
            self.get_logger().error("service call error!")


def main(args=None):
        rclpy.init(args=args)
        node=BatteryNode()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__=="__main__":
        main()