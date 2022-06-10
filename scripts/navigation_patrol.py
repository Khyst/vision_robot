#!/usr/bin/env python
# encoding: utf-8

import os
import rospy
import actionlib
import tf
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist

destination = {
    "남자화장실":0, "404호":1, "여자화장실":2, "402호":3, "엘리베이터":4, "401호":5, "405호":6, "반환점":7,
}

waypoints = [
    (-3.605, 22.011, 0), # 남자 화장실
    (-1.875, 12.125, 0), # 404호
    (-3.375, 17.000, 0), # 여자 화장실
    (-1.875, 18.625, 0), # 402호
    (-5.625, 29.125, 0),# 엘리베이터
    (-1.875, 33.875, 0), # 401호
    (0.375, 5.375, 0), # 405호 
    (0, 0, 0), # 반환점
]

def adjustTwist(): #이동거리, 속도지정 가능 (방향은, 각 좌표축 마다 +, -)로 지정
    velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    vel_msg = Twist()

    vel_msg.linear.x = 0 # x축 선속도 지정 가능
    vel_msg.linear.y = 0 # y축 선속도 지정 가능
    vel_msg.linear.z = 0 
    vel_msg.angular.x = 0 # x축 각속도 지정 가능
    vel_msg.angular.y = 0 # y축 각속도 지정 가능
    vel_msg.angular.z = 0 

    distance = 0 # 움직일 거리 지정 가능
    speed = 0 # 속력 지정 가능

    # 출발 시간 (t0)
    t0 = rospy.Time.now().to_sec()
    current_distance = 0

    # 특정한 거리만큼 로봇을 이동
    while(current_distance < distance):
			# 현재 속도 발행
	    velocity_publisher.publish(vel_msg)

	    # 현재 시간 (t1)
	    t1=rospy.Time.now().to_sec()

	    #Calculates distancePoseStamped
	    current_distance= speed*(t1-t0)

	    #목적지에 도달하면, 로봇을 멈추도록 속도를 조정
	    vel_msg.linear.x = 0
	    vel_msg.linear.y = 0
	    vel_msg.linear.z = 0
	    vel_msg.angular.x = 0
	    vel_msg.angular.y = 0
	    vel_msg.angular.z = 0

	    #속도를 조정하는 메시지 발행
	    velocity_publisher.publish(vel_msg)

def init_pose():
    #rospy.init_node('pub_initpose_node', anonymous=True)
    pose_pub = rospy.Publisher('/amcl_pose', PoseWithCovarianceStamped, queue_size=10)
    initialpose_msg = PoseWithCovarianceStamped()
    initialpose_msg.header.frame_id = "map"
    initialpose_msg.pose.pose.position.x = 2.27
    initialpose_msg.pose.pose.position.y = 2.05
    initialpose_msg.pose.pose.orientation.w = 0
    print("init_pose" +"publishing")
    pose_pub.publish(initialpose_msg)

class Patrol:

    def __init__(self):
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

    def set_goal_to_point(self, point):

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = point[0]
        goal.target_pose.pose.position.y = point[1]
        quaternion = tf.transformations.quaternion_from_euler(0.0, 0.0, point[2])
        goal.target_pose.pose.orientation.x = quaternion[0]
        goal.target_pose.pose.orientation.y = quaternion[1]
        goal.target_pose.pose.orientation.z = quaternion[2]
        goal.target_pose.pose.orientation.w = quaternion[3]

        self.client.send_goal(goal)
        wait = self.client.wait_for_result()
        if not wait:
            rospy.logerr("Action server not available!")
            rospy.signal_shutdown("Action server not available!")
        else:
            return self.client.get_result()


if __name__ == '__main__':

    while True:

        os.system('python3 /home/cilab/ros_ws/src/cilab_nav/user_interface/get_destination.py')

        f = open("/home/cilab/ros_ws/src/cilab_nav/user_interface/output.txt", "r")
        
        dest = f.readline()
        print(dest)

        rospy.init_node('patrolling')
        init_pose()

        num = int(input("input the number: "))

        try:
            p = Patrol()
            p.set_goal_to_point(waypoints[destination[dest]])
        except rospy.ROSInterruptException:
            rospy.logerr("Something went wrong when sending the waypoints")