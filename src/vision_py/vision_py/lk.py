import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from visual_trackers.optical_flow import lk

FRONT_CAMERA_TOPIC = "/hang_cam/image_raw"



class MyNode(Node):
    def __init__(self):
        node_name="lk"
        super().__init__(node_name)
        self.get_logger().info("Hello CV and ROS2 lk")
        self.img_sub = self.create_subscription(
            Image,
            FRONT_CAMERA_TOPIC,
            self.image_handler,
            qos_profile=qos_profile_sensor_data)
        self.cv_br = CvBridge()
        self.lk_tracker = lk.LKTracker()
        self.lk_tracker.register_xxx(self.debug_track_request_handler)

    def debug_track_request_handler(self, x, y):
        self.lk_tracker.track(x, y)

    def image_handler(self, msg: Image):
        """_summary_
        https://docs.ros2.org/latest/api/sensor_msgs/msg/Image.html

        
        """
        frame = self.cv_br.imgmsg_to_cv2(msg)
        self.lk_tracker.calc(frame)
        
    
              
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()