import requests

def search_cves(service_name, version):
    query = f"{service_name} {version}".strip().replace(" ", "%20")
    api_url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={query}"
    
    try:
        res = requests.get(api_url, timeout=10)
        data = res.json()
        cves = [item["cve"]["id"] for item in data.get("vulnerabilities", [])[:5]]
        return cves
    except Exception as e:
        print("[ERROR] CVE Lookup failed:", e)
        return []

