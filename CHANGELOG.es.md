# 📝 Historial de versiones

[← Volver al inicio](README.es.md) · [English](CHANGELOG.md) · [Português](CHANGELOG.pt.md) · **Español**

Todo lo que cambió en el **menú** (`boot.iso`), en el **firmware TADEU** y en el **generador** (`generate_usb.py`), de la versión más nueva a la más antigua.

- [Menu — 1.0](#menu--10)
- [Menú — antes de la 1.0 (versiones 0.x)](#menú--antes-de-la-10-versiones-0x)
- [Firmware TADEU](#firmware-tadeu)
- [Generador (generate_usb.py)](#generador-generate_usbpy)

---

## Menu — 1.0

Primera versión pública. Reúne todo lo hecho en las versiones de desarrollo (0.x), descritas más abajo, y añade:

- 💿🔥 **CD DE VERDAD EN EL XPORT, SIN QUITAR LA PLACA (exclusivo).** Con la placa de expansión conectada, la pantalla principal gana la caja **CD** (gris oscura sin disco, azul clara con disco). **A** saca el Xport del puerto, pide abrir y cerrar la tapa (FZ-10) o abre y cierra la bandeja (otros modelos), y la consola se reinicia sola en el disco. **B** cancela. El menú de fábrica del Xport no tiene esa función. Confirmado en consola real en la FZ-10; la bandeja automática de los otros modelos está en pruebas. La rutina va en un archivo aparte del disco (`XportCD`), cargado solo en ese momento.
- **Pantalla de descripción nueva**: el nombre del juego pasó a la barra de arriba y la ficha quedó ordenada ("Jugado: 2x - Última fecha", **desarrolladora**, **productora**, género, año, país, discos con iconos). Con una imagen, la ficha queda a su lado; con dos, las imágenes van a la izquierda y la ficha y el texto a la derecha; con tres, las imágenes quedan arriba. Nombre, desarrolladora y productora largos se desplazan despacio; desplazar el texto ya no detiene el vídeo; el efecto de favorito aparece sobre la carátula.
- **Tú eliges lo que muestra la ficha**: *Opciones > Apariencia > Descripción* muestra u oculta cada dato.
- **Editor de cada juego**, mostrado en la Vitrina y en la Tira (los textos de los juegos ganaron el campo `Publisher`).
- **Vídeos de 20 segundos a 15 fotogramas por segundo** como valor predeterminado.

Lo que tiene la 1.0, en resumen: 6 modos de vista, vista previa en vídeo, favoritos, recientes y estadísticas, filtro y orden, multidisco, gestor de partidas, herramientas de la consola, 3 idiomas, reloj de tiempo real, detección de la consola y funcionamiento con los dos firmwares.

---

## Menú — antes de la 1.0 (versiones 0.x)

Las versiones de desarrollo, de la más nueva a la más antigua.

### 0.9 — Vitrina, Tira, fondos y opciones nuevas

**Nuevos modos Vitrina y Tira**
- **Dos modos de vista nuevos**: **Vitrina** (portada grande con desarrollador, género, año, país y la descripción entera) y **Tira** (la captura del juego y la descripción arriba, una fila de portadas deslizándose abajo).
- En los dos, ◄ ► cambia de juego y ▲ ▼ desplaza la descripción.
- La captura y la descripción del juego se leen **antes** que las portadas vecinas, para que aparezcan enseguida.
- En el panel del último juego del menú principal, **A abre la descripción** y P juega directamente.
- **Traducciones fuera del programa**: el español y el inglés pasaron a ser archivos en el disco del menú, leídos solo cuando se usan. El programa quedó más pequeño y sobró memoria.
- **Opciones más rápidas**: moverse entre los elementos y cambiar valores ya no redibuja la pantalla entera.
- **Porcentaje dentro de todas las barras de progreso.**
- Al terminar una grabación, la pantalla muestra el **tamaño y el tiempo** ("6 minutos y 11 segundos").
- Prueba del control: la barra de salida toma el color del mando que mantiene los botones.
- La copia de la configuración lista lo que se va a guardar: configuración, recientes, favoritos y estadísticas.
- El protector de pantalla ya no entra justo después de una operación larga.
- La portada del último juego ya no desaparece al cambiar de vista.

**Fondos, herramientas aparte y memoria**
- **9 fondos de pantalla** (Predeterminado, Fibra de carbono, Acero cepillado, Panal, Rayas, Rejilla, Chapa, Viñeta, Puntos).
- **Herramientas en un módulo separado**, cargado solo cuando se abre una de ellas: el menú quedó más ligero.
- **Memoria de portadas por vista**: la cuadrícula de Portadas guarda muchas portadas pequeñas; las demás vistas, portadas grandes.
- **Protector de pantalla** con el logo de 3DO y las consolas paseando por la pantalla.
- La música vuelve a sonar en consolas con poca memoria libre.
- Pantalla de éxito de la actualización del firmware con la foto de la consola y el aviso de apagar y encender.
- *Acerca de* muestra el firmware y la versión de la ODE; *Información de la consola* muestra la música y las portadas en memoria.
- El acordeón de Apariencia se abre siempre cerrado.
- El reloj se consulta cada 5 segundos, dejando el menú más suelto.

**Opciones nuevas y sonido**
- **Apariencia en acordeón**: Menú principal, Juegos, Medios y Pantalla, un grupo abierto cada vez, con animación.
- **Ordenar por** nombre, año, género, desarrollador o más jugados.
- **Recordar la posición**, **Artículo delante**, **Pantalla al encender** y **Protector de pantalla**.
- **Copia y restauración de la configuración**, los favoritos, los recientes y las estadísticas, y **Restaurar los valores predeterminados**.
- **Reproductor de música propio**, con **volumen en barra** que cambia al instante, y la opción **Aleatoria**.

### 0.8 — Tarjeta del juego, firmware de fábrica, reloj y medios

**Tarjeta del juego y ajustes**
- **Tarjeta del juego al iniciar**: portada, nombre en amarillo, género, año y país en azul, "jugado N veces" y "N discos añadidos a la cola".
- **Velocidad del nombre** en 5 niveles.
- Portada del último juego corregida en la cuadrícula de Portadas; ajustes en las líneas de la lista.
- Los juegos vuelven a abrirse con el firmware de fábrica después de navegar por carpetas.

**Firmware de fábrica y reloj**
- **Compatibilidad completa con el firmware de fábrica**: el menú ya no usa comandos que este no tiene, y la grabación en el USB ganó reintentos.
- **Funciones por versión del firmware**: cada opción solo aparece si el firmware instalado la tiene.
- **Aviso de reloj sin hora** (pila baja), sin bloquear el menú, con atajo para ajustarla.
- Al ajustar el reloj, el año ya empieza en el año actual.
- Entrar y salir del panel del último juego pasó a ser instantáneo.
- En la ODE del puerto de expansión, los textos dicen **SD** cuando el medio es una tarjeta microSD.
- Medición de los tiempos de arranque.

**Lista, estadísticas y sonidos**
- **Vídeo en la lista**: la vista previa se reproduce en la caja junto a la lista.
- **Efecto de la estrella** al marcar y desmarcar favorito, con sonido propio.
- **Estadísticas en ranking**, con la cantidad de partidas de cada juego.
- Sonidos guardados en el disco del menú.
- **Leer el USB de nuevo** en vivo y opciones grabadas al instante.
- Página de **Agradecimientos** con desplazamiento.
- Entrada "Último" arriba en la lista de juegos.
- Lectura de la lista hecha una sola vez y diagnóstico completo.
- Lista corregida en la ODE del puerto de expansión.

**Medios en dos tamaños**
- **Portadas y capturas en dos tamaños**: pequeñas para las cuadrículas, grandes para el destacado y la pantalla completa.
- Portadas leídas con menos comandos; cuadrícula de Portadas con 3 páginas en memoria.
- Vídeo en varios tamaños, con imagen fija cuando el vídeo es pesado.
- **Formatos por idioma** (fecha, hora, temperatura, números).
- **Gestor de almacenamiento** y pantalla de **Fecha y hora**.

### 0.7 — Vídeo y sonido
- **Vídeo en Cinepak** con decodificador propio: en la descripción, a pantalla completa (X) y después en la lista.
- **Efectos de sonido y música de fondo**, con 10 pistas.
- Botones definitivos de la pantalla de descripción.

### 0.6 — Aspecto nuevo y herramientas
- **Aspecto nuevo**: franjas finas en todas las pantallas, un brillo que pasa por la caja seleccionada del menú principal.
- **Prueba del control** con la foto del mando, para hasta 8 mandos.
- **Ajuste de imagen**.
- **Lista guardada** (*Leer al encender*) para arrancar más rápido.
- **Idioma cambiado al instante** (Português, Español, English).
- Imágenes del menú fuera del programa, en el disco.
- **Prueba del ODE y del USB**.
- Páginas de información separadas: consola, ODE y USB.
- Ventana de "juego iniciando".

### 0.5 — Jugar con cualquier firmware
- Lanzamiento de juegos corregido en los dos firmwares y en las dos placas.
- **Multidisco**: todos los discos entran en la cola al jugar.
- Menos memoria usada; lista sin fallos en colecciones grandes.

### 0.4 — Opciones, descripción y partidas
- **Opciones grabadas en el USB** (`.config/3doconfig.ode`).
- **Pantalla de descripción del juego**: portada, captura, datos y el texto con desplazamiento.
- **Favoritos, Recientes y Estadísticas**, con fecha y hora.
- **Filtro** por género y país.
- **Almacenamiento**: gestor de partidas, copia, restauración y diagnóstico de la NVRAM.
- **Extracción de las ROM y de la RAM** de la consola.
- **Copia y actualización del firmware** desde el menú.
- Letras en mayúsculas, minúsculas o primera mayúscula.

### 0.3 — Pantalla principal e identidad
- **Menú principal** con las cajas Favoritos, Juegos, Estadísticas, Recientes y Opciones.
- **Panel del último juego.**
- **Detección de la consola por la BIOS**, con la foto del aparato arriba.
- **Reloj, fecha y temperatura** en pantalla.
- **Una portada por juego**, y los textos de todos los juegos en un solo archivo, leído una vez.
- Recuento de discos, región sacada del nombre del archivo, franja translúcida con los discos en la portada.
- Icono de CD en lugar de la portada que falta.

### 0.2 — Reescrito desde cero

El 10 de noviembre de 2026 el menú fue **reescrito desde cero**, con código nuevo, más rápido y más sencillo de mantener.
- **Lista alfabética** con la portada al lado, memoria de portadas y lectura anticipada.
- **Cuatro vistas**: Lista, Portadas, Carrusel y Carrusel FX (en perspectiva, con reflejo).
- **NTSC y PAL** automáticos.
- **Un único `boot.iso`** para la ODE interna y la del puerto de expansión.
- Juegos en subcarpetas (hasta 3 niveles) en una sola lista.
- Salto por letra, desplazamiento del nombre largo, aceleración al mantener la cruceta.

### 0.1 — Primera generación

Del 10 de octubre al 9 de noviembre de 2026.

- **Última etapa** — pestañas cambiadas con L / R; 4 modos de vista; pantalla de detalles rediseñada; Herramientas y Opciones reorganizadas; **copia del firmware** desde la consola; extracciones en la carpeta `roms/` y la NVRAM en `saves/`; protector de pantalla con el logo y las consolas de 3DO; 10 pistas de música.
- Lectura por ruta, orden alfabético garantizado, descripción instantánea, vista previa pequeña más suave, "Limpiar" en Recientes.
- Carpetas por letra unidas en una lista única; base estable.
- Detección del firmware en tiempo real, cuadrícula de Portadas con el motor gráfico de la consola, cambio de género más rápido, vista previa en vídeo, actualización de firmware.
- Menú base: lista alfabética, favoritos y recientes, filtro por género, memoria de portadas, multidisco, capturas a pantalla completa, configuración guardada en el USB.

---

## Firmware TADEU

### 1.0.5
- **Reloj de tiempo real (DS3231)**: fecha, hora, temperatura y estado de la pila.
- **Archivos grabados con la fecha y la hora** correctas.
- Ajuste del reloj desde la consola.

### 1.0.4
- **Espacio del USB**: tamaño total y espacio libre informados al menú.

### 1.0.3
- **Una sola base de código para las dos placas** (la original y la clon con un Pico común), elegida al compilar.

### 1.0.2
- **Marcador de versión** dentro del firmware, que el menú lee y muestra.

### 1.0 y 1.0.1
- **Lista rápida por extensión**: los juegos se reconocen por `.cue` e `.iso` sin abrir cada archivo. Lanzar un juego del final del USB bajó de unos 30 s a entre 2 y 4 s.
- **Paginación incremental** de la lista.
- **Creación de carpetas** desde la consola.
- **Copia del firmware** desde la consola, verificada byte a byte.
- **Actualización desde el menú**, con zona de espera, comprobación por CRC y verificación de cada bloque grabado. El firmware en uso nunca se sobrescribe antes de la comprobación.
- **Actualización a prueba de fallos al encender**: comprueba antes y después de copiar; si algo falla, entra en modo de recuperación en vez de arrancar roto.
- **Número de serie del chip.**
- Apertura de archivos corregida: leer un archivo que no existe ya no crea un archivo vacío.
- Mapa de la memoria flash ajustado para chips de 2 MB.
- Recuperación siempre posible por BOOTSEL.

---

## Generador (`generate_usb.py`)

### Noviembre de 2026
- **Editor** (`Publisher=`) en los textos de los juegos, en portugués, español e inglés.
- Valores predeterminados de los vídeos: 20 segundos, 15 fotogramas por segundo.
- **Vídeos en Cinepak** (`.cvd`), en 5 tamaños, con fotogramas por segundo, duración y calidad a elegir.
- **Conversión de vídeo más rápida**, con un vídeo por núcleo del PC al mismo tiempo.
- **Portadas y capturas en dos tamaños** cada una.
- Preguntas separadas para portadas, capturas y vídeos, cada una con "solo las que faltan".
- Aprovecha un USB generado por versiones antiguas, sin necesitar las imágenes originales.
- Crea el archivo de opciones del menú solo con el idioma, si aún no existe.
- Código antiguo eliminado: quedó un solo archivo, más pequeño y más sencillo.
- Respuestas del asistente guardadas en `generate_usb.ini`.

### Octubre de 2026
- Asistente paso a paso en 3 idiomas.
- Descarga de las portadas y capturas que faltan.
- Textos de los juegos (año, género, desarrollador, descripción).
- Conversión de `.chd` e `.iso` a `.bin/.cue`.
- Renombrado de discos con nombre genérico y organización en carpetas.
- Copia del `boot.iso` y preparación del firmware.
