#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from functools import partial
from example_interfaces.srv import AddTwoInts

class AddTwoIntsClientNode(Node):
    def __init__(self):
        super().__init__("add_two_ints_client")
        self.call_add_two_ints_server(5,6)
        self.call_add_two_ints_server(5,5)
        self.call_add_two_ints_server(5,1)


    def call_add_two_ints_server(self,a,b):
        client=self.create_client(AddTwoInts,"add_two_ints")
        while not client.wait_for_service(1.0):
            self.get_logger().warn("waiting the service...")

        request=AddTwoInts.Request() #parametre olarak aldıklarımızla istek oluşturuyoruz
        request.a=a
        request.b=b

        future=client.call_async(request)   #Servisi çağırıyoruz ve future adlı bir nesne alıyoruz.
        future.add_done_callback(partial(self.callback_call_add_two_ints,a=a,b=b)) #gelecekteki nesne için bir geri arama ekleme

    def callback_call_add_two_ints(self,future,a,b):
        try:
            response=future.result()
            self.get_logger().info(str(response.sum))

        except Exception as e:
            self.get_logger().error("service call error!")

def main(args=None):
        rclpy.init(args=args)
        node=AddTwoIntsClientNode()
        rclpy.spin(node)
        rclpy.shutdown()

if __name__=="__main__":
        main()