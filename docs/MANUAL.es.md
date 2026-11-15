# 🛠️ Generador de USB / SD — Manual

[← Volver al inicio](../README.es.md) · [English](MANUAL.md) · [Português](MANUAL.pt.md) · **Español**

`generate_usb.py` prepara tu USB (o tarjeta) de la 3DO ODE **solo**. Descargas **solo este archivo** y él hace el resto:

- genera las **portadas** y las **capturas** de los juegos, cada una en dos tamaños;
- convierte las **vistas previas en vídeo** a Cinepak;
- arma los **textos de los juegos** (año, género, desarrollador, editor, descripción);
- convierte `.chd` e `.iso` a `.bin/.cue`, renombra y organiza los juegos;
- **copia el menú (`boot.iso`)** al USB;
- crea el archivo de opciones del menú ya en tu idioma;
- puede **descargar y preparar el firmware** de tu placa.

**Nunca borra** tus archivos.

---

## ✅ Instalación (Windows 10 y 11)

Abre **PowerShell** o el **Símbolo del sistema** y pega los comandos, uno cada vez.

**1. Python**

```
winget install -e --id Python.Python.3.12
```

**2. FFmpeg** (solo si vas a convertir vídeos)

```
winget install -e --id Gyan.FFmpeg
```

**3. Cierra PowerShell y ábrelo de nuevo**, para que vea los programas instalados.

**4. Comprueba**

```
py --version
ffmpeg -version
```

Si los dos responden con la versión, está listo.

**No hace falta instalar las bibliotecas de Python.** La primera vez, el propio `generate_usb.py` instala Pillow y NumPy solo (y `pip`, si tu Python vino sin él). Solo si eso falla, por ejemplo sin internet, ejecuta a mano:

```
py -m pip install pillow numpy
```

Para juegos en `.chd` hace falta además **chdman** (viene con MAME): deja `chdman.exe` en la misma carpeta que `generate_usb.py`.

En **Linux** y **macOS**, instala `python3` y `ffmpeg` y ejecuta `python3 -m pip install pillow numpy`.

## 🚀 La forma fácil (asistente)

Ejecútalo sin opciones:

```
py generate_usb.py
```

La **primera pregunta es el idioma** (Português, English, Español). Después vienen los pasos:

1. **Carpetas** — dónde están **tus juegos** (el USB o una carpeta del PC) y tu carpeta de **medios** (portadas, capturas, vídeos y textos).
2. **Ordenar los juegos** — convertir `.chd → .bin/.cue` (sin pérdida) e `.iso → .bin/.cue`, renombrar nombres genéricos (`disc.iso`…), sacar los juegos de carpetas con un solo juego, y **organizar**: como está, todo en la raíz o en carpetas por letra.
3. **Portadas, capturas y textos** — tres preguntas separadas, cada una con la opción **"solo las que faltan"**. El generador usa tus imágenes y **descarga** las que no encuentre.
4. **Vídeos** — convierte los vídeos de la carpeta `videos/` a Cinepak, con el tamaño, la duración y la calidad que elijas.
5. **Extras** — el informe `cover.txt`, o solo simular (muestra lo que haría, sin grabar nada).
6. **Menú** — copia el **`boot.iso`** a la raíz del USB.

Al final muestra el **comando equivalente**, para repetirlo sin preguntas la próxima vez, y lo ejecuta. Las respuestas quedan guardadas en `generate_usb.ini`, junto al programa.

### Firmware (opcional)

El generador también prepara el **firmware TADEU**: dices cuál es tu placa y él descarga el archivo correcto y lo deja en `firmware/` en el USB, listo para *Opciones → Dispositivo ODE → Actualizar firmware*. Si tu ODE aún está con el firmware de fábrica, la primera instalación es por BOOTSEL: mantén el botón, conecta el Pico al PC y arrastra el `.uf2`.

---

## ⚙️ Línea de comandos

```
py generate_usb.py "<carpeta de los juegos>" [opciones]
```

Los nombres de las opciones están en portugués; son los mismos en todos los idiomas.

### General

| Opción | Qué hace |
|---|---|
| `--teste` | Solo simula: muestra lo que haría, sin grabar. |
| `--forcar` | Rehace todo, incluso lo que ya existe. |
| `--offline` | No descarga nada de internet. |
| `--idioma pt\|en\|es` | Idioma de los textos de los juegos. |
| `--midias "<carpeta>"` | Carpeta de los medios, cuando está separada de los juegos. |
| `--relatorio` | Genera el informe `cover.txt`. |
| `--copiar-boot` | Copia el `boot.iso` a la raíz del USB (lo busca junto al programa y, si no está, lo descarga). |
| `--firmware` | Abre directamente el preparador de firmware. |

### Portadas, capturas y textos

| Opción | Qué hace |
|---|---|
| `--pular-capas` / `--capas-faltantes` / `--refazer-capas` | Sin portadas / solo las que faltan / rehace todas. |
| `--pular-telas` / `--telas-faltantes` / `--refazer-telas` | Lo mismo, para las capturas. |
| `--capa-preparo texto\|nitida\|suave\|sempontos\|corfiel` | El tratamiento de la imagen de la portada. El predeterminado es `texto`. Cambiarlo rehace todas las portadas. |
| `--baixar-tudo` | Descarga de nuevo las imágenes, incluso las que ya tienes. |
| `--somente-lista` | Genera solo los textos de los juegos, sin portadas, capturas ni vídeos. |
| `--pular-gamelist` | No toca los textos de los juegos. |

### Vídeos

| Opción | Qué hace |
|---|---|
| `--tamanho mini\|box\|small\|medium\|large` | 80×60 · 128×96 · 160×120 (predeterminado) · 240×180 · 320×240. |
| `--video-fps N` | Fotogramas por segundo. Predeterminado 15. |
| `--video-seg N` | Duración en segundos. Predeterminado 20. |
| `--video-q N` | Calidad, de 1 (mejor, archivo más grande) a 31. Predeterminado 4. |
| `--video-faltantes` / `--refazer-videos` | Solo los que faltan / rehace todos. |
| `--so-video` | Hace solo los vídeos. |
| `--sem-video` | Omite los vídeos. |

### Juegos

| Opción | Qué hace |
|---|---|
| `--iso2bin` / `--apagar-iso` | Convierte `.iso → .bin/.cue` / borra el `.iso` después de convertir. |
| `--sem-chd` / `--apagar-chd` | No convierte los `.chd` / borra el `.chd` después de convertir. |
| `--nao-renomear` / `--identificar-tudo` | No renombra / comprueba cada juego por la firma del disco. |
| `--somente-renomear` | Solo renombra los juegos, sin generar nada. |
| `--nao-achatar` | Mantiene las carpetas que tienen un solo juego. |
| `--organizar letra\|raiz` | Mueve los juegos a carpetas A…Z, o los trae todos a la raíz. |

---

## 📦 Qué graba en el USB

Siempre en la **raíz** del USB, con el mismo nombre que el archivo del juego (en juegos de varios discos, el nombre del disco 1):

| Dónde | Qué es |
|---|---|
| `covers/small/<juego>.cel` | Portada 56 × 78, para la cuadrícula de Portadas y el menú principal. |
| `covers/large/<juego>.cel` | Portada 100 × 140, para las demás vistas y la descripción. |
| `screenshots/medium/<juego>.cel` | Captura de hasta 120 × 90. |
| `screenshots/large/<juego>.cel` | Captura de hasta 304 × 228, para la pantalla completa. |
| `videos/<juego>.cvd` | Vista previa en vídeo, en Cinepak, sin sonido. |
| `.config/3dogamesdetails.ode` | Año, género, desarrollador, editor y descripción de todos los juegos. |
| `.config/3doconfig.ode` | Opciones del menú. Solo se crea si aún no existe, con el idioma elegido. |
| `boot.iso` | El menú (si lo pides). |

El generador **no toca** tus favoritos, recientes ni estadísticas.

### De dónde vienen las imágenes y los textos

- **Imágenes**: primero las tuyas, en las carpetas `cover/` y `screenshot/` de los medios. Lo que falte se descarga y se guarda ahí, para que funcione sin internet la próxima vez.
- **Textos**: de `gamelist.pt.txt`, `gamelist.es.txt` o `gamelist.en.txt`, según el idioma elegido. Cada juego trae año, desarrollador, editor, género y descripción.
- **Vídeos**: los de este repositorio ya vienen convertidos (20 segundos, 15 fotogramas por segundo) y solo se copian. Para convertir los tuyos, pon los vídeos de origen en la carpeta `videos/` (mp4, avi, mkv…) y elige el tamaño, los fotogramas por segundo y la duración.

### Cómo se asocia un juego con su portada y sus textos

Solo cuenta el título: lo que está entre `( )` o `[ ]` en el nombre del archivo se ignora, igual que los acentos, las mayúsculas y la puntuación. `Alone in the Dark (USA).iso`, `Alone in the Dark (U).iso` y `Alone in the Dark (English) [!].cue` encuentran la misma portada, captura, vídeo y textos.

---

## 💡 Consejos

- **¿Vídeo lento de convertir?** Usa `--tamanho small`, menos segundos y `--video-faltantes`.
- **¿USB lento en la consola?** Prefiere vídeos más pequeños (`mini`, `box` o `small`).
- **Formatos de juego**: la ODE lee `.iso` y `.cue` + `.bin`. Otros formatos hay que convertirlos antes en el PC.
- **¿No aparecen las portadas?** Comprueba que el nombre del archivo de la portada sea igual al nombre del archivo del juego.
