# ⏰ Real-time clock on the 3DO — installing the DS3231

[← Back to start](../README.md) · **English** · [Português](RTC.pt.md) · [Español](RTC.es.md)

The 3DO never had a clock. With a **DS3231** module wired to the ODE's Raspberry Pi Pico and the **TADEU 1.0.5** firmware, your console knows the date, the time and the temperature. It is the **first 3DO ODE in the world with a real-time clock**.

It takes **4 wires**. If you have ever soldered a wire, you can do it.

---

## What you get

- Date, time and temperature on the main menu.
- "Played: mm/dd/yyyy - hh:mm" on the last game, in Recent and in Statistics.
- Files written to the USB with the right date (NVRAM backups get the date and time in their name).
- Setting the clock on the console itself, in 12 or 24 hours.
- A warning when the clock battery runs out.

## Automatic detection

You do not need to configure anything. At power-on, the menu asks the ODE whether a clock exists.

- **With the module**: date, time and temperature appear, and the clock options show up in the menu.
- **Without the module**: nothing appears and nothing changes. No zeroed clock and no error message; the console works as always.

In other words: installing the TADEU 1.0.5 firmware **without** the module is no problem at all.

## What you need

| Item | Note |
|---|---|
| **DS3231** module | Any module with the **VCC, GND, SDA and SCL** pins. The most common is the blue one, with a battery holder. |
| Module battery | **CR2032** (see the battery warning below). |
| 4 thin wires | Preferably in 4 colours. About 10 to 15 cm (4 to 6 in) each. |
| Soldering iron and solder | Fine tip. |
| **TADEU 1.0.5** firmware or newer | Earlier versions do not talk to the clock. |

---

## The wiring

<p align="center"><img src="../github/rtc-ds3231-pinos.png" width="720" alt="DS3231 wiring on the Raspberry Pi Pico"></p>

| Pico pin | Name | Goes to the DS3231 |
|:---:|---|:---:|
| **1** | GP0 | **SDA** |
| **2** | GP1 | **SCL** |
| **3** | GND | **GND** |
| **36** | 3V3 (OUT) | **VCC** |

The module's **32K** and **SQW** pins stay unconnected.

**Finding the pins:** look at the Pico from above, with the USB connector at the top. Pin 1 is the first on the left, counting from the top; 2 and 3 come right below. Pin 36 is on the right side: it is the **fifth** from the top (40, 39, 38, 37, **36**).

> ⚠️ **Use 3V3 (pin 36), never VBUS or VSYS (pins 40 and 39).** Those two carry 5 V and can damage the Pico through the data wires.

> ⚠️ **Do not solder to the three "DEBUG" pads** at the bottom end of the Pico. They are not used here.

---

## Step by step

1. **Unplug the console from the wall** and open it until you reach the ODE board.
2. **Check the firmware** before soldering: *Options → ODE Device → ODE information* must show **TADEU 1.0.5** or newer. If not, update first.
3. **Solder the 4 wires to the module**: VCC, GND, SDA and SCL.
4. **Solder the 4 wires to the Pico**, following the table. Solder quickly, with little solder, and check that no pin touches its neighbour. Pins 1, 2 and 3 sit side by side: that is where most mistakes happen.
5. **Put the battery** in the module.
6. **Fix the module** with double-sided tape somewhere it does not touch any metal. Insulate its underside with electrical tape.
7. **Close the console and turn it on.**

## Checking and setting the time

1. Open *Options → ODE Device → Features*. The **Clock (DS3231)** line must say **Yes**.
2. The first time, the menu warns that the clock has no valid time and offers to set it. Press **A**.
   Or go to *Options → ODE Device → Date and time*.
3. ◄ ► chooses the field, ▲ ▼ changes the value, **A** saves. **12 or 24 hours** is chosen there too.
4. Go back to the main menu: date, time and temperature appear at the bottom right.

To hide any of them: *Options → Appearance → Main menu → Time / Date / Temperature*.

---

## ⚠️ The battery

Many blue DS3231 modules leave the factory with a **charging circuit** (a diode and a resistor next to the holder), meant for the rechargeable **LIR2032** battery.

- With a **regular CR2032** (non-rechargeable): **disable the charging circuit** by removing the diode or the resistor next to the battery holder. A regular battery must not be recharged.
- With an **LIR2032** (rechargeable): you can leave the circuit as it is.

When in doubt, use the module with charging disabled and a CR2032: it lasts for years.

The DS3231 does not measure the battery charge. What it can tell is whether **the clock stopped** at some point. When that happens, the menu warns at power-on that the battery is low and asks you to set the time. If the warning comes back every time you turn the console on, replace the battery.

---

## Common problems

| Symptom | What to check |
|---|---|
| **Clock (DS3231): No** in Features | Firmware older than 1.0.5; SDA and SCL swapped; cold solder joint; VCC on the wrong pin. |
| The time resets when powered off | Battery low, missing or reversed. |
| "No valid time" warning every time | Low battery: replace it and set the time again. |
| Console does not turn on after the installation | Turn it off immediately. Look for shorted pins (1, 2 and 3 sit side by side) and check that VCC did not end up on pin 39 or 40. |
| Temperature seems high | It is the temperature **inside the console**, measured by the DS3231 itself. It is normal for it to be higher than the room's. |

## Technical details

- **I²C 0** bus of the RP2040, at 100 kHz: **GP0 = SDA**, **GP1 = SCL**.
- DS3231 address: **0x68**.
- The firmware reads the clock and keeps the last reading; the menu asks every few seconds.
- The date and time are also used by the ODE's file system: everything the console writes to the USB gets the right date.
- Wiring tested on the board with a regular Raspberry Pi Pico. The firmware uses the same GP0 and GP1 on the original board (RP2040-Plus); if that is yours, check first that those two pins are free on the board.
- Without the module, the firmware and the menu work normally: the clock simply does not appear.
