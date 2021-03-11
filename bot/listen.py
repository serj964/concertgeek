import socket

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 8000      # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            data = conn.recv(1024)
            decoded_data = data.decode()
            txt = decoded_data.split()[1]
            token = txt.split(sep='=')[1]
            print(token)
            #token, hash->database
            hash = str(random.getrandbits(128))
            hashlink = "t.me/AlexanderMGOauthBot?start="+hash
            conn.close()