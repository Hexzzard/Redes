from netmiko import ConnectHandler
import ipaddress

#dirección IP de la VM de GNS3
server = '192.168.56.101'

#puertos de cada dispositivo
DISPOSITIVOS = {
    'SWL31': {'port': 5001, 'tipo': 'switch'},
    'SWL32': {'port': 5002, 'tipo': 'switch'},
    'SWL21': {'port': 5003, 'tipo': 'switch'},
    'SWL22': {'port': 5004, 'tipo': 'switch'},
    'SWL23': {'port': 5005, 'tipo': 'switch'},
    'PC1': {'port': 5006, 'tipo': 'pc'},
    'PC2': {'port': 5008, 'tipo': 'pc'},
    'PC3': {'port': 5010, 'tipo': 'pc'},
    'R1': {'port': 5011, 'tipo': 'router'},
}

#tipos de portchannel active - pasive - desirable - auto - on
port_channel1 = ['desirable', 'auto']   # SWL31 - SWL32
port_channel2 = ['active', 'passive']   # SWL31 - SWL21
port_channel3 = ['on', 'on']            # SWL31 - SWL22
port_channel4 = ['active', 'passive']   # SWL32 - SWL22
port_channel5 = ['desirable', 'auto']   # SWL32 - SWL23

#IPs de las VLAN
ip_vlan100 = '192.168.10.0 255.255.255.0'
ip_vlan200 = '192.168.20.0 255.255.255.0'
ip_vlan300 = '192.168.30.0 255.255.255.0'

#configuracion VTP
vtp_domain = 'LAB'
vtp_password = 'hola'
vtp_version = 2



#generar IPs de gateways y pcs pertenecientes a la VLAN

#VLAN100
ip_str, mask = ip_vlan100.split()
gateway_ip = str(ipaddress.IPv4Address(ip_str) + 1)
gateway_vlan100_1 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 2)
gateway_vlan100_2 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 101)
PC_vlan100 = f"{gateway_ip} {mask}"

#VLAN200
ip_str, mask = ip_vlan200.split()
gateway_ip = str(ipaddress.IPv4Address(ip_str) + 1)
gateway_vlan200_1 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 2)
gateway_vlan200_2 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 101)
PC_vlan200 = f"{gateway_ip} {mask}"

#VLAN300
ip_str, mask = ip_vlan300.split()
gateway_ip = str(ipaddress.IPv4Address(ip_str) + 1)
gateway_vlan300_1 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 2)
gateway_vlan300_2 = f"{gateway_ip} {mask}"

gateway_ip = str(ipaddress.IPv4Address(ip_str) + 101)
PC_vlan300 = f"{gateway_ip} {mask}"

# =================== comandos de configuracion ===================

#todos los comandos utilizados para realizar la red
#se añadieron variables para aumentar la flexibilidad de la automatizacion
CONFIGURACIONES = {
    'R1': [
        "interface fastEthernet1/0",
        "ip address 192.168.2.1 255.255.255.0",
        "no shutdown",

        "interface fastEthernet1/1",
        "ip address 192.168.3.1 255.255.255.0",
        "no shutdown",

        "interface loopback0",
        "ip address 8.8.8.8 255.255.255.255",

        f"ip route {ip_vlan100} 192.168.2.2",
        f"ip route {ip_vlan200} 192.168.2.2",
        f"ip route {ip_vlan300} 192.168.3.2"
    ],

    'SWL31':[
        f"vtp domain {vtp_domain}",
        f"vtp password {vtp_password}",
        f"vtp version {vtp_version}",
        "vtp mode server",
        "interface range ethernet0/0-1",
        "no switchport",
        f"channel-group 1 mode {port_channel1[0]}",
        "exit",

        "interface port-channel 1",
        "no switchport",
        "ip address 192.168.1.1 255.255.255.0",
        "exit",

        "interface range ethernet0/2-3",
        f"channel-group 2 mode {port_channel2[0]}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface port-channel2",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface range ethernet1/0-1",
        f"channel-group 3 mode {port_channel3[0]}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface port-channel3",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface ethernet1/2",
        "switchport trunk encapsulation dot1q",
        "switchport trunk allowed vlan 100,200,300",
        "switchport mode trunk",
        "exit",

        "vlan 100",
        "vlan 200",
        "vlan 300",

        "interface vlan 100",
        f"ip address {gateway_vlan100_1}",
        "no shutdown",
        "exit",

        "interface vlan 200",
        f"ip address {gateway_vlan200_1}",
        "no shutdown",
        "exit",

        "interface vlan 300",
        f"ip address {gateway_vlan300_1}",
        "no shutdown",
        "exit",

        "interface ethernet2/0",
        "no switchport",
        "ip address 192.168.2.2 255.255.255.0",
        "no shutdown",

        "ip route 0.0.0.0 0.0.0.0 192.168.2.1",
        "ip routing"
    ],

    'SWL32': [
        f"vtp domain {vtp_domain}",
        f"vtp password {vtp_password}",
        "vtp mode client",
        "interface range ethernet0/0-1",
        "no switchport",
        f"channel-group 1 mode {port_channel1[1]}",
        "exit",

        "interface port-channel 1",
        "no switchport",
        "ip address 192.168.1.2 255.255.255.0",
        "exit",

        "interface range ethernet0/2-3",
        f"channel-group 2 mode {port_channel4[0]}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface port-channel2",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface range ethernet0/2-3",
        f"channel-group 3 mode {port_channel5[0]}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface port-channel3",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface ethernet1/2",
        "switchport trunk encapsulation dot1q",
        "switchport trunk allowed vlan 100,200,300",
        "switchport mode trunk",
        "exit",

        "interface vlan 100",
        f"ip address {gateway_vlan100_2}",
        "no shutdown",
        "exit",

        "interface vlan 200",
        f"ip address {gateway_vlan200_2}",
        "no shutdown",
        "exit",

        "interface vlan 300",
        f"ip address {gateway_vlan300_2}",
        "no shutdown",
        "exit",

        "interface ethernet2/0",
        "no switchport",
        "ip address 192.168.3.2 255.255.255.0",
        "no shutdown",

        "ip route 0.0.0.0 0.0.0.0 192.168.3.1",
        "ip routing"
    ],

    'SWL21': [
        f"vtp domain {vtp_domain}",
        f"vtp password {vtp_password}",
        "vtp mode client",
        "interface range ethernet0/0-1",
        f"channel-group 1 mode {port_channel2[1]}",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        
        "exit",

        "interface port-channel1",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface ethernet0/2",
        "switchport trunk allowed vlan 100,200,300",
        "switchport mode trunk",

        "interface range ethernet1/0-1",
        "switchport mode access",
        "switchport access vlan 100",
        "spanning-tree portfast"
    ],

    'SWL22': [
        f"vtp domain {vtp_domain}",
        f"vtp password {vtp_password}",
        "vtp mode client",
        "interface range ethernet0/0-1",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        f"channel-group 1 mode {port_channel3[1]}",
        "exit",

        "interface port-channel1",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface range ethernet0/2-3",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        f"channel-group 2 mode {port_channel4[1]}",
        "exit",

        "interface port-channel2",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface range ethernet1/0-1",
        "switchport mode access",
        "switchport access vlan 200",
        "spanning-tree portfast"
    ],

    'SWL23': [
        f"vtp domain {vtp_domain}",
        f"vtp password {vtp_password}",
        "vtp mode client",
        "interface range ethernet0/0-1",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk native vlan 1",
        "switchport trunk allowed vlan 100,200,300",
        f"channel-group 1 mode {port_channel5}",
        "exit",

        "interface port-channel1",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface ethernet0/2",
        "switchport trunk encapsulation dot1q",
        "switchport mode trunk",
        "switchport trunk allowed vlan 100,200,300",
        "exit",

        "interface range ethernet1/0-1",
        "switchport mode access",
        "switchport access vlan 300",
        "spanning-tree portfast"
    ]
    #no funcionan los VPCs
    #,
    #'PC1':[
    #    f"ip {PC_vlan100} {gateway_vlan100_1}"
    #],
    #'PC2':[
    #    f"ip {PC_vlan200} {gateway_vlan200_1}"
    #],
    #'PC3':[
    #    f"ip {PC_vlan300} {gateway_vlan300_2}"
    #]
    


}

# =================== Función general para configurar ===================

def generar_conexion(nombre_dispositivo, info):
    return {
        'device_type': 'cisco_ios_telnet', #se conecta por telnet
        'ip': server,
        'port': info['port'],
        'username': '',
        'password': '',
        'secret': '',
        'timeout': 30,  # aumentar tiempo de espera
    }

def configurar_dispositivo(nombre_dispositivo, comandos):
    device_info = generar_conexion(nombre_dispositivo, DISPOSITIVOS[nombre_dispositivo])
    print(f"[*] Conectando a {nombre_dispositivo} ({device_info['ip']}:{device_info['port']}) ...")
    
    connection = ConnectHandler(**device_info)
    connection.enable()

    output = connection.send_config_set(comandos)
    print(f"[+] Salida de {nombre_dispositivo}:\n{output}")

    connection.save_config()
    connection.disconnect()
    print(f"[✓] Configuración de {nombre_dispositivo} completada.\n")

# =================== Ejecución ===================

if __name__ == "__main__":
    for nombre, comandos in CONFIGURACIONES.items():
        configurar_dispositivo(nombre, comandos)
