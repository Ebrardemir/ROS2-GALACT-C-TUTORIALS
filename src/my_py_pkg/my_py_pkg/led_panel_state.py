#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

from my_robot_interfaces.msg import LedStateArray
from my_robot_interfaces.srv import LedStateServer

class LedPanelState(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.led_count_=[0,0,0]
        self.led_states_publisher_= self.create_publisher(LedStateArray,"led_states",10)
        self.led_state_timer_= self.create_timer(4,self.publish_led_states)
        self.server_=self.create_service(LedStateServer,"set_led",self.callback_led_server)

        self.get_logger().info("publisher has been starting")

    def publish_led_states(self):
        msg=LedStateArray()
        msg.led_state=self.led_count_
        self.led_states_publisher_.publish(msg)

    def callback_led_server(self, request, response):
        led_number=request.led_number
        state=request.state

        if led_number >len(self.led_count_) or led_number<=0:
            response.success =False
            return response
        
        if state not in(0,1):
            response.success=False
            return response
        
        self.led_count_[led_number-1] =state
        response.success=True       
        self.publish_led_states()
        return response


def main(args=None):
        rclpy.init(args=args)
        node=LedPanelState()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__=="__main__":
        main()