cases = [
    {
        "case_id": 1,
        "symptom": "PC cannot ping gateway",
        "host_ip": "192.168.1.10",
        "gateway": "192.168.2.1",  
        "interface_status": "down",
        "duplicate_ip": False,
        "vlan_configured": True,
        "route_exists": True
    },
    {
        "case_id": 2,
        "symptom": "PC gets IP but cannot reach server",
        "host_ip": "192.168.1.20",
        "gateway": "192.168.1.1",
        "interface_status": "up",
        "duplicate_ip": False,
        "vlan_configured": False,  
        "route_exists": False      
    },
    {
        "case_id": 3,
        "symptom": "Two PCs cannot communicate",
        "host_ip": "192.168.1.10",
        "gateway": "192.168.1.1",
        "interface_status": "up",
        "duplicate_ip": True,  
        "vlan_configured": True,
        "route_exists": True
    },
]

print("=" * 50)
print(" Network Issue - Network Rule Checker")
print("=" * 50)

for case in cases:
    print(f"\nCase {case['case_id']}: {case['symptom']}")
    print("-" * 40)
    errors_found = False

    # Check 1: Gateway mismatch
    host_network = ".".join(case["host_ip"].split(".")[:3])
    gateway_network = ".".join(case["gateway"].split(".")[:3])
    if host_network != gateway_network:
        print("ERROR: Gateway mismatch - host and gateway on different subnets")
        errors_found = True

    # Check 2: Interface down
    if case["interface_status"] == "down":
        print("ERROR: Interface is down - check shutdown command")
        errors_found = True

    # Check 3: Duplicate IP
    if case["duplicate_ip"]:
        print("ERROR: Duplicate IP address detected")
        errors_found = True

    # Check 4: VLAN not configured
    if not case["vlan_configured"]:
        print("ERROR: VLAN not configured on this port")
        errors_found = True

    # Check 5: Missing route
    if not case["route_exists"]:
        print("ERROR: No route found - missing static or dynamic route")
        errors_found = True

    if not errors_found:
        print("All checks passed!")

print("\n" + "=" * 50)
print("Rule check complete!")
print("=" * 50)
