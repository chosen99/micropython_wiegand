from wiegand import Wiegand
from machine import Pin

WIEGAND_ZERO = 14  # NUMERO DE PIN D0 verde
WIEGAND_ONE = 15  # NUMERO DE PIN D1 blanco


def on_card(card_number, facility_code, cards_read):
    print("Numero de tarjeta: "+ str(card_number) + "\nFacility code: " + str(facility_code))
    fc = bin(facility_code) # CONVERTIR FACILITY_CODE A BINARIO
    
    cn = bin(card_number) # CONVERTIR CARD_NUMBER A BINARIO
    cn = cn[2:len(cn)] # EXTRAER 0b DEL CODIGO BONARIO
    
    faltantes = 16 - len(cn) # VER CANTIDAD DE 0 QUE HACEN FALTA PARA COMPLETAR 16 bits DE CARD_NUMBER
    ceros = "" # ACARREO DE CEROS FALTANTES
    
    if (faltantes != 0):
        for i in range(faltantes):
            ceros = ceros + "0" # GERERAR CEROS FALTANTES
        
    co = int(fc + ceros + cn) # UNIFICAR FACILITY_CODE Y CARD_CODE PARA CALCULAR EL CODIGO DE TARJETA
    """
    NOTA: ESTA PARTE ES OPCIONAL SI SE REQUIEREN LOS 10 DIGITOS QUE CONTRAE ALGUNAS DE LAS TARJETAS
    EN ESTE CASO EN ESPECIFICO ES REQUERIDO CONTAR CON ELLO YA QUE SE REALIZA UNA CONSULTA A BASE CON
    LOS 10 CARACTERES DE LA TARJETA
    """
    plantilla = "Codigo de tarjeta: "
    faltantes = 10 - len(str(co))
    ceros = ""
    if(faltantes < 10):
        for i in range(faltantes):
            ceros = ceros + "0"
    print(plantilla + ceros + str(co) + "\n")

Wiegand(WIEGAND_ZERO, WIEGAND_ONE, on_card)



