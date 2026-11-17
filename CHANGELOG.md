# 📝 Version history

[← Back to start](README.md) · **English** · [Português](CHANGELOG.pt.md) · [Español](CHANGELOG.es.md)

Everything that changed in the **menu** (`boot.iso`), the **TADEU firmware** and the **generator** (`generate_usb.py`), from the newest version to the oldest.

- [Menu — 1.1](#menu--11)
- [Menu — 1.0](#menu--10)
- [Menu — before 1.0 (0.x versions)](#menu--before-10-0x-versions)
- [TADEU firmware](#tadeu-firmware)
- [Generator (generate_usb.py)](#generator-generate_usbpy)

---

## Menu — 1.1

**Save manager**
- 🎮 **Shows which game each save belongs to.** A bar under the list gives the game name of the selected save (e.g. `alone1.save` → Alone in the Dark). The table has 240 names, ignores upper/lower case and recognises numbered saves (`TE_Devils_1`, `EA_RR3`...). A save that is not in the table is shown by its file name.
- **Copy with the game name or the original name**: the menu asks when copying to USB. With the game name the file becomes `Game (save name).sav`. **Back on the console the save always gets its original name**, which is what the game looks for.
- **Name table can be updated without replacing the menu**: the web page writes the table to `.config/3dogamessaves.ode`. Without that file the menu uses its built-in table. You can also create the file by hand with corrections only (`=name<TAB>game` or `*prefix<TAB>game`).
- **Much faster to navigate**: the screen background is no longer redrawn on every move.
- **Consistent screens**: title, gold bar and text. The copy/restore **SUMMARY** shows one count per line, in colour (green copied/restored, yellow identical, red errors), and gives the reason for the last error.
- **USB list in alphabetical order.**
- **Saves copied into the `saves/` folder from a computer** now show up and restore after the card is prepared on the web page (it records each file in the `saves/3dosaves.ode` catalogue). A catalogue line without a CRC restores unchecked; with a CRC, a changed file is still refused.
- Backups made with 1.0 still restore.

**Showcase and Strip**
- **The game description appears instantly when moving to a neighbouring game**: with the controller idle and the covers already on screen, the menu reads ahead the descriptions of the 2 games on each side and of the letter-jump targets. Reading stops as soon as the controller moves.

**Options**
- The menu stores **which ODE it detected** (firmware, type and whether there is a clock). The web page reads this and pre-selects the right choices.

**Web page**
- **Selects the ODE, the TADEU firmware and the clock by itself** from what the menu detected.
- **Writes the save-name table** to the card.
- **Records the saves in the `saves/` folder** in the catalogue and fixes size and CRC of old lines.
- Fix: with **Keep** selected, your own covers, screenshots and videos already on the card are no longer copied again.

---

## Menu — 1.0

First public version. It gathers everything done in the development versions (0.x), described below, and adds:

- 💿🔥 **REAL CDs ON THE XPORT, WITHOUT REMOVING THE BOARD (exclusive).** With the expansion board plugged in, the main screen gains the **CD** tile (dark gray with no disc, light blue with a disc). **A** takes the Xport off the port, asks you to open and close the lid (FZ-10) or opens and closes the tray (other models), and the console restarts by itself into the disc. **B** cancels. The Xport factory menu has no such function. Confirmed on real hardware on the FZ-10; automatic tray on the other models is being tested. The routine lives in a separate file on the disc (`XportCD`), loaded only at that moment.
- **New description screen**: the game name moved to the top bar and the sheet was organised ("Played: 2x - Last date", **developer**, **publisher**, genre, year, country, discs with icons). With one image, the sheet sits beside it; with two, the images go to the left and the sheet and text to the right; with three, the images stay on top. Long names, developers and publishers scroll slowly; scrolling the text no longer stops the video; the favorite effect shows over the cover.
- **You choose what the sheet shows**: *Options > Appearance > Description* shows or hides each item.
- **Publisher of each game**, shown in Showcase and Strip (the game texts gained the `Publisher` field).
- **Videos of 20 seconds at 15 frames per second** as the default.

What 1.0 has, in short: 6 view modes, video preview, favorites, recent games and statistics, filter and sorting, multi-disc, save manager, console tools, 3 languages, real-time clock, console detection and support for both firmwares.

---

## Menu — before 1.0 (0.x versions)

The development versions, from the newest to the oldest.

### 0.9 — Showcase, Strip, backgrounds and new options

**New Showcase and Strip modes**
- **Two new view modes**: **Showcase** (a large cover with developer, genre, year, country and the whole description) and **Strip** (the game screenshot and the description on top, a sliding row of covers below).
- In both, ◄ ► changes game and ▲ ▼ scrolls the description.
- The screenshot and the description of the game are read **before** the neighbouring covers, so they appear right away.
- On the last game panel of the main menu, **A opens the description** and P plays right away.
- **Translations outside the program**: Spanish and English became files on the menu disc, read only when used. The program got smaller and memory was freed.
- **Faster options**: moving between items and changing values no longer redraws the whole screen.
- **Percentage inside every progress bar.**
- When a write finishes, the screen shows the **size and time** ("6 minutes and 11 seconds").
- Controller test: the exit bar takes the colour of the controller holding the buttons.
- The settings backup lists what will be saved: settings, recent games, favorites and statistics.
- The screen saver no longer starts right after a long operation.
- The last game cover no longer disappears when changing the view.

**Backgrounds, separate tools and memory**
- **9 backgrounds** (Default, Carbon fibre, Brushed steel, Honeycomb, Stripes, Grid, Plate, Vignette, Dots).
- **Tools in a separate module**, loaded only when one of them opens: the menu got lighter.
- **Cover memory per view**: the Covers grid keeps many small covers; the other views, large covers.
- **Screen saver** with the 3DO logo and the consoles drifting across the screen.
- Music playing again on consoles with little free memory.
- Firmware update success screen with the console picture and the reminder to power off and on.
- *About* shows the ODE firmware and version; *Console information* shows the music and the covers in memory.
- The Appearance accordion always opens closed.
- The clock is polled every 5 seconds, making the menu more responsive.

**New options and sound**
- **Appearance as an accordion**: Main menu, Games, Media and Screen, one group open at a time, animated.
- **Sort by** name, year, genre, developer or most played.
- **Remember the position**, **Article in front**, **Start screen** and **Screen saver**.
- **Backup and restore of the settings**, favorites, recent games and statistics, and **Restore the defaults**.
- **Own music player**, with a **volume bar** that changes on the spot, and the **Random** option.

### 0.8 — Game card, factory firmware, clock and media

**Game card and adjustments**
- **Game card at start**: cover, name in yellow, genre, year and country in blue, "played N times" and "N discs added to the queue".
- **Name speed** in 5 levels.
- Last game cover fixed in the Covers grid; adjustments to the list lines.
- Games opening again on the factory firmware after browsing folders.

**Factory firmware and clock**
- **Full compatibility with the factory firmware**: the menu no longer uses commands it does not have, and writing to the USB gained retries.
- **Features per firmware version**: each option only appears if the installed firmware has it.
- **Warning for a clock without a valid time** (low battery), without freezing the menu, with a shortcut to set it.
- When setting the clock, the year already starts at the current year.
- Entering and leaving the last game panel became instant.
- On the expansion-port ODE, the texts say **SD** when the media is a microSD card.
- Measurement of start-up times.

**List, statistics and sounds**
- **Video in the list**: the preview plays in the box next to the list.
- **Star effect** when adding and removing a favorite, with its own sound.
- **Statistics as a ranking**, with the number of plays of each game.
- Sounds kept on the menu disc.
- **Read the USB again** live, and options saved on the spot.
- **Acknowledgements** page with scrolling.
- "Last" entry at the top of the game list.
- The list is read only once, and full diagnostics.
- List fixed on the expansion-port ODE.

**Media in two sizes**
- **Covers and screenshots in two sizes**: small for the grids, large for the highlight and full screen.
- Covers read with fewer commands; Covers grid with 3 pages in memory.
- Video in several sizes, with a still image when the video is heavy.
- **Formats per language** (date, time, temperature, numbers).
- **Storage manager** and **Date and time** screen.

### 0.7 — Video and sound
- **Cinepak video** with its own decoder: in the description, full screen (X) and later in the list.
- **Sound effects and background music**, with 10 tracks.
- Final buttons of the description screen.

### 0.6 — New look and tools
- **New look**: thin bands on every screen, a shine passing over the selected tile of the main menu.
- **Controller test** with the picture of the controller, for up to 8 controllers.
- **Picture adjustment**.
- **Saved list** (*Read at power-on*) to start faster.
- **Language switched on the spot** (Português, Español, English).
- Menu images outside the program, on the disc.
- **ODE and USB test**.
- Separate information pages: console, ODE and USB.
- "Game starting" window.

### 0.5 — Playing on any firmware
- Game launching fixed on both firmwares and both boards.
- **Multi-disc**: all discs are queued when you play.
- Less memory used; no list failures on large collections.

### 0.4 — Options, description and saves
- **Options saved to the USB** (`.config/3doconfig.ode`).
- **Game description screen**: cover, screenshot, data and the scrolling text.
- **Favorites, Recent and Statistics**, with date and time.
- **Filter** by genre and country.
- **Storage**: save manager, backup, restore and diagnostics of the NVRAM.
- **Extraction of the console's ROMs and RAM**.
- **Firmware backup and update** from the menu.
- Letters in uppercase, lowercase or capitalized.

### 0.3 — Main screen and identity
- **Main menu** with the Favorites, Games, Statistics, Recent and Options tiles.
- **Last game panel.**
- **Console detection through the BIOS**, with the picture of the machine at the top.
- **Clock, date and temperature** on screen.
- **One cover per game**, and the texts of all games in a single file, read once.
- Disc count, region taken from the file name, translucent strip with the discs on the cover.
- CD icon in place of a missing cover.

### 0.2 — Rewritten from scratch

On November 10, 2026 the menu was **rewritten from scratch**, with new code, faster and simpler to maintain.
- **Alphabetical list** with the cover next to it, cover memory and read-ahead.
- **Four views**: List, Covers, Carousel and Carousel FX (in perspective, with a reflection).
- Automatic **NTSC and PAL**.
- **A single `boot.iso`** for the internal ODE and the expansion-port one.
- Games in subfolders (up to 3 levels) in a single list.
- Jump by letter, scrolling of long names, acceleration when holding the D-pad.

### 0.1 — First generation

From October 10 to November 9, 2026.

- **Last stage** — tabs switched with L / R; 4 view modes; details screen redesigned; Tools and Options reorganized; **firmware backup** from the console; extractions in the `roms/` folder and the NVRAM in `saves/`; screen saver with the 3DO logo and consoles; 10 music tracks.
- Reading by path, guaranteed alphabetical order, instant description, smoother small preview, "Clear" in Recent.
- Folders by letter merged into a single list; stable base.
- Real-time firmware detection, Covers grid drawn by the console's graphics engine, faster genre switching, video preview, firmware update.
- Base menu: alphabetical list, favorites and recent games, filter by genre, cover memory, multi-disc, full-screen screenshots, settings saved to the USB.

---

## TADEU firmware

### 1.0.5
- **Real-time clock (DS3231)**: date, time, temperature and battery state.
- **Files written with the right date and time**.
- Setting the clock from the console.

### 1.0.4
- **USB space**: total size and free space reported to the menu.

### 1.0.3
- **A single code base for both boards** (the original and the clone with a regular Pico), chosen at build time.

### 1.0.2
- **Version marker** inside the firmware, which the menu reads and shows.

### 1.0 and 1.0.1
- **Fast list by extension**: games are recognized by `.cue` and `.iso` without opening each file. Launching a game at the end of the USB dropped from about 30 s to 2 to 4 s.
- **Incremental paging** of the list.
- **Folder creation** from the console.
- **Firmware backup** from the console, verified byte by byte.
- **Update from the menu**, with a staging area, CRC check and verification of every block written. The firmware in use is never overwritten before the check.
- **Fail-safe update at power-on**: checks before and after copying; if anything fails, it enters recovery mode instead of starting broken.
- **Chip serial number.**
- File opening fixed: reading a file that does not exist no longer creates an empty file.
- Flash memory map adjusted for 2 MB chips.
- Recovery always possible through BOOTSEL.

---

## Generator (`generate_usb.py`)

### November 2026
- **Publisher** (`Publisher=`) in the game texts, in Portuguese, Spanish and English.
- Video defaults: 20 seconds, 15 frames per second.
- **Cinepak videos** (`.cvd`), in 5 sizes, with frames per second, length and quality of your choice.
- **Faster video conversion**, one video per PC core at the same time.
- **Covers and screenshots in two sizes** each.
- Separate questions for covers, screenshots and videos, each with "only the missing ones".
- Reuses a USB generated by old versions, without needing the original images.
- Creates the menu options file with just the language, if it does not exist yet.
- Old code removed: a single file is left, smaller and simpler.
- Wizard answers kept in `generate_usb.ini`.

### October 2026
- Step-by-step wizard in 3 languages.
- Download of the missing covers and screenshots.
- Game texts (year, genre, developer, description).
- Conversion of `.chd` and `.iso` to `.bin/.cue`.
- Renaming of discs with generic names and organization into folders.
- Copy of `boot.iso` and firmware preparation.
