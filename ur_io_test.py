import rtde_control
import rtde_receive
import rtde_io          # <-- 1. IO 라이브러리 임포트
import time
import logging

# 로봇 컨트롤러 IP
ROBOT_IP = "192.168.1.10"

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

rtde_c = None
rtde_io_ctrl = None     # <-- 2. IO 제어 객체를 위한 변수

try:
    # 1. 모든 인터페이스 연결
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)
    logging.info("Receive interface (rtde_r) connected.")
    
    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    logging.info("Control interface (rtde_c) connected.")
    
    rtde_io_ctrl = rtde_io.RTDEIOInterface(ROBOT_IP) # <-- 3. IO 인터페이스 연결
    logging.info("IO interface (rtde_io_ctrl) connected.")


    # 2. 로봇 이동 (이전과 동일)
    current_pose = rtde_r.getActualTCPPose()
    target_pose = current_pose[:]
    target_pose[2] += 0.01
    logging.info(f"Moving 1cm up (Z+) to: {target_pose}")
    rtde_c.moveL(target_pose, speed=0.1, acceleration=0.1)
    time.sleep(1)
    logging.info("Move complete.")


    # 3. I/O 읽기 (이전과 동일)
    digital_inputs = rtde_r.getActualDigitalInputBits()
    logging.info(f"Digital Input (Integer): {digital_inputs}")


    # 4. --- I/O 쓰기 (rtde_io_ctrl 사용) ---
    logging.info("--- Setting Digital Output (Test) ---")
    output_pin = 0  # 0번 핀을 테스트합니다.
    
    # 0번 핀 켜기 (True)
    logging.info(f"Turning ON DO[{output_pin}]...")
    rtde_io_ctrl.setStandardDigitalOut(output_pin, True)
    
    time.sleep(4)# 1초간 켜진 상태 유지

    # 0번 핀 끄기 (False)
    logging.info(f"Turning OFF DO[{output_pin}]...")
    rtde_io_ctrl.setStandardDigitalOut(output_pin, False)
    
    logging.info("IO Write test complete.")
    # --- I/O 쓰기 종료 ---


except RuntimeError as e:
    logging.error(f"RUNTIME ERROR: {e}")
    if "RTDE input registers are already in use" in str(e):
        logging.error("--> RTDE 리소스 충돌입니다. URCap 제거 및 컨트롤러 재부팅이 필요합니다.")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
finally:
    # 5. 스크립트 종료
    # (rtde_io_ctrl는 stopScript()가 필요 없습니다)
    if rtde_c and rtde_c.isConnected():
        rtde_c.stopScript()
        logging.info("Control script stopped.")