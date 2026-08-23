# Network Issue - Diagnosis Prompt Template

## How to Use This Prompt
Copy the template below, fill in the details from your network case,
and send it to an AI assistant. The AI will return a JSON diagnosis.

---

## Main Prompt Template

You are a network troubleshooting assistant for Cisco lab networks.
Given the following network problem, respond ONLY in JSON format.

Symptom: [describe what is not working]
Topology: [describe the network setup]
Show command output: [paste the output here]

Respond ONLY with this JSON, nothing else:
{
  "root_cause": "what is causing the problem",
  "osi_layer": "which OSI layer is affected (e.g. Layer 2, Layer 3)",
  "confidence": "low / medium / high",
  "evidence": "what in the show output proves this",
  "next_command": "the next command to run to confirm",
  "fix_steps": [
    "Step 1: do this",
    "Step 2: do this",
    "Step 3: verify with this command"
  ]
}

---

## Worked Example 1

Symptom: PC gets IP address but cannot reach server in VLAN 30. Gateway ping works.
Topology: One router, two switches, three VLANs (10, 20, 30)
Show command output:
  show ip route - no entry for 192.168.30.0
  show interfaces trunk - VLAN 30 not in allowed list

Expected JSON response:
{
  "root_cause": "VLAN 30 is missing from the trunk link and no route exists for it",
  "osi_layer": "Layer 2 and Layer 3",
  "confidence": "high",
  "evidence": "show ip route shows no entry for 192.168.30.0 and trunk does not allow VLAN 30",
  "next_command": "show interfaces trunk",
  "fix_steps": [
    "Step 1: switchport trunk allowed vlan add 30",
    "Step 2: Add ip route for 192.168.30.0 on router",
    "Step 3: Ping from PC to server to verify"
  ]
}

---

## Worked Example 2

Symptom: Guest WiFi can reach internal server
Topology: Wireless router, guest VLAN 50, internal VLAN 10
Show command output:
  show vlan brief - VLAN 50 not isolated
  show access-lists - no ACL applied to guest VLAN

Expected JSON response:
{
  "root_cause": "Guest VLAN isolation not configured and no ACL blocking guest to internal traffic",
  "osi_layer": "Layer 2 and Layer 4",
  "confidence": "high",
  "evidence": "show access-lists shows no rules applied between VLAN 50 and VLAN 10",
  "next_command": "show access-lists",
  "fix_steps": [
    "Step 1: Create ACL to block VLAN 50 from reaching VLAN 10",
    "Step 2: Apply ACL to guest VLAN interface",
    "Step 3: Test that guest cannot reach internal server"
  ]
}

---

## Worked Example 3

Symptom: PC cannot get IP address automatically
Topology: One DHCP server, one switch, three PCs
Show command output:
  show running-config - default-router is 192.168.2.1 but subnet is 192.168.1.0
  show ip dhcp pool - wrong default router configured

Expected JSON response:
{
  "root_cause": "DHCP pool has wrong default gateway configured",
  "osi_layer": "Layer 3",
  "confidence": "high",
  "evidence": "show running-config shows default-router 192.168.2.1 which is not in the 192.168.1.0 subnet",
  "next_command": "show ip dhcp pool",
  "fix_steps": [
    "Step 1: ip dhcp pool POOL_NAME",
    "Step 2: default-router 192.168.1.1",
    "Step 3: Release and renew IP on PC - ipconfig /release then ipconfig /renew"
  ]
}
