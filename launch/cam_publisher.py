import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import serial

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'camera/image_raw', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Publish at 10 Hz
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)  # Open the default camera


    def timer_callback(self):
        ret, frame = self.cap.read() # Captures Frame
        if ret:
            image_message = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            self.publisher_.publish(image_message)
            self.get_logger().info('Publishing an image')
    
    def destroy_node(self):
        self.cap.release()
        super().destroy_node()
    
    def main(args=None):
        rclpy.init(args=args)
        camera_publisher = CameraPublisher()
        try:
            rclpy.spin(camera_publisher)
        except KeyboardInterrupt:
            pass
        camera_publisher.destroy_node()
        rclpy.shutdown()

    if __name__ == '__main__':
        main()




