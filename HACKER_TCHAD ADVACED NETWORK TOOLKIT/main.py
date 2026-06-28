import socket
import requests
import dns.resolver
import dns.reversename
import dns.zone
import whois
import subprocess
import platform
import os
import json
import re
from bs4 import BeautifulSoup

# Configuration des couleurs
GREEN = '\033[92m'
BOLD = '\033[1m'
END = '\033[0m'

# Logo et Titre
LOGO = """
                       .                  ...:=*#%%@@@@@@%%#+=:..                  .                    
                                ..=*%@@@#*=--:::....:::-=+*%@@@%*=..           .                    
         .           .      .-*@@%*=....:-=+*#%%@@@@@%#*+=-:....=*%@@*-.                            
 . .            . .     .:*@@#-...:+%@@@%*=:..     .. ..:=*%@@@@+-...=%@@+:.                        
                     .:#@@=...=@@@#-.....    .      .    .  ....:#@@@=...+@@#.                      
                   .*@@=..-#@@+:.                                  .:=@@#-..=@@+..  .               
     .          .:#@*:.-#@%=..  .              .                      ..-#@#-.:#@#:.  .         .   
              .:%@+..=@@=.                       .                        .=%@+..*@#:. .         .  
            ..%@+..#@%. .                          .                     .   .#@#..*@#..            
         . .*@*..*@*..                    ...::-*%%%#-....                    ..*@#..#@=.        .  
         .:@%:.=@#:..     ... .      ..:-=====@@===%@@@+===-:..       .::.       .#@+.-@%:.         
       ..+@+.:%@-.    .:+@*.     ..:====--==:*@@#=-=@@@%==--===-:..  . .:%@*:.    .:@%:.#@=.        
    . ..#@-.-@#.  ...-@@@:    ..:-==-:..-=-. .+*:=-+@@@+-=-. .:-==-:..    +@@@:...  .*@=.+@+.  .    
    . .%@:.#@-. .=%.%@@#.    .-===:.  .-=-.     .==@@@-..-==:  ..:===-.   .:@@@+:%+...-@#.:@#.      
     .%@..#@:..:@%.%@@=-.  .--=-..   .-=-.      .=%*:.   .:=-.    ..-=-:.  =.+@@+-@%. .:@%.:@#.     
    .%@:.#@: .:@@--@+.++. .-=-:.    .-=-.       .+*. .    .-=-.    ..:-=-...%+:+%:#@%:. :%%.:@#..   
   .*@-.*@:.::*@%:-:#@#..-==-.      :=-.        .==.       .-=-..     .-==:..%@@-.-@@-=- .@#.=@=.   
  .=@= +@- -%.#@*-@@@- .-=======================+@@+=======================-..-@@@=%@=:@- :@*.+@-.  
  :%%.:@*.:%%.#%#@@=:..-==:::::::::-=-::::::::::@@@@-::::::::-=-::::::::::==-..-:%@%@--@%..+@-.%%.  
  +@:.%%..=@%:*@%::%. :=-.        .-=: . .      -##-.    .   .==:.        :-=:.-@-.#@-=@@- .%%.=@=  
 .@*.=@-  *@@-+-:%@= .==:. .      :=-.   .  ...-====-:..     .-=-.        .-==. +@@-::+@@-  -@+.#%. 
.+@-.%%...*@@=.#@@*..-=-.         -=-.    .:%=..+@@*. :%-.    :=-.   .     .-=-..+@@%:*@@-:..%%.-@=.
.%%.:@*.:--@@-%@@-. .-=:         .==:...-#@@@-  :@@-. :@@@#=...-=.         .:=-..::@@@+@%:+:.+@::%#.
:%#.=@- -*.#@#@%:+. :=-.         .=%@@@@@@@@%: .:-*:...#@@@@@@@@@-          .-=: -+.#@#@=.@- :@=.%%.
:@+ *@. +@:.@@#.=%..-=-..........:+@@@@@@@@@@:  .*%.  .%@@@@@@@@@+...........-=: .@+.*@*.*@=  @#.*@:
-@= #%  =@%.-%.*@*  -=============#@@@@@@@@@@-  .#%:  :@@@@@@@@@@@=============-  *@#.*:-@@-  #%.+@:
-@- %%  :@@#..=@@-  -=-..........:@@@@@@@@@@@#. .%@:  +@@@@@@@@@@@=..........-=:. -@@*.:@@%:  #% +@:
-@= #%  .%@@+:@@%.. :=-.        .=@@@@@@@@@@@@+..%@:.-@@@@@@@@@@@@#.. .     .-=:  .%@@-#@@*. .#%.+@:
:@+ *@. ::@@%*@@-=. .-=:.       .#@@@@@@@@@@@@@=:%@--@@@@@@@@@@@@@%:        :=-. -=-@@*@@#.-  %#.*@:
:@#.=@: =::%@#@#.**..-=-.       :@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@-       .-=-..%*.+@#@*.+= .@+.%%.
.%%.:@+.-@-.*@@-.%%. :==:.      -@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.     .:==. :@%.-@@:.#@: =@-:%#.
.+@:.%#..%@#.:@:-@@: .-=-.      *@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%.     .-=:. -@@--*.=@@*..#%:-@=.
 :@*.+@:.:@@@+..-@@-:..-=-......%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:.....-=-..:-@@-.-%@@*. :@*.#@. 
  *@:.@#. .%@@@--@@=:#..-=======@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+======-.-%.+@@:*@@@=.  *@:-@=  
  :@#.=@=...-@@@#%@*.#@:.-==:..:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@+ .:==-.=@*.#@#%@@*.=. -@=.%%.  
  .+@-.#%: -*.:%@%%@.=@@:.:==-..-@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*..-==:.=@@-.@@@@=.:%..:%%.=@=.  
   .#@:.%%. =@+..=@@+.@@%...-==-..#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-.-==-..:%@@.#@+..=%@: .#@.-@+.   
    .%%.:@#..:@@@*:.=:+@@=--..-==-.:#@@@@@@@@@@@@@@@@@@@@@@@@@@%-:-==-..+-+@@=:::+@@@*. .#@::@#.    
     .@%.:@#. .+@@@@@=.#@@:+@=..--==-#@@@@@@@@@@@@@@@@@@@@@@@@%-==--..*@=-@@+-#@@@@%.  .#@-.@%.     
      :%%.:%%.  .:@@@@@@=@%.+@@-  .-=%@@@@@@@@@@@@@@@@@@@@@@@@@=-...+@@=:@%#@@@@@=..  .%@::@%.      
      ..%@:.#@-...+.:-#@@@@@:=@@@-  .%@@@@@@@@@@@@@@@@@@@@@@@@@:  =@@@==@@@%+-:.-+. .-@#.-@#..      
   .    .*@=.+@*. .=@#+=:....:.+@@@*-@@@@@@@@@@@@@@@@@@@@@@@@@@+*@@%=..:-=++*#@%-. .*@+.+@+.        
         .-@%..%@=. .-#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.. .-@%::%@:          
     ..    .#@+.-@%:.   .:*%%%#+-...+@@@@@@@@@@@@@@@@@@@@@@@@@@%....:-==-:... ..:%@-.*@*.           
  .         .:@@-.=@%:. .-%*=::-+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%#**#%%:.  :%@=.=@%:.            
     ..       .-@@=.-%@+....=#@@@@@@@*@@@@@@@@@@@@@@@@@@@@@@@@+*@@@@@@*-.. .+@@=.=@@-.              
                .=%@=.:*@%-.          *@@@@@@@@@@@@@@@@@@@@@@@.        ..-#@#:.+@%-.    .           
     .            .:%@#:.:%@@=..      =@@@@@@@@@@@@@@@@@@@@@@#.     ..-%@%-.-%@#..         ..       
   .               . .-@@%:..*@@@+.   -@@@@@@@@@@@@@@@@@@@@@@+.  .=@@@*..-%@@:.                     
   .                   ..-%@%+..:=%@@%#@@@@@@@@@@@@@@@@@@@@@@%%@@%=:.:*@@#-..          .            
                           .:+%@@#=:..-=*#@@@@@@@@@@@@@@@@#*=-..:+#@@#=:..      . .             .   
          .                     .-*%@@@#+=-::..........::-=*%@@@%*-..     .  .            .         
     .           .                    ..-+#%@@@@@@@@@@@@%*=:..   .  .     .                       ..

"""
TITLE = "                      HACKER_TCHAD ADVANCED NETWORK TOOLKIT"


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80


def print_g(text, bold=False, center=False):
    style = BOLD if bold else ""
    width = get_terminal_width()
    if center:
        for line in text.split('\n'):
            print(f"{GREEN}{style}{line.center(width)}{END}")
    else:
        print(f"{GREEN}{style}{text}{END}")


class AdvancedNetworkTool:
    def __init__(self, target):
        self.target = target
        try:
            self.ip = socket.gethostbyname(target)
        except:
            self.ip = None

    # --- NETWORK TESTS ---
    def ping_test(self):
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        res = subprocess.run(['ping', param, '3', self.target], capture_output=True, text=True)
        return res.stdout

    def traceroute(self):
        cmd = 'tracert' if platform.system().lower() == 'windows' else 'traceroute'
        res = subprocess.run([cmd, self.target], capture_output=True, text=True)
        return res.stdout

    # --- DNS TOOLS ---
    def dns_lookup(self, rtype='A'):
        try:
            ans = dns.resolver.resolve(self.target, rtype)
            return [str(r) for r in ans]
        except:
            return "Aucun enregistrement."

    def reverse_dns(self):
        try:
            name = dns.reversename.from_address(self.ip)
            return str(dns.resolver.resolve(name, "PTR")[0])
        except:
            return "Non trouvé."

    def zone_transfer(self):
        try:
            ns = dns.resolver.resolve(self.target, 'NS')
            results = []
            for server in ns:
                try:
                    z = dns.zone.from_xfr(dns.query.xfr(str(server), self.target))
                    results.append(f"Succès sur {server}")
                except:
                    results.append(f"Échec sur {server}")
            return results
        except:
            return "Erreur NS."

    # --- IP & GEO ---
    def geo_lookup(self):
        try:
            r = requests.get(f"http://ip-api.com/json/{self.ip}").json()
            return json.dumps(r, indent=4)
        except:
            return "Erreur API."

    def asn_lookup(self):
        try:
            r = requests.get(f"https://ipapi.co/{self.ip}/json/").json()
            return f"ASN: {r.get('asn')} | Org: {r.get('org')}"
        except:
            return "Indisponible."

    # --- SCANNERS ---
    def port_scan(self, protocol='TCP'):
        open_p = []
        ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == 'TCP' else socket.SOCK_DGRAM)
            s.settimeout(0.5)
            if s.connect_ex((self.ip, p)) == 0: open_p.append(p)
            s.close()
        return open_p

    # --- WEB TOOLS ---
    def http_headers(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            return "\n".join([f"{k}: {v}" for k, v in r.headers.items()])
        except:
            return "Erreur HTTP."

    def extract_links(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            return [a.get('href') for a in soup.find_all('a', href=True)][:15]
        except:
            return "Erreur d'extraction."

    def reverse_analytics(self):
        try:
            r = requests.get(f"http://{self.target}", timeout=5)
            ua = re.findall(r'UA-\d+-\d+', r.text)
            gas = re.findall(r'G-[A-Z0-9]+', r.text)
            return {"Google_Analytics": list(set(ua + gas))}
        except:
            return "Aucun ID trouvé."


def menu():
    os.system('cls' if platform.system().lower() == 'windows' else 'clear')
    print_g(LOGO, center=True)
    print_g(TITLE, bold=True, center=True)
    print("\n")
    target = input(f"{GREEN} [>] ENTRER CIBLE (ex: google.com) : {END}").strip()
    tool = AdvancedNetworkTool(target)
    print()

    options = [
        "1. Test Ping", "2. Traceroute", "3. DNS Lookup (A)", "4. MX/NS/TXT Records",
        "5. Reverse DNS", "6. Whois Lookup", "7. IP Geolocation", "8. ASN Lookup",
        "9. TCP Port Scan", "10. HTTP Headers", "11. Extract Links", "12. Analytics Search",
        "13. Zone Transfer (AXFR)", "0. Quitter"
    ]

    while True:
        print_g("\n--- MENU DES OUTILS ---", bold=True)
        for o in options: print_g(o)

        choice = input(f"\n{GREEN} [?] CHOISIR UN NUMÉRO : {END}")

        if choice == '1':
            print_g(tool.ping_test())
        elif choice == '2':
            print_g(tool.traceroute())
        elif choice == '3':
            print_g(tool.dns_lookup('A'))
        elif choice == '4':
            for r in ['MX', 'NS', 'TXT']: print_g(f"{r}: {tool.dns_lookup(r)}")
        elif choice == '5':
            print_g(tool.reverse_dns())
        elif choice == '6':
            print_g(whois.whois(target))
        elif choice == '7':
            print_g(tool.geo_lookup())
        elif choice == '8':
            print_g(tool.asn_lookup())
        elif choice == '9':
            print_g(f"Ports ouverts: {tool.port_scan()}")
        elif choice == '10':
            print_g(tool.http_headers())
        elif choice == '11':
            print_g(tool.extract_links())
        elif choice == '12':
            print_g(tool.reverse_analytics())
        elif choice == '13':
            print_g(tool.zone_transfer())
        elif choice == '0':
            break
        else:
            print_g("Choix invalide.")


if __name__ == "__main__":
    menu()