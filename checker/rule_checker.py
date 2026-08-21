cases = [
    {"host_ip":"192.168.1.10", "gateway":"192.168.1.1"}
    {"host_ip":"192.168.2.10", "gateway":"192.168.1.1"}
]
for i,case in enumerate(cases):
    host = ".".join(case["host_ip"].split(".")[:3])
    gateway = ".".join(case["gateway"].split(".")[:3])

    if host != gateway:
        print(f"case {i+1}: Gateway mismatch!")
    else:
        print(f"case{i+1}: Gateway OK")
