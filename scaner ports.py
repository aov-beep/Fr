import socket
import threading
from datetime import datetime


def scan_port(target, port, open_ports):
    """Сканує окремий порт та додає відкриті порти до списку"""
    try:
    
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"[+] Порт {port:5} ВІДКРИТИЙ")
                open_ports.append(port)
    except (socket.error, socket.timeout):
        pass  
    except Exception as e:
        print(f"[-] Помилка при скануванні порту {port}: {e}")


def get_service_name(port):
   
    services = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        80: "HTTP",
        110: "POP3",
        443: "HTTPS",
        3306: "MySQL",
        3389: "RDP",
        8080: "HTTP-Proxy"
    }
    return services.get(port, "Невідомий сервіс")


def main():
    print("=" * 50)
    print("          СКАНЕР ПОРТІВ")
    print("=" * 50)
    
   
    target = input("\nВведіть IP-адресу або домен для сканування: ").strip()
    
    
    if not target:
        print("\n[!] Помилка: Не вказано ціль для сканування.")
        return
    
   
    try:
        target_ip = socket.gethostbyname(target)
        print(f"\n[+] Резолвінг домену: {target} -> {target_ip}")
    except socket.gaierror:
        print("\n[!] Помилка: Неможливо розпізнати хост. Перевірте правильність введення.")
        return

    print("-" * 50)
    print(f"Сканування цілі: {target_ip}")
    print(f"Час початку: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 50)

   
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 3389, 8080]
    
    print(f"\n[+] Сканується {len(ports)} портів...\n")
    
    threads = []
    open_ports = []  # Список для зберігання відкритих портів

 
    for port in ports:
        t = threading.Thread(target=scan_port, args=(target_ip, port, open_ports))
        threads.append(t)
        t.start()

    
    for t in threads:
        t.join()

   
    print("-" * 50)
    print("\n" + "=" * 50)
    print("          РЕЗУЛЬТАТИ СКАНУВАННЯ")
    print("=" * 50)
    
    if open_ports:
        print(f"\n[✓] Знайдено {len(open_ports)} відкритих портів:\n")
        print("Порт\tСервіс")
        print("-" * 30)
        for port in sorted(open_ports):
            service = get_service_name(port)
            print(f"{port}\t{service}")
    else:
        print("\n[!] Відкритих портів не знайдено.")
    
    print("\n" + "-" * 50)
    print(f"Сканування завершено: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 50)

   
    again = input("\nБажаєте виконати нове сканування? (так/ні): ").strip().lower()
    if again in ['так', 'yes', 'y', 'т']:
        print("\n" * 2)
        main()
    else:
        print("\nДякуємо за використання сканера портів!")


if __name__ == "__main__":
    main()














