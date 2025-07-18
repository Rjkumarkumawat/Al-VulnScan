import nmap
from rich.console import Console

def scan_target(target_ip, custom_ports=None):
    nm = nmap.PortScanner()
    console = Console()

    port_range = ",".join(str(p) for p in custom_ports) if custom_ports else "1-65535"

    try:
        console.print(f"[DEBUG] Scanning {target_ip} on ports: [bold]{port_range}[/bold] with -Pn -sV...", style="dim")
        nm.scan(target_ip, arguments=f"-Pn -sV -p {port_range}")
    except Exception as e:
        console.print(f"[red]Scan failed:[/red] {e}")
        return []

    services = []

    if target_ip not in nm.all_hosts():
        console.print("[red]No results found for the target IP.[/red]")
        return []

    for proto in nm[target_ip].all_protocols():
        ports = nm[target_ip][proto].keys()
        for port in ports:
            service = nm[target_ip][proto][port]
            services.append({
                "port": port,
                "name": service.get("name", ""),
                "product": service.get("product", ""),
                "version": service.get("version", ""),
                "extrainfo": service.get("extrainfo", "")
            })

    console.print("[DEBUG] Scan finished.\n", style="dim")
    return services

