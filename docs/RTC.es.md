# ⏰ Reloj de tiempo real en la 3DO — instalación del DS3231

[← Volver al inicio](../README.es.md) · [English](RTC.md) · [Português](RTC.pt.md) · **Español**

La 3DO nunca tuvo reloj. Con un módulo **DS3231** conectado al Raspberry Pi Pico de la ODE y el firmware **TADEU 1.0.5**, tu consola pasa a saber la fecha, la hora y la temperatura. Es la **primera ODE de 3DO del mundo con reloj de tiempo real**.

Son **4 cables**. Quien ya soldó un cable puede hacerlo.

---

## Qué ganas

- Fecha, hora y temperatura en el menú principal.
- "Jugado: dd/mm/aaaa - hh:mm" en el último juego, en Recientes y en Estadísticas.
- Archivos grabados en el USB con la fecha correcta (las copias de la NVRAM llevan la fecha y la hora en el nombre).
- Ajuste del reloj desde la propia consola, en 12 o 24 horas.
- Aviso cuando se agota la pila del reloj.

## Detección automática

No hace falta configurar nada. Al encender, el menú pregunta a la ODE si existe un reloj.

- **Con el módulo**: aparecen la fecha, la hora y la temperatura, y las opciones del reloj entran en el menú.
- **Sin el módulo**: nada aparece y nada cambia. No hay reloj a cero ni mensaje de error; la consola funciona como siempre.

Es decir: instalar el firmware TADEU 1.0.5 **sin** el módulo no da ningún problema.

## Qué necesitas

| Elemento | Observación |
|---|---|
| Módulo **DS3231** | Cualquier módulo con los pines **VCC, GND, SDA y SCL**. El más común es el azul, con soporte para pila. |
| Pila del módulo | **CR2032** (mira el aviso de la pila más abajo). |
| 4 cables finos | Mejor en 4 colores. Unos 10 a 15 cm cada uno. |
| Soldador y estaño | Punta fina. |
| Firmware **TADEU 1.0.5** o más nuevo | Las versiones anteriores no hablan con el reloj. |

---

## La conexión

<p align="center"><img src="../github/rtc-ds3231-pinos.png" width="720" alt="Conexión del DS3231 en el Raspberry Pi Pico"></p>

| Pin del Pico | Nombre | Va al DS3231 |
|:---:|---|:---:|
| **1** | GP0 | **SDA** |
| **2** | GP1 | **SCL** |
| **3** | GND | **GND** |
| **36** | 3V3 (OUT) | **VCC** |

Los pines **32K** y **SQW** del módulo quedan sin conectar.

**Cómo encontrar los pines:** mira el Pico desde arriba, con el conector USB hacia arriba. El pin 1 es el primero de la izquierda, de arriba abajo; el 2 y el 3 vienen justo debajo. El pin 36 está en el lado derecho: es el **quinto** de arriba abajo (40, 39, 38, 37, **36**).

> ⚠️ **Usa el 3V3 (pin 36), nunca el VBUS ni el VSYS (pines 40 y 39).** Esos dos tienen 5 V y pueden dañar el Pico a través de los cables de datos.

> ⚠️ **No sueldes en los tres puntos "DEBUG"** del extremo inferior del Pico. Aquí no se usan.

---

## Paso a paso

1. **Desenchufa la consola** y ábrela hasta llegar a la placa de la ODE.
2. **Comprueba el firmware** antes de soldar: en *Opciones → Dispositivo ODE → Información del ODE* debe aparecer **TADEU 1.0.5** o más nuevo. Si no, actualiza primero.
3. **Suelda los 4 cables al módulo**: VCC, GND, SDA y SCL.
4. **Suelda los 4 cables al Pico**, siguiendo la tabla. Suelda rápido, con poco estaño, y comprueba que ningún pin toque al vecino. Los pines 1, 2 y 3 están uno al lado del otro: es donde más se falla.
5. **Pon la pila** en el módulo.
6. **Sujeta el módulo** con cinta de doble cara en un lugar donde no toque nada de metal. Aísla su parte inferior con cinta aislante.
7. **Cierra la consola y enciéndela.**

## Comprobar y ajustar la hora

1. Abre *Opciones → Dispositivo ODE → Recursos*. La línea **Reloj (DS3231)** debe decir **Sí**.
2. La primera vez, el menú avisa de que el reloj no tiene la hora correcta y ofrece ajustarla. Pulsa **A**.
   O ve a *Opciones → Dispositivo ODE → Fecha y hora*.
3. ◄ ► elige el campo, ▲ ▼ cambia el valor, **A** graba. Ahí también se elige **12 o 24 horas**.
4. Vuelve al menú principal: la fecha, la hora y la temperatura aparecen abajo, a la derecha.

Si quieres ocultar alguna: *Opciones → Apariencia → Menú principal → Hora / Fecha / Temperatura*.

---

## ⚠️ La pila

Muchos módulos DS3231 azules salen de fábrica con un **circuito de recarga** (un diodo y una resistencia junto al soporte), pensado para la pila recargable **LIR2032**.

- Con pila **CR2032 común** (no recargable): **desactiva el circuito de recarga**, quitando el diodo o la resistencia junto al soporte de la pila. Una pila común no se puede recargar.
- Con pila **LIR2032** (recargable): puedes dejar el circuito como está.

En caso de duda, usa el módulo con la recarga desactivada y una CR2032: dura años.

El DS3231 no mide la carga de la pila. Lo que sabe decir es si **el reloj se detuvo** en algún momento. Cuando eso ocurre, el menú avisa al encender de que la pila está baja y pide ajustar la hora. Si el aviso vuelve cada vez que enciendes la consola, cambia la pila.

---

## Problemas comunes

| Síntoma | Qué comprobar |
|---|---|
| **Reloj (DS3231): No** en Recursos | Firmware anterior al 1.0.5; SDA y SCL cruzados; soldadura fría; VCC en el pin equivocado. |
| La hora vuelve a cero al apagar | Pila baja, ausente o invertida. |
| Aviso de reloj sin hora cada vez | Pila baja: cámbiala y ajusta la hora de nuevo. |
| La consola no enciende después de la instalación | Apágala enseguida. Busca pines en corto (1, 2 y 3 están uno al lado del otro) y comprueba que el VCC no haya ido a parar al pin 39 o 40. |
| La temperatura parece alta | Es la temperatura **dentro de la consola**, medida por el propio DS3231. Es normal que sea más alta que la del ambiente. |

## Detalles técnicos

- Bus **I²C 0** del RP2040, a 100 kHz: **GP0 = SDA**, **GP1 = SCL**.
- Dirección del DS3231: **0x68**.
- El firmware lee el reloj y guarda la última lectura; el menú pregunta cada pocos segundos.
- La fecha y la hora también las usa el sistema de archivos de la ODE: todo lo que la consola graba en el USB sale con la fecha correcta.
- Conexión probada en la placa con un Raspberry Pi Pico común. El firmware usa los mismos GP0 y GP1 en la placa original (RP2040-Plus); si la tuya es esa, comprueba antes que esos dos pines estén libres en la placa.
- Sin el módulo, el firmware y el menú funcionan con normalidad: el reloj simplemente no aparece.
