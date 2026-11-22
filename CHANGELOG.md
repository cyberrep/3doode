# 📝 Version history

[← Back to start](README.md) · **English** · [Português](CHANGELOG.pt.md) · [Español](CHANGELOG.es.md)

Everything that changed in the **menu** (`boot.iso`), the **TADEU firmware** and the **generator** (`generate_usb.py`), from the newest version to the oldest.

- [Menu — 1.5](#menu--15)
- [Menu — 1.4](#menu--14)
- [Menu — 1.3](#menu--13)
- [Menu — 1.2](#menu--12)
- [Menu — 1.1](#menu--11)
- [Menu — 1.0](#menu--10)
- [Menu — before 1.0 (0.x versions)](#menu--before-10-0x-versions)
- [TADEU firmware](#tadeu-firmware)
- [Generator (generate_usb.py)](#generator-generate_usbpy)

---

## Menu — 1.5

**Fixes**
- **The controller no longer freezes while covers load.** Each cover is now read in short steps, and the controller keeps responding during loading, in every view. A quick tap on a direction is no longer lost.
- **Strip view: the country was cut off**, showing only its first letter. Year and country now sit on a translucent band along the bottom of the game screenshot (year on the left, country on the right); the genre stays in the text.
- **Strip view: a game name that does not fit on screen now scrolls**, as in the List.
- **Message windows and Tools:** the button band went past the rounded border of the window.
- **Showcase:** the CD jewel case cover sat lower than the long box; both now start at the same height.

**Speed**
- ⚡ **Covers load before you reach them:** the current page and the next one, in the Covers view.
- **Game screenshots ready as you browse** (Strip, and List with screenshot): the menu keeps 5 screenshots and reads the neighbours of the selected game ahead of time.
- **Faster description in Showcase and Strip.** On an ODE that can seek inside a file, the menu jumps straight to the game's text instead of reading the description file from the start.
- **Lighter drawing** in the Covers view while covers arrive.

**Memory**
- 🧠 **More covers in memory at once.** Tools and the save catalogue only take memory while open, the folder area only exists in Folders mode, and free video memory now holds covers.
- The cover space is rebuilt on every view change, sized for what the view needs.

**Options and texts**
- **Options → ODE Device** opens as an accordion, like Appearance (every submenu that does not fit on screen works this way).
- First start text: **"SAVING THE GAME LIST — The next startup will be faster"**.

---

## Menu — 1.4

**Game list**
- **The first game on the card no longer goes missing on the Xport with FAT32.** On cards with one folder per letter, the game in the first folder (e.g. `#/3D Pinball…`) was left out of the list.
- **A game with no description uses the one from the same game of another region.** "Battle Blues (Korea)" shows the developer, genre, year and description of "Battle Blues (USA)" when only one of them has text.
- The **COULD NOT START** notice shows the whole error code (it used to show only the last digit).

**Covers**
- 🖼️ **New option Options → Appearance → Cover format.** Long boxes and CD jewel cases are no longer stretched:
  - **Original** (default): the cover is shown in its own proportion, with the frame around it.
  - **Ambilight**: the cover in the middle, with a glow in the cover's own colors filling the rest.
  - **Black background**: the cover in the middle, the rest black.
  - **Stretched**: as it was before.
- It applies to every screen: List, Covers, Carousel, Carousel FX, Showcase, Strip, Description and the small cover on the home screen.
- In the **List**, the cover always starts at the height of the first game row, and the gold line and the play count sit right under it.
- Covers need to be **written again** (the web page does it by itself); old ones keep working, stretched as before.

**Options and Tools**
- The **Test the ODE and the USB** report (`3dodiag.txt`) now also carries the USB read log: a single file to send when something goes wrong.
- Five texts that showed up in Portuguese in Spanish and English are now translated (Read the USB again, save backup and the missing-tool notice).

**Web page**
- ✨ **Sharper, cleaner images.** Covers and screenshots are now shrunk by averaging the whole area of the original image, with light sharpening and no dithering: the jagged edges, the grain and the white outline around letters and characters are gone.
- **Covers in their real proportion** (long box and CD jewel case), ready for the Cover format option.
- **Old covers and screenshots on the card are replaced by the new ones** on the first write, even with "Keep" selected. Only the ones with no source to rebuild from stay.
- **Summary before writing**: the Write to the card screen shows what will be written, what is already on the card and the total number of files.
- **The right region's cover** for your own images: "Cannon Fodder (USA)" no longer takes the "(Europe)" cover. With no cover for the region, the order is USA, Europe, Japan.
- Images in subfolders with unknown names (such as `cover3d`) no longer count as covers.
- One button at a time while writing: Start when idle, Stop while writing.

---

## Menu — 1.3

**Game list**
- 🏷️ **New option Options → Games → Game names: Title or File.** With **File** the list shows the file name without the extension (e.g. `Doom (USA)`); with **Title**, the usual clean name (`Doom`).
- **A game stored as `.cue` + `.iso` with the same name shows up only once** (it used to show twice). If you use the saved list, run **Read the USB again** once.
- **Empty Favorites and Recents**: new messages and the window closes on the first button press.

**Notice and confirmation windows (standard pop-up)**
- 🪟 **Every confirmation and notice now uses the same window**, in the menu and in the Tools: yellow title, golden line, text and a band at the bottom with the buttons (Ⓐ YES / Ⓑ NO, Ⓑ BACK, Ⓑ CANCEL). Several of them used to open full screen.
- **One window from start to finish.** For backup, restore, extraction and firmware writing, the same window shows the question, the progress and the result.
- **SUMMARY inside the window** at the end: "Saved successfully", size and time; in the save manager, the count of copied, identical and failed items.
- Clear recents and clear statistics ask in the window, describing what will be erased.

**Write progress**
- 📊 **New "SAVING" progress**: shows what is being written (system ROM, firmware, NVRAM…), the **file name**, the bar with the percentage and the **speed in KB/s**.
- **Ⓑ cancels the firmware backup and the firmware write.** When writing, the cancel happens before applying: the current firmware stays.
- Writing the firmware asks for **a single confirmation** (it was two).
- After writing the firmware: "The ODE is restarting the 3DO. If it doesn't return, power off and on."

**Options and Tools**
- **Read the USB again happens inside the window**, with the game count and the bar, without switching to the start screen.
- Real scroll arrows on the information screens (they were the letters `^` and `v`).
- Restore the options backup: clearer text ("All items will be restored from USB.").
- The **STARTING THE GAME** window got the yellow title, like the others.

**Web page**
- New options **Show games (List / Folders)** and **Game names (Title / File)**.
- When preparing the card, it **creates the `.config`, `saves`, `firmware` and `roms` folders**, so the menu finds everything in place.
- The firmware choice is now **DIR-HIGH** or **DIR-LOW**, with an explanation of which one fits each board.

---

## Menu — 1.2

**Folder navigation**
- 📁 **New option Options → Appearance → Show games: List or Folders.** In **Folders** mode, the card's folders become items you **enter** (A) and **go back** from (B). A folder with 2 games or more becomes a folder; **a folder with a single game becomes that game**. System folders (covers, videos, saves, roms…) stay ignored.
- 🎨 **Folders match the menu's look**: a yellow folder icon with a **big letter in the middle**, cover-shaped in the large modes (Covers, Carousel, Showcase, Strip). The folder is **transparent**, with no frame — only the selected one is highlighted.
- Clearer **"no games found"** message (in all 3 languages), warning about reserved folder names.

**Save manager**
- 🌎 **Fully translated** (Spanish and English): a few screens were still Portuguese-only.

**Fixes**
- The folder list shows up **right away**, without re-reading the USB.
- Fixed a cover-border color swap (red where it should be blue) in some modes.

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
- ⚡ **Showcase and Strip are much faster to navigate.** In 1.0, on every game change the menu waited and read the text file again, even for a game it had just shown; on large lists the description took close to 1 second.
- **Instant description when going back or forward**: the last 8 descriptions stay in memory, so moving back and forth between neighbouring games no longer reads the card.
- **Read-ahead of neighbours**: with the controller idle and the covers already on screen, the menu reads the descriptions of the 2 games on each side and of the letter-jump targets (previous and next). Reading stops as soon as the controller moves, so it delays neither the covers nor navigation.

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

### 1.0.6
- 🕒 **The clock protects itself.** At power-on the firmware looks for the clock chip (DS3231). If the board does not have it, the two clock pins are released and the date and time functions stay off, instead of disturbing everything else.
- 📦 **Two files, one for each kind of board: `TADEU_1.0.6_DIR-HIGH` and `TADEU_1.0.6_DIR-LOW`.**

**Which file: DIR-HIGH or DIR-LOW?**

The ODE boards have a chip that controls the direction of the data between the ODE and the console. There are two models of that chip, and they work with the direction signal inverted relative to each other. The firmware must match your board.

- **`TADEU_1.0.6_DIR-LOW`**: original Waveshare board (74HC245 chip).
- **`TADEU_1.0.6_DIR-HIGH`**: clone boards such as tzmwx and TaiHu (74LVC4245 chip).

**If you write the wrong one:** the console shows the 3DO logo and then a black screen. Nothing is damaged: put the Pico in BOOTSEL mode (hold the button while plugging it into the computer) and write the other file.

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

### November 2026 (menu 1.4)
- ✨ **Sharper, cleaner images**: area-average shrinking, light sharpening and no dithering, the same as the web page. The old "preparations" (text, sharp, soft…) are gone.
- **Covers in their real proportion** (long box ≈ 76x140, CD jewel case ≈ 100x87), not stretched.
- **Old covers and screenshots are rebuilt by themselves** on the first run (`generate_usb.py` and `converter_tudo.py`).

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
