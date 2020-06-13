import enum
import socket
import time
import threading
from .bytecodes import *

class ProtocolType(enum.Enum):
    LD686 = 1,
    LD382A = 2,
    LD382 = 3

def send_data(data_bytes: bytes, protocol_type: ProtocolType, sock: socket.socket, timeout = 0.1):
    if protocol_type == ProtocolType.LD382A or protocol_type == ProtocolType.LD686:
        data_bytes = bytes([*data_bytes, 0x0F])

    checksum = checksum_for(data_bytes)

    total_bytes = bytes([*data_bytes, checksum])

    print(f"Send: '{data_bytes.hex()}' CS:{hex(checksum)}")
    sock.sendall(total_bytes)

    if timeout > 0:
        sock.settimeout(timeout)
        response = []
        while True:
            try:
                r = sock.recv(1)
                response.append(r[0])
            except socket.timeout:
                break
        response = bytes(response)
        response_data = response[:-1]
        expected_checksum = checksum_for(response_data)
        actual_checksum = response[-1]
        print(f" -> Receive: '{response_data.hex()}' CS:{hex(actual_checksum)}")
        if actual_checksum != expected_checksum:
            raise RuntimeWarning(f"Received invalid checksum: {actual_checksum}!={expected_checksum}")
        return response_data
    return None


def checksum_for(data_bytes: bytes):
    checksum = 0
    for byte in data_bytes:
        checksum += byte
    checksum = checksum & 0xFF
    return checksum


def scan(seconds: int) -> dict:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", 48899))
    sock.settimeout(1)

    results = {}

    stop_receiver = threading.Event()
    receiver = threading.Thread(target=receive, args=(sock, stop_receiver, results))
    receiver.start()

    for i in range(seconds):
        sock.sendto(b"HF-A11ASSISTHREAD", ("255.255.255.255", 48899))
        time.sleep(1)
    stop_receiver.set()
    receiver.join()

    return results


def receive(sock: socket.socket, stop: threading.Event, results: dict):
    while not stop.is_set():
        try:
            data, (ip, port) = sock.recvfrom(200)
            if data == b"HF-A11ASSISTHREAD":
                continue
            if ip not in results:
                results[ip] = data
        except socket.timeout:
            continue