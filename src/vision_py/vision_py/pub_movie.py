import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

FRONT_CAMERA_TOPIC = "/hang_cam/image_raw"

class MyNode(Node):
    def __init__(self):
        node_name="image_pub"
        super().__init__(node_name)
        self.get_logger().info("pub movie tester")
        self.img_pub = self.create_publisher(Image,
                                             FRONT_CAMERA_TOPIC,
                                             qos_profile=qos_profile_sensor_data)
        self.cv_br = CvBridge()
        self.cap = cv2.VideoCapture("/home/user/workspaces/vision_ws/src/vision_py/scripts/slow_traffic_small.mp4")

        self.create_timer(1/9, self.play_frame)

    def play_frame(self):
        ret, frame = self.cap.read()
        msg = self.cv_br.cv2_to_imgmsg(frame)
        self.img_pub.publish(msg)
        self.get_logger().info("send --")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()