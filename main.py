import requests, sys, json, time

if len(sys.argv) < 2:
    print(f"[ x ] Error, Invalid arguments provided...\nUsage: {sys.argv[0]} <host> <nodes>")
    exit(0)

HOST = sys.argv[1]
NODES = 3

if len(sys.argv) > 2:
    NODES = int(sys.argv[2])

req = requests.get(f"https://check-host.net/check-ping?host={HOST}&max_nodes={NODES}", headers={"Accept": "application/json"})
if req.status_code != 200:
    print(f"[ x ] Error, Unable to connect to check-host...!")
    exit(0)

if not req.text.startswith("{") and not req.text.endswith("}"):
    print(f"[ x ] Error, Unexpected response from check-host...!")
    exit(0)

jsn = json.loads(req.text)
link = jsn["permanent_link"]
print(f"Permanent Link: {link}")

time.sleep(2 * NODES)
new_req = requests.get(link, headers={"Accept": "application/json"})
if new_req.status_code != 200:
    print(f"[ x ] Error, Unable to connect to check-host...!")
    exit(0)

resp = new_req.text
if "check_displayer.display" not in resp:
    print(f"[ x ] Error, Unexpected response from check-host...!")
    exit(0)

ping_info = {}
lines = resp.split('\n')
for line in lines:
    if "check_displayer.display" in line:
        info = line.replace("check_displayer.display(\"", "").replace(");", "").replace("'", "").replace("\"", "").replace("OK,", "OK: ").replace("[", "").replace("]", "").strip().split(",")
        ping_info[info[0]] = info[1:]

print("Server | rtt min | avg | max")
for server in ping_info:
    print(f"{server}: {ping_info[server]}")
