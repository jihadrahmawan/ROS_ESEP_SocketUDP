#!/usr/bin/env python

'''
jr-ros drone python ROS 
Reading ESP8266 over wifi Data and publish the topic
code rev 4
github : jihadrahmawan
last_update = 1/1/2023
'''
##
import socket
import struct
import contextlib 
import rospy
from std_msgs.msg import Int32MultiArray


if __name__=="__main__":
    rospy.init_node('ESP8266')
    
    pub = rospy.Publisher("espData", Int32MultiArray, queue_size=10)
    UDP_IP=""
    UDP_PORT=9000

    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((UDP_IP,UDP_PORT))
    sock.setblocking(0)
    data = ''
    addr = ''
    r = rospy.Rate(5)
    pritlogConecting = True
    pritlogConected = True
    #rospy.logwarn('Waiting Connection from ESP8266...')
    array=[]
    with contextlib.closing(sock):
        while not rospy.is_shutdown():
            try:
	            data,addr = sock.recvfrom(1024)
            except socket.error as e:
                if pritlogConecting:
                    rospy.logerr('Sarung tangan is Offline !, Try to Connect to ESP')
                    pritlogConected = True
                    pritlogConecting = False
                array=[]
                pass
            else:
                array=[]
                for p in range(len(data)):
                    array.append(int (data[p:p+1]))
                if pritlogConected:  
                    rospy.loginfo('Connected to ESP')
                    rospy.loginfo('Received data = {}'.format(array))
                    pritlogConecting = True
                    pritlogConected = False
      		
            array_forPublish = Int32MultiArray(data=array)
            pub.publish(array_forPublish)
            #rospy.loginfo('ESPData = {}'.format(array))
            r.sleep()



