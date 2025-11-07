import ur_control_script
import rtde_receive
import time

ROBOT_IP = "192.168.0.10"

rtde_c = ur_control_script.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

print("Connected:", rtde_r.isConnected())
print("Program running:", rtde_r.isProgramRunning())
print("Current TCP Pose:", rtde_r.getActualTCPPose())
print("joint_pos : " ,rtde_r.getActualQ())

# Z축 3cm 이동
pose = rtde_r.getActualTCPPose()
pose[2] += 0.03
rtde_c.moveL(pose, 0.25, 0.2)

time.sleep(1)
rtde_c.stopScript()
rtde_c.disconnect()
rtde_r.disconnect()
