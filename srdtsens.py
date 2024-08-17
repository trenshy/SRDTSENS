import requests
import sys
import argparse

# Cores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"

# Banner e versão
BANNER = """
  _____ _____  _____ _______ _____            _____  
 / ____|  __ \|  __ \__   __/ ____|          / ____| 
| (___ | |__) | |  | | | | | (___   ___  _ __ | (___   
 \___ \|  _  /| |  | | | |  \___ \ / _ \| '_ \ \___ \  
 ____) | | \ \| |__| | | |  ____) |  __/| | | |____) | 
|_____/|_|  \_\_____/  |_| |_____/ \___||_| |_|_____/  
                                                 
                SSRF Port Scanner - Versão 1.0                   
                    Feito por: Trenshy                   
"""


def ssrf_port_scan(target_url, port, keyword=None):
    """Realiza o port scanning usando SSRF e verifica o conteúdo da resposta."""
    url = f"{target_url}:{port}"
    try:
        response = requests.get(url, timeout=5)
        
        if response.ok:
            if keyword and keyword in response.text:
                print(f"{GREEN}[+] Porta {port} aberta - Conteúdo contém a palavra-chave '{keyword}'{RESET}")
            elif response.text:
                print(f"{GREEN}[+] Porta {port} aberta - Conteúdo significativo recebido{RESET}")
            else:
                print(f"{RED}[-] Porta {port} fechada - Sem conteúdo significativo{RESET}")
        else:
            print(f"{RED}[-] Porta {port} fechada ou resposta inválida{RESET}")
    except requests.exceptions.RequestException:
        print(f"{RED}[-] Porta {port} fechada ou inacessível{RESET}")

def print_help():
    """Exibe uma mensagem de ajuda."""
    help_message = """
Uso: python ssrf_port_scanner.py [opções]

Opções:
  -h, --help            Exibe esta mensagem de ajuda e sai
  -u URL, --url URL     URL alvo para o SSRF
  -w WORDLIST, --wordlist WORDLIST
                        Arquivo com a wordlist de portas
  -k KEYWORD, --keyword KEYWORD
                        Palavra-chave para verificar no conteúdo da resposta
  -v, --version         Exibe a versão do script

Exemplo:
  python ssrf_port_scanner.py -u "http://example.com/vulnerable_endpoint" -w ports.txt -k "flag"
"""
    print(help_message)

def print_version():
    """Exibe a versão do script."""
    print(BANNER)

def main():
    parser = argparse.ArgumentParser(description="SSRF Port Scanner", add_help=False)
    parser.add_argument("-u", "--url", required=True, help="URL alvo para o SSRF")
    parser.add_argument("-w", "--wordlist", required=True, help="Arquivo com a wordlist de portas")
    parser.add_argument("-k", "--keyword", help="Palavra-chave para verificar no conteúdo da resposta")
    parser.add_argument("-v", "--version", action="store_true", help="Exibe a versão do script")
    parser.add_argument("-h", "--help", action="store_true", help="Exibe esta mensagem de ajuda")

    args = parser.parse_args()

    if args.version:
        print_version()
        sys.exit(0)

    if args.help:
        print_help()
        sys.exit(0)

    target_url = args.url
    wordlist_file = args.wordlist
    keyword = args.keyword

    print(BANNER)
    print("\nIniciando o port scan...\n")

    try:
        with open(wordlist_file, "r") as file:
            ports = file.readlines()
            ports = [port.strip() for port in ports]
    except FileNotFoundError:
        print(f"{RED}Erro: Arquivo {wordlist_file} não encontrado.{RESET}")
        sys.exit(1)

    for port in ports:
        ssrf_port_scan(target_url, port, keyword)

    print("\nEscaneamento concluído.")

if __name__ == "__main__":
    main()
