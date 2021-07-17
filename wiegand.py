from machine import Pin, Timer
import utime

CARD_MASK = 0b11111111111111110 # 16 unos
FACILITY_MASK = 0b1111111100000000000000000 # 8 unos

# Intervalo de pulso máximo: 2ms
# Ancho de pulso: 50us

class Wiegand:
    def __init__(self, pin0, pin1, callback):
        """
        pin0: el GPIO que sube cuando el lector envía un cero.
        pin1: el GPIO que sube cuando el lector envía uno.
        Devolución de llamada: la función llamada (con dos argumentos: ID de tarjeta y cuenta de tarjeta)
        cuando se detecta una tarjeta. Tenga en cuenta que las limitaciones de implementación de interrupciones
        de micropython se aplican a la devolución de llamada.
        """
        self.pin0 = Pin(pin0, Pin.IN)
        self.pin1 = Pin(pin1, Pin.IN)
        
        self.callback = callback
        self.last_card = None
        self.next_card = 0
        self._bits = 0
        
        self.pin0.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin0)
        self.pin1.irq(trigger=Pin.IRQ_FALLING, handler=self._on_pin1)
        
        self.last_bit_read = None
        self.timer = Timer(-1)
        self.timer.init(period=50, mode=Timer.PERIODIC, callback=self._cardcheck)
        self.cards_read = 0

    def _on_pin0(self, newstate): self._on_pin(0, newstate)
    def _on_pin1(self, newstate): self._on_pin(1, newstate)

    def _on_pin(self, is_one, newstate):
        now = utime.ticks_ms()
        if self.last_bit_read is not None and now - self.last_bit_read < 2:
            # Demasiado rápido
            return

        self.last_bit_read = now
        self.next_card <<= 1
        if is_one: self.next_card |= 1
        self._bits += 1

    def get_card(self):
        if self.last_card is None:
            return None
        return ( self.last_card & CARD_MASK ) >> 1
        
    def get_facility_code(self):
        if self.last_card is None:
            return None
        # Específico para wiegand estándar de 26 bits
        return ( self.last_card & FACILITY_MASK ) >> 17

    def _cardcheck(self, t):
        if self.last_bit_read is None: return
        now = utime.ticks_ms()
        if now - self.last_bit_read > 50:
            # Demasiado lento - nuevo comienzo!
            self.last_bit_read = None
            self.last_card = self.next_card
            self.next_card = 0
            self._bits = 0
            self.cards_read += 1
            self.callback(self.get_card(), self.get_facility_code(), self.cards_read)
