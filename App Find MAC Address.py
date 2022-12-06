import netmiko as nk
import re

def Buscar(macadd,conex):
    macta = conex.send_command("show mac address-table | include " + macadd)
    mat=re.compile(r"\s*?(\d\s+[a-f0-9]{1,4}\.[a-f0-9]{1,4}\.[a-f0-9]{1,4}\s+\w+)\s+((Fa|Gi)\d{1,2}\/\d{1,2}\/?(\d{1,2})?)")
    checar = mat.search(macta)
    if checar != None:
        port = checar.group(2)
   
    else:
        print("--- La mac address ingresada no esta en esta red")
    neidet= conex.send_command("show cdp neighbors detail")
    todip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",neidet)  
    ipssw = []
    [ipssw.append(i) for i in todip if i not in ipssw] 
    inter = re.findall(r"Interface:\s+[a-zA-Z]*\d{1,2}\/\d{1,2}\/?\d{1,2}",neidet)
    i=0
    for H in inter:     
        formato=re.compile(r"(Fa|Gi)[a-zA-Z]*([0-9]{1,2}\/[0-9]{1,2}\/?[0-9?]{1,2})")
        revisar=formato.search(H)
        inter[i]=revisar.group(1)+revisar.group(2)
        i+=1
    if port in inter:      
        pos=inter.index(port)
        ip = ipssw[pos]
              
        Device_cisco={
            "host":ip,
            "username":"cisco",
            "device_type":"cisco_ios",
            "port": 22,
            "password":"cisco",
            }
        try:
            conect = nk.ConnectHandler(**Device_cisco)
            conect.enable()
        except:
            print("----- NO SE LOGRO LA CONEXION REVISA TU DIRECCIONAMINETO -----")
        Buscar(macadd, conect)
           
    else:
        Host = conex.send_command("show running-config | include hostname")
        mat=re.compile(r"hostname (.*)")
        checar=mat.search(Host)
        print("!!! Direccion MAC encontrada en ",checar.group(1))
        print("en el puerto" ,port, "!!!")
        return None
        
def Verificar(ver,pat):
    mat = re.compile(pat)
    exp = mat.search(ver)
    if exp == None:
        print("-----Formato incorrecto, intente de nuevo.-----")
        return exp
    else:
        print("!!!DIRECCION EN FORMATO CORRECTO!!!")
        return exp.group()

def run():  
    while True:   
        print("-----APLICACION FIND MAC ADDRESS-----")
        print("Mauricio Macias  IRT 4-A")
        print("1-. Buscar MAC address.")
        print("2-. Salir") 
        opcion=input("Ingresa una opcion: ")
        if opcion == "1":
            
            while True:
             print("********  **    **       **   ****         **         **       **           ******")
             print("**        **    ** **    **   **   **      ** **   ** **      ** **      ****     ")
             print("*****     **    **  **   **   **    **     **  ** **  **     **   **     ****     ")
             print("**        **    **   **  **   **    **     **   **    **    **     **    ****     ")
             print("**        **    **    ** **   **   **      **         **   ***********   ****     ")
             print("**        **    **     **     ****         **         **  **         **     ******")

             ip = input("Ingresa la ip del SWITCH CORE: ")
             if Verificar(ip, r"\d{1,4}\.\d{1,4}\.\d{1,4}\.\d{1,4}") != None:
        
                 user = input("Ingrese el usuario:")
                 cont = input("Ingrese la contraseña:")
        
             else:
               print(" ----IP INGRESADA EN FORMATO ERRONEO---- ")
             break
    
            Device_cisco={
                "host":ip,
                "username":user,
                "device_type":"cisco_ios",
                "port":22,
                "password":cont,
                }
            try:
             net_connect = nk.ConnectHandler(**Device_cisco)
             net_connect.enable()
            except:
             print(" ----- NO SE LOGRO LA CONEXION INTENTA DE NUEVO -----")
             print("------ Asegurate que sea la IP de tu main switch -----")
             exit()
            
            print("!!! SE LOGRO LA CONEXION CON EXITO !!!")
            bus_mac = input("Ingresa la direccion mac que buscas en formato (FF-FF-FF-FF-FF-FF):").lower()
            #00-02-02-03-E7-F3 mia
            #c0-3e-ba-1d-d9-11 santi
            bus_mac = Verificar(bus_mac,r"[a-f0-9]{1,2}.[a-f0-9]{1,2}.[a-f0-9]{1,2}.[a-f0-9]{1,2}.[a-f0-9]{1,2}.[a-f0-9]{1,2}")

            if bus_mac != None:
                bus_mac = bus_mac.replace("-","")
                bus_mac = list(bus_mac)
                bus_mac.insert(4,".")
                bus_mac.insert(9,".")
                bus_mac = "".join(bus_mac)
                print(bus_mac)
                f = Buscar(bus_mac, net_connect)

                if f == None:
                 pass
        
            else:
                print(" ---- MAC INCORRECTA INTENTA CON OTRA ----")
                pass
        elif opcion == "2":
            print("Saliendo del script...")
            exit()

        else:
            print("Escoje otra opcion del menu, esa no existe")

run()