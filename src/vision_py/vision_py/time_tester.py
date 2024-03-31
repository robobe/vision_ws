import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data, qos_profile_system_default
from rcl_interfaces.msg import Log
from rclpy.time import Time, Duration

class MyNode(Node):
    def __init__(self):
        super().__init__("my_node")
        self.timer = self.create_timer(1, self.timer_handler)
        self.create_subscription(Log, "/rosout", self.handler, qos_profile_system_default)
        self.last_time = self.get_clock().now()

    def timer_handler(self):
        self.get_logger().info("message from timer")

    def handler(self, msg: Log):
        t = Time.from_msg(msg.stamp)
        d = t-self.last_time
        print(d, type(d), d.nanoseconds/1e9)
        self.last_time=t
        

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()