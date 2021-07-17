## Raspberry Pi Pico Lectura de Wiegand 26 bits

### Descripción
Codigo para la lectura de tags/tarjetas RFID mediante una lectora de RFID conectada a una Raspberry Pi pico.

### Requisitos 
* Micropython
* Tener en cuenta que la raspberry pi (cualquier versión) trabaja con entradas en GPIO de 3.3 volts, es recomendable realizar un divisor de voltaje de al menos esta cantidad y hasta un pico de 3.5 volts, en cuestión de lo que se ha trabajado, este divisor no trabaja como uno "normal", ya que los valores adecuados en teoría serian con R1 = 100R y R2 = 220R dando un voltaje aproximado de 3.43 volts, esto en práctica no es así (al menos para el modelo de la lectora testeada la cual es una marca china, cabe resaltar que en lo personal esta lectora me daba demasiados problemas para mantener el voltaje con el divisor, tenía que estar desconectando esta para que los voltajes no se cayeran a 0.5 volts, esto en los pines D0 y D1, con la ROSSLARE AY-Z12A no tenia dicho problema con los divisores), en las pruebas la R1 = 100R y R2 = 3.3k, esto arroja en práctica un voltaje de 3.12 volts.

### Programas utilizados
* Thonny

### Instalación de Librerías
* Dirigirse a Herramientas > Gestionar paquetes, buscar la libreria machine e instalar
* Para la instalación de la librería wiegand.py, crear un nuevo fichero copiar el código y guardar dentro de Raspberry Pi Pico en carpeta llamada lib con el nombre wiegand.py

### Metodo de conexión 
* Se necesita conectar el cable verde (D0) en el GPIO 14 y el cable blanco (D1) en el GPIO 15 (con divisor de voltaje).
* Tambien es requerido conectar la tierra (GND) de la lectora a la Raspberry en un pin GND, de lo contrario esto genera que haya ruido durante la lectura y los datos no puedan ser interpretados correcatmente.
