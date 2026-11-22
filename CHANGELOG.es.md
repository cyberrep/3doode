# 📝 Historial de versiones

[← Volver al inicio](README.es.md) · [English](CHANGELOG.md) · [Português](CHANGELOG.pt.md) · **Español**

Todo lo que cambió en el **menú** (`boot.iso`), en el **firmware TADEU** y en el **generador** (`generate_usb.py`), de la versión más nueva a la más antigua.

- [Menu — 1.4](#menu--14)
- [Menu — 1.3](#menu--13)
- [Menu — 1.2](#menu--12)
- [Menu — 1.1](#menu--11)
- [Menu — 1.0](#menu--10)
- [Menú — antes de la 1.0 (versiones 0.x)](#menú--antes-de-la-10-versiones-0x)
- [Firmware TADEU](#firmware-tadeu)
- [Generador (generate_usb.py)](#generador-generate_usbpy)

---

## Menu — 1.4

**Lista de juegos**
- **El primer juego de la tarjeta ya no desaparece en el Xport con FAT32.** En tarjetas con una carpeta por letra, el juego de la primera carpeta (ej.: `#/3D Pinball…`) quedaba fuera de la lista.
- **Un juego sin descripción usa la del mismo juego de otra región.** "Battle Blues (Korea)" muestra el desarrollador, el género, el año y la descripción de "Battle Blues (USA)" cuando solo uno de ellos tiene texto.
- El aviso **NO SE PUDO INICIAR** muestra el código de error entero (antes solo el último dígito).

**Portadas**
- 🖼️ **Nueva opción Opciones → Apariencia → Formato de las portadas.** Las long box y las cajas de CD ya no se estiran:
  - **Original** (predeterminado): la portada aparece en su proporción, con el marco alrededor.
  - **Ambilight**: la portada en el centro, con un brillo en los colores de la propia portada llenando el resto.
  - **Fondo negro**: la portada en el centro, con el resto en negro.
  - **Estirada**: como era antes.
- Vale en todas las pantallas: Lista, Portadas, Carrusel, Carrusel FX, Vitrina, Tira, Descripción y la portada pequeña de la pantalla de inicio.
- En la **Lista**, la portada siempre empieza a la altura de la primera línea de juegos, y la línea dorada y las partidas quedan pegadas debajo de ella.
- Las portadas hay que **grabarlas de nuevo** (la página lo hace sola); las antiguas siguen funcionando, estiradas como antes.

**Opciones y Herramientas**
- El informe de **Probar el ODE y el USB** (`3dodiag.txt`) ahora trae también el registro de la lectura del USB: un solo archivo para enviar cuando algo falle.
- Se tradujeron cinco textos que aparecían en portugués en español e inglés (Leer el USB de nuevo, copia de las partidas y el aviso de herramienta ausente).

**Página web**
- ✨ **Imágenes más nítidas y limpias.** Las portadas y las capturas ahora se reducen con la media de toda el área de la imagen original, con nitidez leve y sin tramado: desaparecen el dentado, el granulado y el contorno blanco alrededor de las letras y de los personajes.
- **Portadas en su proporción real** (long box y caja de CD), listas para el Formato de las portadas.
- **Las portadas y capturas antiguas de la tarjeta se sustituyen por las nuevas** en la primera grabación, incluso con "Mantener" elegido. Solo queda la antigua que no tiene de dónde rehacerse.
- **Resumen antes de grabar**: la pantalla Grabar en la tarjeta muestra lo que se grabará, lo que ya está en la tarjeta y el total de archivos.
- **Portada de la región correcta** en tus propias imágenes: "Cannon Fodder (USA)" ya no toma la portada de "(Europe)". Sin la de la región, el orden es USA, Europe, Japan.
- Las imágenes en subcarpetas de nombre desconocido (como `cover3d`) ya no entran como portadas.
- Al grabar aparece un botón a la vez: Empezar parado, Parar grabando.

---

## Menu — 1.3

**Lista de juegos**
- 🏷️ **Nueva opción Opciones → Juegos → Nombre de los juegos: Título o Archivo.** Con **Archivo** aparece el nombre del archivo sin la extensión (ej.: `Doom (USA)`); con **Título**, el nombre limpio de siempre (`Doom`).
- **Un juego guardado como `.cue` + `.iso` con el mismo nombre aparece una sola vez** (antes salía dos veces). Si usas la lista guardada, haz **Leer el USB de nuevo** una vez.
- **Favoritos y Recientes vacíos**: mensajes nuevos y la ventana se cierra con el primer botón.

**Ventanas de aviso y confirmación (pop-up estándar)**
- 🪟 **Todas las confirmaciones y avisos usan ahora la misma ventana**, en el menú y en las Herramientas: título en amarillo, línea dorada, texto y una franja abajo con los botones (Ⓐ SÍ / Ⓑ NO, Ⓑ VOLVER, Ⓑ CANCELAR). Antes varias se abrían a pantalla completa.
- **Una sola ventana de principio a fin.** En copia de seguridad, restauración, extracción y grabación de firmware, la misma ventana muestra la pregunta, el progreso y el resultado.
- **RESUMEN dentro de la ventana** al terminar: "Grabado con éxito", tamaño y tiempo; en el gestor de partidas, el recuento de copiados, iguales y errores.
- Borrar recientes y borrar estadísticas preguntan en la ventana, con la descripción de lo que se borrará.

**Progreso de las grabaciones**
- 📊 **Nuevo progreso "GRABANDO"**: muestra qué se está grabando (ROM del sistema, firmware, NVRAM…), el **nombre del archivo**, la barra con el porcentaje y la **velocidad en KB/s**.
- **Ⓑ cancela la copia y la grabación del firmware.** En la grabación, la cancelación ocurre antes de aplicar: el firmware actual continúa.
- Grabar el firmware pide **una sola confirmación** (eran dos).
- Al terminar de grabar el firmware: "El ODE está reiniciando la 3DO. Si no vuelve, apague y encienda."

**Opciones y Herramientas**
- **Leer el USB de nuevo ocurre dentro de la ventana**, con el recuento de juegos y la barra, sin cambiar a la pantalla de inicio.
- Flechas de desplazamiento de verdad en las pantallas de información (antes eran las letras `^` y `v`).
- Restaurar la copia de las opciones: texto más directo ("Todos los elementos se restaurarán del USB.").
- La ventana **INICIANDO EL JUEGO** tiene ahora el título en amarillo, como las demás.

**Página web**
- Nuevas opciones **Mostrar juegos (Lista / Carpetas)** y **Nombre de los juegos (Título / Archivo)**.
- Al preparar la tarjeta, **crea las carpetas `.config`, `saves`, `firmware` y `roms`**, para que el menú lo encuentre todo en su sitio.
- La elección del firmware pasa a ser **DIR-HIGH** o **DIR-LOW**, con la explicación de cuál corresponde a cada placa.

---

## Menu — 1.2

**Navegación por carpetas**
- 📁 **Nueva opción Opciones → Apariencia → Mostrar juegos: Lista o Carpetas.** En el modo **Carpetas**, las carpetas de la tarjeta se vuelven elementos en los que **entras** (A) y **vuelves** (B). Una carpeta con 2 juegos o más se vuelve carpeta; **una carpeta con un solo juego se vuelve ese juego**. Las carpetas de sistema (carátulas, vídeos, saves, roms…) siguen ignoradas.
- 🎨 **Las carpetas tienen la cara del menú**: ícono de carpeta amarillo con la **letra grande en el medio**, con forma de carátula en los modos grandes (Carátulas, Carrusel, Vitrina, Tira). La carpeta queda **transparente**, sin marco — solo la seleccionada se resalta.
- Mensaje de **"ningún juego encontrado"** más claro (en los 3 idiomas), avisando de los nombres de carpeta reservados.

**Gestor de saves**
- 🌎 **Traducido por completo** (español e inglés): faltaban pantallas que estaban solo en portugués.

**Correcciones**
- La lista de carpetas aparece **al instante**, sin tener que releer el USB.
- Corregido un cambio de colores en los bordes de las carátulas (aparecían rojos donde debían ser azules) en algunos modos.

---

## Menu — 1.1

**Gestor de partidas**
- 🎮 **Muestra de qué juego es cada partida.** Una franja debajo de la lista trae el nombre del juego de la partida seleccionada (ej.: `alone1.save` → Alone in the Dark). La tabla tiene 240 nombres, no distingue mayúsculas de minúsculas y reconoce partidas numeradas (`TE_Devils_1`, `EA_RR3`...). La partida que no está en la tabla aparece con el nombre del archivo.
- **Copiar con el nombre del juego o con el nombre original**: al copiar al USB el menú pregunta. Con el nombre del juego el archivo queda `Juego (nombre de la partida).sav`. **Al volver a la consola la partida siempre recibe el nombre original**, que es el que el juego busca.
- **Tabla de nombres actualizable sin cambiar el menú**: la página web graba la tabla en `.config/3dogamessaves.ode`. Sin ese archivo, el menú usa la tabla que trae dentro. Se puede crear el archivo a mano solo con correcciones (`=nombre<TAB>juego` o `*prefijo<TAB>juego`).
- **Mucho más rápido al navegar**: el fondo de la pantalla ya no se redibuja en cada movimiento.
- **Pantallas uniformes**: título, franja dorada y textos. El **RESUMEN** de copiar y restaurar muestra un conteo por línea, en colores (verde copiadas/restauradas, amarillo iguales, rojo errores), e indica el motivo del último error.
- **Lista del USB en orden alfabético.**
- **Las partidas copiadas a la carpeta `saves/` desde el ordenador** pasan a aparecer y restaurarse después de preparar la tarjeta en la página web (registra cada archivo en el catálogo `saves/3dosaves.ode`). Una línea del catálogo sin CRC se restaura sin comprobación; con CRC, el archivo alterado sigue siendo rechazado.
- Las copias hechas con la 1.0 siguen restaurándose.

**Vitrina y Tira**
- ⚡ **Vitrina y Tira mucho más rápidas al navegar.** En la 1.0, en cada cambio de juego el menú esperaba y leía de nuevo el archivo de textos, incluso para un juego que acababa de mostrar; en listas grandes la descripción tardaba cerca de 1 segundo.
- **Descripción al instante al volver o avanzar**: las últimas 8 descripciones quedan en memoria, así que ir y volver entre juegos vecinos ya no lee la tarjeta.
- **Lectura adelantada de los vecinos**: con el mando quieto y las portadas ya en pantalla, el menú lee las descripciones de los 2 juegos de cada lado y del destino del salto de letra (anterior y siguiente). La lectura se detiene en cuanto se mueve el mando, así que no retrasa las portadas ni la navegación.

**Opciones**
- El menú guarda en las opciones **qué ODE detectó** (firmware, tipo y si hay reloj). La página web lo lee y ya marca las opciones correctas.

**Página web**
- **Marca sola el ODE, el firmware TADEU y el reloj** a partir de lo que el menú detectó.
- **Graba la tabla de nombres de las partidas** en la tarjeta.
- **Registra las partidas de la carpeta `saves/`** en el catálogo y corrige tamaño y CRC de líneas antiguas.
- Corrección: con **Mantener** marcado, tus portadas, capturas y vídeos que ya están en la tarjeta no se copian de nuevo.

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

### 1.0.6
- 🕒 **El reloj se protege solo.** Al encender, el firmware busca el chip del reloj (DS3231). Si la placa no lo tiene, los dos pines del reloj se liberan y las funciones de fecha y hora quedan desactivadas, en vez de estorbar al resto.
- 📦 **Dos archivos, uno para cada tipo de placa: `TADEU_1.0.6_DIR-HIGH` y `TADEU_1.0.6_DIR-LOW`.**

**¿Qué archivo usar: DIR-HIGH o DIR-LOW?**

Las placas del ODE tienen un chip que controla el sentido de los datos entre el ODE y la consola. Hay dos modelos de ese chip, y funcionan con la señal de dirección invertida uno respecto al otro. El firmware tiene que ser el de tu placa.

- **`TADEU_1.0.6_DIR-LOW`**: placa original Waveshare (chip 74HC245).
- **`TADEU_1.0.6_DIR-HIGH`**: placas clon, como tzmwx y TaiHu (chip 74LVC4245).

**Si grabas el equivocado:** la consola muestra el logo de 3DO y luego la pantalla queda negra. No se daña nada: pon el Pico en modo BOOTSEL (mantén el botón al conectarlo al ordenador) y graba el otro archivo.

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

### Noviembre de 2026 (menú 1.4)
- ✨ **Imágenes más nítidas y limpias**: reducción con la media del área, nitidez leve y sin tramado, igual que la página web. Los "preparados" antiguos (texto, nítida, suave…) dejaron de existir.
- **Portadas en su proporción real** (long box ≈ 76x140, caja de CD ≈ 100x87), sin estirar.
- **Las portadas y capturas antiguas se rehacen solas** en la primera ejecución (`generate_usb.py` y `converter_tudo.py`).

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
