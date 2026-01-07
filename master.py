import socket, json, threading, math

PORT = 5000
TOKEN = "bro123"
TOTAL_FRAMES = 240

workers = []

def handle_worker(conn):
    auth = json.loads(conn.recv(4096).decode())
    if auth["token"] != TOKEN:
        conn.send(json.dumps({"status": "NO"}).encode())
        conn.close()
        return

    node = auth["node"]
    workers.append((node, conn))
    conn.send(json.dumps({"status": "OK"}).encode())

server = socket.socket()
server.bind(("", PORT))
server.listen()

print("Master listening...")

# Accept workers
while len(workers) < 2:   # change based on nodes you want
    conn, _ = server.accept()
    threading.Thread(target=handle_worker, args=(conn,)).start()

# Frame split
total_nodes = len(workers) + 1  # + master
chunk = math.ceil(TOTAL_FRAMES / total_nodes)

current = 1
for node, conn in workers:
    conn.send(json.dumps({
        "type": "JOB",
        "start": current,
        "end": min(current + chunk - 1, TOTAL_FRAMES)
    }).encode())
    current += chunk

print("Workers dispatched.")
print(f"Master renders frames {current} to {TOTAL_FRAMES}")
