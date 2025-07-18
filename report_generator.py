# report_generator.py

def append_report_md(service, cves, ai_text):
    with open("report.md", "a") as f:
        f.write(f"""## 🔍 Port {service['port']} - {service['product']} {service['version']}

📜 **CVEs**: {"None Found" if not cves else ", ".join(cves)}

📝 **AI Analysis**:
{ai_text}

---

""")

