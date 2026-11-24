# 🛠️ USB / SD Generator — Manual

[← Back to start](../README.md) · **English** · [Português](MANUAL.pt.md) · [Español](MANUAL.es.md)

> 🌐 **Most people do not need this generator.** The easiest way is the [web page](https://cyberrep.github.io/3doode/), which prepares the card in the browser with nothing to install: see the **[page manual](SITE.md)**. Use the generator to convert games (`.chd`, `.iso`), convert your own videos, or if your browser is Firefox or Safari.

`generate_usb.py` prepares your 3DO ODE USB (or card) **by itself**. You download **only this file** and it does the rest:

- builds the **covers** and **screenshots** of the games, each in two sizes;
- converts the **video previews** to Cinepak;
- builds the **game texts** (year, genre, developer, publisher, description);
- converts `.chd` and `.iso` to `.bin/.cue`, renames and organizes the games;
- **copies the menu (`boot.iso`)** to the USB;
- creates the menu options file already in your language;
- can **download and prepare the firmware** for your board.

It **never deletes** your files.

---

## ✅ Installation (Windows 10 and 11)

Open **PowerShell** or the **Command Prompt** and paste the commands, one at a time.

**1. Python**

```
winget install -e --id Python.Python.3.12
```

**2. FFmpeg** (only if you are going to convert videos)

```
winget install -e --id Gyan.FFmpeg
```

**3. Close PowerShell and open it again**, so it can see the installed programs.

**4. Check**

```
py --version
ffmpeg -version
```

If both answer with a version, you are ready.

**You do not need to install the Python libraries.** The first time, `generate_usb.py` installs Pillow and NumPy by itself (and `pip`, if your Python came without it). Only if that fails, for example without internet, run by hand:

```
py -m pip install pillow numpy
```

For `.chd` games you also need **chdman** (it comes with MAME): leave `chdman.exe` in the same folder as `generate_usb.py`.

On **Linux** and **macOS**, install `python3` and `ffmpeg` and run `python3 -m pip install pillow numpy`.

## 🚀 The easy way (wizard)

Run it with no options:

```
py generate_usb.py
```

The **first question is the language** (Português, English, Español). Then come the steps:

1. **Folders** — where **your games** are (the USB or a folder on the PC) and your **media** folder (covers, screenshots, videos and texts).
2. **Tidy up the games** — convert `.chd → .bin/.cue` (lossless) and `.iso → .bin/.cue`, rename generic names (`disc.iso`…), take games out of folders that hold a single game, and **organize**: as it is, everything in the root or in folders by letter.
3. **Covers, screenshots and texts** — three separate questions, each with the **"only the missing ones"** option. The generator uses your images and **downloads** the ones it cannot find.
4. **Videos** — converts the videos in the `videos/` folder to Cinepak, in the size, length and quality you choose.
5. **Extras** — the `cover.txt` report, or just simulate (shows what it would do, without writing anything).
6. **Menu** — copies **`boot.iso`** to the root of the USB.

At the end it shows the **equivalent command**, so you can repeat it without questions next time, and runs. The answers are kept in `generate_usb.ini`, next to the program.

### Firmware (optional)

The generator also prepares the **TADEU firmware**: you say which board you have and it downloads the right file and leaves it in `firmware/` on the USB, ready for *Options → ODE Device → Update firmware*. If your ODE is still on the factory firmware, the first installation is through BOOTSEL: hold the button, plug the Pico into the PC and drag the `.uf2`.

> ⚠️ **Before installing TADEU for the first time, back up your board's original firmware** (`picotool save -a firmware_original.uf2`). The step by step, with Zadig on Windows, is in the [README](../README.en.md). TADEU has not been tested yet on the FZ-10 dual boards, nor on GoldStar and Sanyo.

The generator downloads **TADEU 1.0.7** for your board (**DIR-LOW**: original Waveshare; **DIR-HIGH**: tzmwx and TaiHu clones), writes the version next to it, which the menu shows before updating, and records the board in the card's options file.

---

## ⚙️ Command line

```
py generate_usb.py "<games folder>" [options]
```

The option names are in Portuguese; they are the same in every language.

### General

| Option | What it does |
|---|---|
| `--teste` | Only simulates: shows what it would do, without writing. |
| `--forcar` | Redoes everything, even what already exists. |
| `--offline` | Downloads nothing from the internet. |
| `--idioma pt\|en\|es` | Language of the game texts. |
| `--midias "<folder>"` | Media folder, when it is separate from the games. |
| `--relatorio` | Creates the `cover.txt` report. |
| `--copiar-boot` | Copies `boot.iso` to the root of the USB (looks next to the program and, if it is not there, downloads it). |
| `--firmware` | Opens the firmware preparer directly. |

### Covers, screenshots and texts

| Option | What it does |
|---|---|
| `--pular-capas` / `--capas-faltantes` / `--refazer-capas` | No covers / only the missing ones / redo all. |
| `--pular-telas` / `--telas-faltantes` / `--refazer-telas` | The same, for the screenshots. |
| `--capa-preparo texto\|nitida\|suave\|sempontos\|corfiel` | How the cover image is treated. The default is `texto`. Changing it redoes all covers. |
| `--baixar-tudo` | Downloads the images again, even the ones you already have. |
| `--somente-lista` | Builds only the game texts, without covers, screenshots or videos. |
| `--pular-gamelist` | Leaves the game texts alone. |
| `--pak` / `--sem-pak` | Builds the cover and screenshot packs (`covers/small.pak`, `covers/large.pak`, `screenshots/medium.pak`) from what is on the card / deletes the packs. For menu 1.6 with the TADEU 1.0.7 firmware: the menu goes straight to the image inside the pack. The loose files stay on the card. |

### Videos

| Option | What it does |
|---|---|
| `--tamanho mini\|box\|small\|medium\|large` | 80×60 · 128×96 · 160×120 (default) · 240×180 · 320×240. |
| `--video-fps N` | Frames per second. Default 15. |
| `--video-seg N` | Length in seconds. Default 20. |
| `--video-q N` | Quality, from 1 (best, bigger file) to 31. Default 4. |
| `--video-faltantes` / `--refazer-videos` | Only the missing ones / redo all. |
| `--so-video` | Does only the videos. |
| `--sem-video` | Skips the videos. |

### Games

| Option | What it does |
|---|---|
| `--iso2bin` / `--apagar-iso` | Converts `.iso → .bin/.cue` / deletes the `.iso` after converting. |
| `--sem-chd` / `--apagar-chd` | Does not convert `.chd` / deletes the `.chd` after converting. |
| `--nao-renomear` / `--identificar-tudo` | Does not rename / checks every game by the disc signature. |
| `--somente-renomear` | Only renames the games, without generating anything. |
| `--nao-achatar` | Keeps the folders that hold a single game. |
| `--organizar letra\|raiz` | Moves the games into A…Z folders, or brings them all to the root. |

---

## 📦 What it writes to the USB

Always in the **root** of the USB, with the same name as the game file (for multi-disc games, the name of disc 1):

| Where | What it is |
|---|---|
| `covers/small/<game>.cel` | 56 × 78 cover, for the Covers grid and the main menu. |
| `covers/large/<game>.cel` | 100 × 140 cover, for the other views and the description. |
| `screenshots/medium/<game>.cel` | Screenshot up to 120 × 90. |
| `screenshots/large/<game>.cel` | Screenshot up to 304 × 228, for full screen. |
| `videos/<game>.cvd` | Video preview, in Cinepak, without sound. |
| `.config/3dogamesdetails.ode` | Year, genre, developer, publisher and description of every game. |
| `.config/3doconfig.ode` | Menu options. Only created if it does not exist yet, with the chosen language. |
| `boot.iso` | The menu (if you ask for it). |

The generator **does not touch** your favorites, recent games and statistics.

### Where the images and texts come from

- **Images**: yours first, in the `cover/` and `screenshot/` folders of the media. Whatever is missing is downloaded and kept there, so it works offline next time.
- **Texts**: from `gamelist.pt.txt`, `gamelist.es.txt` or `gamelist.en.txt`, according to the chosen language. Each game has year, developer, publisher, genre and description.
- **Videos**: the ones in this repository are already converted (20 seconds, 15 frames per second) and are just copied. To convert your own, put the source videos in the `videos/` folder (mp4, avi, mkv…) and choose the size, frames per second and length.

### How a game is matched to its cover and texts

Only the title counts: whatever is inside `( )` or `[ ]` in the file name is ignored, as are accents, upper and lower case and punctuation. `Alone in the Dark (USA).iso`, `Alone in the Dark (U).iso` and `Alone in the Dark (English) [!].cue` all find the same cover, screenshot, video and texts.

---

## 💡 Tips

- **Videos slow to convert?** Use `--tamanho small`, fewer seconds and `--video-faltantes`.
- **Slow USB on the console?** Prefer smaller videos (`mini`, `box` or `small`).
- **Game formats**: the ODE reads `.iso` and `.cue` + `.bin`. Other formats must be converted on the PC first.
- **Covers not showing?** Check that the cover file name is the same as the game file name.
