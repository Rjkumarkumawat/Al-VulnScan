from scanner import scan_target
from cve_lookup import search_cves
from ai_analyzer import analyze_with_llm
from report_generator import append_report_md
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import pyfiglet

# Initialize rich console
console = Console()

# Fancy ASCII Banner
def print_banner():
    ascii_banner = pyfiglet.figlet_format("AI-VulnScan")
    console.print(f"[bold blue]{ascii_banner}[/bold blue]")

    banner_text = Text()
    banner_text.append("🧠 AI-Powered Network Vulnerability Scanner\n", style="bold magenta")
    banner_text.append("🔍 Built with Nmap + CVE Lookup + Local AI (LLM)\n")
    banner_text.append("👨‍💻 Created by Rajkumar Kumawat\n")
    console.print(Panel(banner_text, expand=False, border_style="bold green"))

# Main execution
def main():
    print_banner()

    # Reset the report file at the beginning
    with open("report.md", "w") as f:
        f.write("# 🔐 Network Vulnerability Report\n\n")

    # Ask user for target IP
    target_ip = console.input("[bold yellow]Enter target IP address: [/bold yellow]")

    # Ask for custom port input
    custom_ports = None
    port_choice = console.input("[bold cyan]Do you want to specify ports? (y/n): [/bold cyan]").strip().lower()
    if port_choice == "y":
        ports_input = console.input("[bold cyan]Enter comma-separated ports (e.g., 21,22,80): [/bold cyan]")
        try:
            custom_ports = [int(p.strip()) for p in ports_input.split(",") if p.strip().isdigit()]
            console.print(f"[green]✔️ Custom ports selected:[/green] {custom_ports}")
        except:
            console.print("[red]Invalid input. Scanning all ports...[/red]")

    console.print(f"\n[*] Scanning target [cyan]{target_ip}[/cyan]...\n", style="bold yellow")
    services = scan_target(target_ip, custom_ports)

    console.print(f"[+] Scan complete. Processing {len(services)} services...\n", style="bold green")

    for s in services:
        port = s["port"]
        product = s["product"]
        version = s["version"]

        console.print(f"\n[bold cyan]🔍 Port {port} - {product} {version}[/bold cyan]")

        # CVE Lookup
        cves = search_cves(product, version)
        if cves:
            console.print(f"📜 CVEs Found: [yellow]{', '.join(cves)}[/yellow]")
        else:
            console.print("📜 [dim]No CVEs found[/dim]")

        # AI Analysis
        console.print("🧠 Sending to local AI for analysis...")
        ai_text = analyze_with_llm(port, f"{product} {version}", cves)
        console.print("✅ [green]AI analysis complete.[/green]")

        # Display AI result
        console.print(f"\n[bold magenta]📝 Summary:[/bold magenta]\n{ai_text}\n")

        # Append to Markdown report
        append_report_md(s, cves, ai_text)
        console.print(f"[blue]📄 Report updated for port {port}[/blue]")

    console.print("\n✅ [bold green]Scan complete. Report saved to [underline]report.md[/underline][/bold green]")

if __name__ == "__main__":
    main()

