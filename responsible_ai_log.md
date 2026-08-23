AI LOG - Network-issue

This log documents cases where the AI diagnosis (produced using
`diagnose_prompt.md`) required human correction after review against
the deterministic rule checker and the case's known ground truth.
Verdict key: **Accepted** = AI matched ground truth · **Edited** = AI
was partly right but needed correction · **Rejected** = AI's root
cause was wrong.

---

## Case 1
**Symptom:** PC cannot ping gateway
**Show/config evidence:** host 192.168.1.10, gateway 192.168.2.1, interface_status = down

**AI Diagnosis:**
- root_cause: "Gateway is on a different subnet than the host, causing unreachability"
- osi_layer: "Layer 3"
- confidence: "high"
- next_command: "show ip interface brief"

**Ground Truth (rule checker):** Two separate faults — (1) gateway/host subnet
mismatch, **and** (2) the interface is administratively down.

**Human Reviewer Verdict:** Edited

**Why AI Was Wrong:** The AI locked onto the subnet mismatch (Layer 3) because
it was the more "interesting" evidence, but never checked interface status —
a Layer 1/2 fault. Since the interface is down, the PC couldn't even reach the
gateway or its own subnet correctly, regardless of the IP mismatch. The AI
should have flagged interface_status first, as it's the lower-layer, more
fundamental fault (OSI troubleshooting normally works bottom-up).

**Correction Applied:** Reviewer added "Interface down (check shutdown /
no shutdown)" as the primary root cause, with the subnet mismatch as a
secondary contributing issue. osi_layer corrected to "Layer 1/2 and Layer 3".

---

## Case 2
**Symptom:** PC gets IP but cannot reach server
**Show/config evidence:** vlan_configured = False, route_exists = False

**AI Diagnosis:**
- root_cause: "Missing route to the destination server subnet"
- osi_layer: "Layer 3"
- confidence: "medium"
- next_command: "show ip route"

**Ground Truth (rule checker):** VLAN not configured on the port **and**
no route exists — two independent errors.

**Human Reviewer Verdict:** Edited

**Why AI Was Wrong:** The AI only surfaced the routing issue and missed
that the port's VLAN isn't even configured — a Layer 2 problem that would
prevent traffic from reaching the router in the first place. This mirrors
the project's own example case (VLAN 30 missing from trunk + no route),
which explicitly requires checking both layers.

**Correction Applied:** Reviewer added "VLAN not configured on access port"
as a co-primary cause, updated next_command to `show vlan brief` before
`show ip route`, and changed osi_layer to "Layer 2 and Layer 3".

---

## Case 3
**Symptom:** Two PCs cannot communicate
**Show/config evidence:** duplicate_ip = True

**AI Diagnosis:**
- root_cause: "ACL blocking traffic between the two hosts"
- osi_layer: "Layer 4"
- confidence: "low"
- next_command: "show access-lists"

**Ground Truth (rule checker):** Duplicate IP address on the segment.

**Human Reviewer Verdict:** Rejected

**Why AI Was Wrong:** With no ACL evidence provided in the case data at all,
the AI guessed a plausible-sounding but unsupported cause instead of
checking basic addressing first. This is a classic case of the AI not
following bottom-up troubleshooting — duplicate IP is a fundamental
Layer 3 addressing conflict that should be ruled out before investigating
ACLs. The AI's own stated confidence ("low") should have been a signal to
the reviewer that the diagnosis wasn't evidence-backed.

**Correction Applied:** Reviewer rejected the ACL theory entirely, replaced
root_cause with "Duplicate IP address assigned to two hosts", changed
next_command to `show ip arp` / `arping`, and confidence to "high" once
duplicate_ip evidence was confirmed.

---

## Case 4
**Symptom:** PC gets IP automatically but gateway is on the wrong subnet
**Show/config evidence:** route_exists = False, gateway otherwise fine

**AI Diagnosis:**
- root_cause: "DHCP pool has wrong default gateway configured"
- osi_layer: "Layer 3"
- confidence: "high"
- next_command: "show ip dhcp pool"

**Ground Truth (rule checker):** Missing static/dynamic route — no
evidence of a DHCP misconfiguration in this case's data.

**Human Reviewer Verdict:** Rejected

**Why AI Was Wrong:** The AI pattern-matched this case to Worked Example 3
in the prompt library (DHCP wrong default-router) because the symptom
phrasing was similar, rather than reasoning from the actual evidence
provided (route_exists = False). This shows a risk of the AI over-relying
on worked examples instead of the specific case data — exactly why
evidence-backed, per-case output is required.

**Correction Applied:** Reviewer replaced root_cause with "Missing route
to destination subnet", next_command with `show ip route`, and noted in
the review that examples should guide format/reasoning style only, not
be copied onto superficially similar symptoms.

---

## Case 5
**Symptom:** Guest WiFi reaches internal server
**Show/config evidence:** all rule-checker flags pass (no duplicate IP,
interface up, VLAN configured, route exists)

**AI Diagnosis:**
- root_cause: "No issue detected — all connectivity checks pass"
- osi_layer: "N/A"
- confidence: "high"
- next_command: "None"

**Ground Truth (per project's own example case):** Guest VLAN isolation
is not configured and no ACL blocks guest → internal traffic. This is a
security fault, not a connectivity fault, so the rule checker's basic
connectivity checks pass even though the network is misconfigured.

**Human Reviewer Verdict:** Rejected

**Why AI Was Wrong:** This is the most important case in the log: both
the AI and the deterministic checker treated "everything connects" as
"nothing is wrong." Neither tool checks for guest isolation/ACL rules
between VLANs, so a real security misconfiguration was missed entirely.
This shows why human review matters even when both the AI and automated
checks report "all clear" — connectivity ≠ correct/secure configuration.

**Correction Applied:** Reviewer flagged root_cause as "Guest VLAN
isolation not configured — guest traffic can reach internal VLAN",
osi_layer "Layer 2 and Layer 4", next_command `show access-lists`, and
recommended the rule checker be extended with a VLAN-isolation/ACL check
for future cases.

---

## Summary

| Case | AI Verdict | Category of AI Error |
|------|-----------|------------------------|
| 1 | Edited | Missed lower-layer (interface) fault |
| 2 | Edited | Missed co-occurring Layer 2 fault |
| 3 | Rejected | Unsupported guess, ignored own low confidence |
| 4 | Rejected | Over-matched to a worked example instead of case evidence |
| 5 | Rejected | False negative — missed security misconfiguration entirely |

**Key takeaway:** AI diagnoses were most reliable on single, clearly
evidenced faults, and least reliable when (a) multiple faults co-occurred,
(b) case evidence loosely resembled a worked example, or (c) the fault was
a security/policy issue rather than a hard connectivity failure. This
directly supports the project's Safety Rule requiring human review before
any diagnosis is accepted.
