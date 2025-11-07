import socket
import time
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --- 로봇 IP 및 대시보드 포트 ---
ROBOT_IP = "192.168.1.10"
DASHBOARD_PORT = 30003
BUFFER_SIZE = 1024

def power_on_robot(robot_ip):
    logging.info(f"Connecting to Dashboard Server at {robot_ip}:{DASHBOARD_PORT}...")
    
    # 1. 소켓 생성 (TCP/IP)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(2.0)

    try:
        # 2. 로봇에 연결
        client_socket.connect((robot_ip, DASHBOARD_PORT))
        
        # 3. (중요) 연결 직후, 환영 메시지를 먼저 받음.
        welcome_msg = client_socket.recv(BUFFER_SIZE).decode('latin-1')
        logging.info(f"[ROBOT SAYS]: {welcome_msg.strip()}")

        # 4. 'power on' 명령 보내기
        command_on = "power on\n"
        logging.info(f"[PYTHON SENDS]: {command_on.strip()}")
        client_socket.sendall(command_on.encode('utf-8'))
        
        # 응답 받기
        response_on = client_socket.recv(BUFFER_SIZE).decode('latin-1')
        logging.info(f"[ROBOT SAYS]: {response_on.strip()}")

        time.sleep(2) # 로봇이 전원을 켤 시간을 줌

        # 5. 'brake release' 명령 보내기 (필수)
        command_brake = "brake release\n"
        logging.info(f"[PYTHON SENDS]: {command_brake.strip()}")
        client_socket.sendall(command_brake.encode('utf-8'))

        # 응답 받기
        response_brake = client_socket.recv(BUFFER_SIZE).decode('latin-1')
        logging.info(f"[ROBOT SAYS]: {response_brake.strip()}")
        
        if "Brake releasing" in response_brake:
            logging.info("SUCCESS: Robot power on and brakes released.")
        else:
            logging.warning("Check robot state. Brakes may not have released.")

    except socket.timeout:
        logging.error("Connection timed out. Check IP and port.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # 6. 소켓 닫기
        client_socket.close()
        logging.info("Connection closed.")

# --- 메인 실행 ---
if __name__ == "__main__":
    # ⚠️ 로봇 IP 주소를 실제 환경에 맞게 수정하세요.
    power_on_robot(ROBOT_IP)