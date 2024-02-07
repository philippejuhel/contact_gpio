# Copyright 2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from std_msgs.msg import Bool

PIN_CONTACT = 17 # BCM position on the Raspberry Pi board

class ContactPublisher(Node):

    def __init__(self):
        super().__init__('contact_publisher')
        self.publisher_ = self.create_publisher(Bool, 'contact', 10)
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
    # Configure the Raspberry board to be able to read the contact value on PIN_CONTACT
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN_CONTACT, GPIO.IN)

    def timer_callback(self):
        msg = Bool()
        msg.data = GPIO.input(PIN_CONTACT) == 1
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%r"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    publisher = ContactPublisher()

    rclpy.spin(publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
