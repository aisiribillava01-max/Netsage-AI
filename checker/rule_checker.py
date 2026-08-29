"""
Netsage AI - Rule-Based Config Checker
Standalone script: scans cases.csv, predicts each case's category from
its symptom text using keyword rules, and reports the AI agreement rate.
Run with: python checker/rule_checker.py   (from the NetSage-AI root folder)
"""
import pandas as pd

df = pd.read_csv("dataset/cases.csv")

CATEGORY_KEYWORDS = {
    "VLAN": ["vlan", "trunk", "switchport", "svi", "native vlan"],
    "DHCP": ["dhcp", "ip address", "lease", "apipa", "169.254", "helper-address"],
    "DNS": ["dns", "resolve", "hostname", "nslookup", "name-server"],
    "ACL": ["acl", "access-list", "blocked", "denied", "access-group"],
    "NAT": ["nat", "overload", "translation", "public ip", "inside global"],
    "Routing": ["route", "ospf", "routing", "neighbor", "next-hop", "gateway"],
    "Wireless": ["wireless", "wifi", "ssid", "wpa", "ap ", "access point", "channel"],
}

def predict_category(symptom_text):
    text = str(symptom_text).lower()
    scores = {cat: sum(1 for kw in kws if kw in text) for cat, kws in CATEGORY_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "Mixed/Unknown"

if __name__ == "__main__":
    df["ai_predicted_category"] = df["symptom_reported"].apply(predict_category)
    df["correct"] = df["ai_predicted_category"] == df["category"]

    print(f"Total cases checked: {len(df)}")
    print(f"AI agreement rate: {df['correct'].mean()*100:.1f}%\n")

    mismatches = df[~df["correct"]]
    print(f"Cases needing human correction ({len(mismatches)}):")
    for _, row in mismatches.iterrows():
        print(f"  {row['case_id']}: predicted={row['ai_predicted_category']}, actual={row['category']}")
