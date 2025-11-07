import rtde_control
import rtde_receive
import time
import logging

# 로봇 컨트롤러 IP
ROBOT_IP = "192.168.1.10"

# 로깅 설정 (에러 확인을 위해 INFO 레벨로 설정)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

rtde_c = None # rtde_c 변수를 try 블록 밖에서 선언

try:
    # 1. 수신 및 제어 인터페이스 모두 연결
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    logging.info("Receive interface (rtde_r) connected.")

    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    logging.info("Control interface (rtde_c) connected.")

    # 2. 현재 TCP 위치 가져오기 (Base 기준 [X, Y, Z, Rx, Ry, Rz])
    current_pose = rtde_r.getActualTCPPose()
    logging.info(f"Current pose (X,Y,Z,Rx,Ry,Rz): {current_pose}")

    # 3. 목표 위치 계산 (현재 위치에서 Z축 + 1cm)
    target_pose = current_pose[:]  # 현재 위치 리스트를 복사
    
    # Z값(인덱스 2번)에 0.01 미터(1cm)를 더함
    target_pose[2] += 0.01  

    logging.info(f"Moving 1cm up (Z+) to: {target_pose}")

    # 4. ⚠️ 로봇이 움직입니다! ⚠️
    # MoveL로 이동 (안전을 위해 속도/가속도 낮게 설정)
    speed = 0.1  # 0.1 m/s
    acceleration = 0.1 # 0.1 m/s^2
    rtde_c.moveL(target_pose, speed, acceleration)
    
    time.sleep(1) # 이동 완료 대기 (실제로는 isSteady() 등을 확인해야 함)
    logging.info("Move complete.")

except RuntimeError as e:
    # (!!!) 예상되는 에러
    logging.error(f"RUNTIME ERROR: {e}")
    if "RTDE input registers are already in use" in str(e):
        logging.error("--> 역시 RTDE 리소스 충돌입니다. URCap 제거 및 컨트롤러 재부팅이 필요합니다.")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    # 5. 스크립트 종료 (연결이 성공했을 경우에만)
    if rtde_c and rtde_c.isConnected():
        rtde_c.stopScript()
        logging.info("Control script stopped.")