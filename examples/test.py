from pyufoled.protocol import checksum_for
import socket

def send_data(*data_bytes, timeout = 0.1, cs=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.170.101", 5577))

    data_bytes = bytes(data_bytes)
    if cs:
        checksum = checksum_for(data_bytes)

        total_bytes = bytes([*data_bytes, checksum])
    else:
        total_bytes = data_bytes
        checksum = 0

    print(f"Send: '{data_bytes.hex()}' CS:{hex(checksum)}")
    sock.sendall(total_bytes)

    if timeout > 0:
        sock.settimeout(timeout)
        response = sock.recv(64)
        #response = []
        #while True:
        #    try:
        #        r = sock.recv()
        #        response.append(r[0])
        #    except socket.timeout:
        #        break
        response = bytes(response)
        response_data = response[:-1]
        expected_checksum = checksum_for(response_data)
        actual_checksum = response[-1]
        print(f" -> Receive: '{response_data.hex()}' CS:{hex(actual_checksum)}")
        if actual_checksum != expected_checksum:
            raise RuntimeWarning(f"Received invalid checksum: {actual_checksum}!={expected_checksum}")
        return response_data.hex()
    return None

    sock.close()


a = 0x00

def toggled():
    global a
    a = 0xFF - a
    return a