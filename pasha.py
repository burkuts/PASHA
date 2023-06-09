#!/usr/bin/env python3
# PASHA V2
import os
import socket
import whois
import getpass
import requests
import json
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from colorama import Fore, Style
from bs4 import BeautifulSoup

def find_subdomains(hedef):
    url = f"https://crt.sh/?q=%.{hedef}&output=json"
    response = requests.get(url)
    data = response.json()
    subdomains = set()
    for item in data:
        name_value = item['name_value']
        if '*' not in name_value:
            subdomains.add(name_value)
    return subdomains

username = getpass.getuser()

def clear_screen():
    os.system("clear")

def print_menu():
    with open("banner.txt", "r") as file:
        banner = file.read()
    print(banner)
    print("[1] IP Derin Tarama [YAKINDA]")
    print("[2] Web Derin Tarama")
    print("[3] Robots.txt verisi")
    print("[4] IP üzerinden açık portlar")
    print("[5] WHOIS")
    print("[6] DNS kayıtları")
    print("[7] Web Headers Bilgisi")
    print("[8] CMS Algılama")

try:
    while True:
        tur = None
        while tur is None or tur < 1 or tur > 8:
            try:
                clear_screen()
                print_menu()
                tur = int(input(Fore.GREEN + "Ne tür bir arama yapmak istiyorsunuz: "))
                if tur < 1 or tur > 8:
                    raise ValueError(Fore.RED + "Geçersiz giriş!")
            except ValueError as e:
                clear_screen()
                print(Fore.RED + str(e))
                input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")

        if tur == 1:
            print(Fore.GREEN + "YAKINDA", username)
        
        elif tur == 2:
            
            clear_screen()
            hedef = input(Fore.BLUE + "Hedef web sitesini HTTP/S olmadan yazınız: ")
            wp = requests.head(f"https://{hedef}/wp-content/")
            if wp.status_code == 200:
               print(Fore.GREEN + "\nWordPress CMS!")
            else:
               print(Fore.RED + "\nWordPress CMS değil!")
           
            def get_page(url):
                response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'}))
                soup = BeautifulSoup(response, 'html.parser', from_encoding=response.headers.get_content_charset())
                return soup
    
            try:
                robots = get_page(f"https://{hedef}/robots.txt/")
                robots_txt = str(robots)
                print(Fore.GREEN + "\nrobots.txt bulundu.")
                print("robots.txt içeriği:")
                print(robots_txt)
    
            except urllib.error.HTTPError as e:
                print(Fore.RED + "\nrobots.txt bulunamadı;", e)

            # Web headers bilgisi
            try:
                response = requests.head(f"https://{hedef}/")
                if response.status_code == 200:
                    print(Fore.CYAN + "\nBaşarılı!")
                    headers = response.headers
                    print(Fore.RED + "Web Headers Bilgisi:")
                    for header, value in headers.items():
                        print(Fore.LIGHTRED_EX + f"{header}: {value}")
                else:
                    print(Fore.RED + "Web Headers Başarısız!")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + "Hata oluştu:", str(e))

            def get_whois_info(hedef):
                try:
                   whois_info = whois.whois(hedef)  # WHOIS bilgilerini alın
                   print(Fore.GREEN + "\nWHOIS Bilgileri:")
                   print("Domain Adı:", whois_info.domain_name)
                   print("Oluşturulma Tarihi:", whois_info.creation_date)
                   print("Son Güncelleme Tarihi:", whois_info.updated_date)
                   print("Son Geçerlilik Tarihi:", whois_info.expiration_date)
                   print("Kayıt Sahibi:", whois_info.registrar)
                   print("Name Server'lar:", whois_info.name_servers)
                except Exception as e:
                   print(Fore.RED + "\nWHOIS bilgileri alınırken hata oluştu:", str(e))
            get_whois_info(hedef)
            
            
            subdomains = find_subdomains(hedef)

            print(Fore.GREEN + "\nBulunan subdomainler:")
            for subdomain in subdomains:
                print(subdomain)  
            
            print("\n")
            print(Fore.GREEN + "DNS Kayıtları:")
            # A kaydı sorgusu
            a_records = socket.gethostbyname_ex(hedef)[2]
            for record in a_records:
                print(Fore.GREEN + "A Record:", record)

            # MX kaydı sorgusu
            mx_records = socket.getaddrinfo(hedef, 25, socket.AF_INET, socket.SOCK_STREAM)
            for record in mx_records:
                print(Fore.GREEN + "MX Record:", record[4][0])

            # NS kaydı sorgusu
            ns_records = socket.gethostbyname_ex(hedef)[2]
            for record in ns_records:
                print(Fore.GREEN + "NS Record:", record)

            # CNAME kaydı sorgusu
            cname_record = socket.gethostbyname_ex(hedef)[0]
            if cname_record != hedef:
                print(Fore.GREEN + "CNAME Record:", cname_record)

            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")
        
        elif tur == 3:
            hedef = input(Fore.RED + "Hedef web sitesini HTTP/S olmadan yazınız: ")
            print(Fore.GREEN + hedef)
            def get_page(url):
                response = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla'}))
                soup = BeautifulSoup(response, 'html.parser', from_encoding=response.headers.get_content_charset())
                return soup
    
            try:
                robots = get_page(f"https://{hedef}/robots.txt/")
                robots_txt = str(robots)
                print(Fore.GREEN + "robots.txt bulundu.")
                print("robots.txt içeriği:")
                print(robots_txt)
    
            except urllib.error.HTTPError as e:
                print(Fore.RED + "robots.txt bulunamadı;", e)

            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")
        
        elif tur == 4:
            hedef = input(Fore.RED + "Hedef web sitesini HTTP/S olmadan yazınız: ")
            print(Fore.GREEN + hedef)
            
            dosya_adı = input(Fore.LIGHTYELLOW_EX + "Verinin kaydedileceği dosyanın adını yazınız (dosya uzantısı belirtmeyiniz): ")
            clear_screen()
            with open("banner.txt", "r") as file:
                banner = file.read()
            print(Fore.RED + banner)
            
            subprocess.run(["nmap", "-Pn", "-sV", "-oX", f"{dosya_adı}.xml", hedef])
            
            tree = ET.parse(f"{dosya_adı}.xml")
            root = tree.getroot()
            
            etiket_yolu = './host/ports/port[state][service]'
            portlar = root.findall(etiket_yolu)
            
            for port in portlar:
                portid = port.get('portid')
                protocol = port.get('protocol')
                state = port.find('state').get('state')
                service = port.find('service').get('name')
                print(Fore.GREEN + f"Port ID: {portid}, Protocol: {protocol}, State: {state}, Service: {service}")
                input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")

        elif tur == 5:
            def get_whois_info(domain):
                try:
                   whois_info = whois.whois(domain)  # WHOIS bilgilerini alın
                   print(Fore.GREEN + "WHOIS Bilgileri:")
                   print("Domain Adı:", whois_info.domain_name)
                   print("Oluşturulma Tarihi:", whois_info.creation_date)
                   print("Son Güncelleme Tarihi:", whois_info.updated_date)
                   print("Son Geçerlilik Tarihi:", whois_info.expiration_date)
                   print("Kayıt Sahibi:", whois_info.registrar)
                   print("Name Server'lar:", whois_info.name_servers)
                except Exception as e:
                   print(Fore.RED + "WHOIS bilgileri alınırken hata oluştu:", str(e))

            def get_domain_info(domain):
                get_whois_info(domain)

            while True:
                domain = input("Hedef alan adını giriniz (Çıkmak için 'q' tuşuna basın): ")
                if domain.lower() == 'q':
                    break
                get_domain_info(domain)
            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")

        elif tur == 6:
            domain = input(Fore.RED + "Hedef alan adını giriniz: ")
            # A kaydı sorgusu
            a_records = socket.gethostbyname_ex(domain)[2]
            for record in a_records:
                print(Fore.GREEN + "A Record:", record)

            # MX kaydı sorgusu
            mx_records = socket.getaddrinfo(domain, 25, socket.AF_INET, socket.SOCK_STREAM)
            for record in mx_records:
                print(Fore.GREEN + "MX Record:", record[4][0])

            # NS kaydı sorgusu
            ns_records = socket.gethostbyname_ex(domain)[2]
            for record in ns_records:
                print(Fore.GREEN + "NS Record:", record)

            # CNAME kaydı sorgusu
            cname_record = socket.gethostbyname_ex(domain)[0]
            if cname_record != domain:
                print(Fore.GREEN + "CNAME Record:", cname_record)

            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")
        
        elif tur == 7:
            hedef = input("Hedef web sitesini HTTP/S olmadan yazınız: ")
            print(Fore.GREEN + hedef)
            
            clear_screen()
            # Web headers bilgisi
            try:
                response = requests.head(f"https://{hedef}/")
                if response.status_code == 200:
                    print(Fore.CYAN + "Başarılı!")
                    headers = response.headers
                    print(Fore.RED + "Web Headers Bilgisi:")
                    for header, value in headers.items():
                        print(Fore.LIGHTRED_EX + f"{header}: {value}")
                else:
                    print(Fore.RED + "Başarısız!")
            except requests.exceptions.RequestException as e:
                print(Fore.RED + "Hata oluştu:", str(e))
            
            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")
        
        elif tur == 8:
            hedef = input(Fore.BLUE + "Hedef web sitesini HTTP/S olmadan yazınız: ")
            wp = requests.head(f"https://{hedef}/wp-content/")
            if wp.status_code == 200:
               print(Fore.GREEN + "WordPress CMS!")
            else:
               print(Fore.RED + "WordPress CMS değil!")
            input(Style.RESET_ALL + "Devam etmek için bir tuşa basın...")

except KeyboardInterrupt:
    print(Fore.MAGENTA + "\nProgram kullanıcı tarafından durduruldu!")
    exit()
