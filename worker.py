import socket, json, subprocess, os, zipfile

MASTER_IP = "192.168.1.10"   # change
PORT = 5000
TOKEN = "bro123"
NODE_NAME = "node1"

sock = socket.socket()
sock.connect((MASTER_IP, PORT))

# Authenticate
sock.send(json.dumps({
    "type": "AUTH",
    "token": TOKEN,
    "node": NODE_NAME
}).encode())

data = json.loads(sock.recv(4096).decode())

if data["status"] != "OK":
    print("Auth failed")
    exit()

# Wait for job
job = json.loads(sock.recv(4096).decode())
start, end = job["start"], job["end"]

os.makedirs(f"output/{NODE_NAME}", exist_ok=True)

# Render
cmd = [
    "blender", "-b", "scene.blend",
    "-s", str(start),
    "-e", str(end),
    "-a",
    "--",
]
subprocess.run(cmd)

# Zip results
zip_name = f"{NODE_NAME}.zip"
with zipfile.ZipFile(zip_name, "w") as z:
    for f in os.listdir(f"output/{NODE_NAME}"):
        z.write(f"output/{NODE_NAME}/{f}")

# Send ZIP
with open(zip_name, "rb") as f:
    sock.sendall(f.read())

sock.send(json.dumps({"type": "DONE", "node": NODE_NAME}).encode())
sock.close()
