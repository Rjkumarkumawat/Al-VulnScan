import subprocess

def analyze_with_llm(port, service, cves):
    prompt = f"""
Analyze the following network service for vulnerabilities and provide remediations:

Port: {port}
Service: {service}
CVEs: {', '.join(cves) if cves else 'None found'}

1. Summarize each CVE with severity and description.
2. Provide clear, command-line remediation steps (Linux).
3. Rate risk level: LOW, MEDIUM, HIGH, CRITICAL
"""

    try:
        process = subprocess.Popen(
            ["ollama", "run", "llama3"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        response, _ = process.communicate(prompt)
        return response.strip()
    except Exception as e:
        return f"[ERROR] AI analysis failed: {e}"

