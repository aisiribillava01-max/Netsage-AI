# NetSage AI Troubleshooting Dataset

This dataset contains 35 network troubleshooting cases created for the NetSage AI project.

## Categories

- VLAN - 5 cases
- DHCP - 5 cases
- DNS - 4 cases
- ACL - 4 cases
- NAT - 4 cases
- Routing - 5 cases
- Wireless - 4 cases
- Mixed - 4 cases

## Case Structure

Each case contains:

- Case ID
- Network category
- Problem title
- Difficulty
- Network topology
- Symptoms
- User report
- Device
- Relevant configuration
- Expected behavior
- Root cause
- Correct fix
- Severity
- Packet Tracer file reference

## Purpose

The dataset acts as the ground-truth reference for evaluating AI-generated network troubleshooting diagnoses.

The `root_cause` and `correct_fix` fields represent the expected human-verified answer.
