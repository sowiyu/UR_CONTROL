# main_test.py

# 1. 클래스 및 필요 라이브러리 임포트
from ur_control_script import URControl
import time
import logging
import numpy as np

# 2. 로깅 설정 (메인 스크립트에서 수행)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

####################################################################
# 테스트 함수들 (이전에 제안한 것과 동일)
####################################################################

def test_connection_and_info(robot):
    """ 1. 로봇 연결, 기본 정보 (TCP/관절) 확인, 연결 해제 """
    print("--- 테스트 1: 연결 및 정보 확인 ---")
    try:
        robot.connect()
        tcp_pos = robot.get_tcp_pos()
        print(f"현재 TCP 위치 (Base 기준): {tcp_pos}")
        
        joint_pos = robot.get_joint_pos()
        print(f"현재 관절 위치 (radians): {joint_pos}")
        
    except Exception as e:
        logging.error(f"테스트 1 실패: {e}")
    finally:
        robot.stop_robot_control() # 스크립트 정지
        print("----------------------------------\n")


def test_move_l(robot):
    """ 2. MoveL (선형 이동) 테스트 """
    print("--- 테스트 2: MoveL (선형 이동) ---")
    # ⚠️ 경고: 로봇이 도달할 수 있는 안전한 좌표로 수정하세요!
    # [x, y, z, rx, ry, rz] (m, rad)
    target_pose_l = [0.0, -0.3, 0.2, 3.14, 0, 0] # 예시 좌표입니다. 반드시 수정하세요.
    
    try:
        initial_pos = robot.get_tcp_pos()
        print(f"이동 전 위치: {initial_pos}")
        
        print(f"{target_pose_l} 위치로 선형 이동합니다...")
        robot.move_l(target_pose_l, speed=0.1, acceleration=0.1)
        
        time.sleep(2) 
        
        final_pos = robot.get_tcp_pos()
        print(f"이동 후 위치: {final_pos}")
        
    except Exception as e:
        logging.error(f"테스트 2 실패: {e}")
    finally:
        robot.stop_robot_control()
        print("----------------------------------\n")


def test_move_j(robot):
    """ 3. MoveJ (관절 이동) 테스트 """
    print("--- 테스트 3: MoveJ (관절 이동) ---")
    # ⚠️ 경고: 안전한 관절 각도(radian)로 수정하세요!
    target_joints = [0, -np.pi/2, -np.pi/2, -np.pi/2, np.pi/2, 0] # 예: 위를 보는 자세
    
    try:
        initial_joints = robot.get_joint_pos()
        print(f"이동 전 관절 위치: {initial_joints}")
        
        print(f"{target_joints} 위치로 관절 이동합니다...")
        robot.move_j(target_joints, speed=0.2, acceleration=0.2)
        
        time.sleep(2)
        
        final_joints = robot.get_joint_pos()
        print(f"이동 후 관절 위치: {final_joints}")
        
    except Exception as e:
        logging.error(f"테스트 3 실패: {e}")
    finally:
        robot.stop_robot_control()
        print("----------------------------------\n")

# ... (다른 test_... 함수들도 여기에 추가: test_relative_move_l, test_digital_io 등) ...
def test_relative_move_l(robot):
    """ 4. MoveL Add (상대 이동) 테스트 """
    print("--- 테스트 4: 상대 이동 (MoveL Add) ---")
    relative_move = [0, 0, 0.05, 0, 0, 0] 
    
    try:
        initial_pos = robot.get_tcp_pos()
        print(f"초기 TCP 위치: {initial_pos}")
        
        print(f"현재 위치에서 [0, 0, 0.05, 0, 0, 0] 만큼 상대 이동 (Base 기준)...")
        robot.move_add_l(relative_move, speed=0.05, acceleration=0.05)
        
        time.sleep(1)
        
        final_pos = robot.get_tcp_pos()
        print(f"이동 후 TCP 위치: {final_pos}")
        
    except Exception as e:
        logging.error(f"테스트 4 실패: {e}")
    finally:
        robot.stop_robot_control()
        print("----------------------------------\n")


def test_digital_io(robot):
    """ 5. 디지털 출력 (Pulse) 테스트 """
    print("--- 테스트 5: 디지털 출력 (Pulse) ---")
    output_id = 0 
    duration = 1.0 
    
    try:
        print(f"디지털 출력 {output_id}번 핀을 {duration}초 동안 켭니다 (Pulse)...")
        robot.pulse_digital_output(output_id, duration)
        print("펄스 완료.")
        
    except Exception as e:
        logging.error(f"테스트 5 실패: {e}")
    finally:
        robot.stop_robot_control()
        print("----------------------------------\n")


def get_joint(robot):
    try:
        robot.getActualQ()
    except Exception as e:
        logging.error(f"테스트 5 실패: {e}")
    finally:
        robot.stop_robot_control()
        print("----------------------------------\n")

####################################################################
# 메인 실행 블록
####################################################################

if __name__ == '__main__':
    # ⚠️ 로봇 IP 주소를 실제 환경에 맞게 수정하세요.
    ROBOT_IP = '192.168.1.10' 

    print(f"로봇 {ROBOT_IP}에 연결을 시도합니다.")
    print("="*40)
    print("⚠️ 경고: 테스트 코드가 실행됩니다. 로봇이 움직일 수 있습니다!")
    print("⚠️ 5초 후에 테스트를 시작합니다. 비상 정지 버튼을 준비하세요...")
    print("="*40)
    
    try:
        time.sleep(5) # 사용자가 경고를 인지할 시간
    except KeyboardInterrupt:
        print("테스트 취소됨.")
        exit()

    # 3. URControl 객체 생성 (ur_control_script 파일에서 가져온 클래스)
    my_robot = URControl(ROBOT_IP)

    # 4. 테스트 실행
    # (안전을 위해 한 번에 하나씩 주석을 해제하며 테스트하는 것을 권장합니다)
    try:
        test_connection_and_info(my_robot)
        time.sleep(1)
        
        # test_move_j(my_robot) # 안전한 자세로 먼저 이동
        # time.sleep(1)

        # test_move_l(my_robot)
        # time.sleep(1)
        test_relative_move_l(my_robot)
        time.sleep(1)
        
        # test_digital_io(my_robot)
        # time.sleep(1)
        
        print("\n모든 테스트 완료.")

    except Exception as e:
        logging.error(f"메인 테스트 중 에러 발생: {e}")
    except KeyboardInterrupt:
        logging.info("사용자에 의해 프로그램이 중단되었습니다.")
        # 프로그램 중단 시에도 로봇 연결을 멈추도록 시도
        try:
            my_robot.stop_robot_control()
        except Exception as e:
            logging.error(f"중단 시 로봇 정지 실패: {e}")