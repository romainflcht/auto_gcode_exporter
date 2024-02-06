# That file contain every text interface used by the program.

VERSION = '1.2'

START_MENU = f"""
╭───────────────────────────────────────────────────┬──────╮
│                    auto_gcode_exporter            │ v{VERSION} │
├───────────────────────────────────────────────────┴──────┤
│ auto_gcode_formatter is an automation script that export │
│ every gcode of a 3D project into a 3D printer USB key    │
│ or SD card.                                              │
│                                                          │
│ HOW TO USE :                                             │
│ - First of all, you need to setup the path of the folder │
│   that contain your 3D projects.                         │
│                                                          │
│ - Next, you need to setup the volume storage by creating │
│   a file named 'usb_printer'. Only volume that contain   │
│   this file will be used to export gcode files.          │
│                                                          │
│ - The only thing that need to be done now is executing   │
│   the file. If you want to use it you may want to        │
│   execute this automation on computer startup. For that  │
│   you can check the step by step guide on the GitHub     │
│   repo.                                                  │
│                                                          │
│    https://github.com/romainflcht/auto_gcode_exporter    │
╰──────────────────────────────────────────────────────────╯
                                       coded by romain_flcht

"""

LOG_STARTUP = """
DEBUG IS ENABLE, DISABLE IT IN THE 'settings.py' FILE. 
─ LOGS ─────────────────────────────────────────────────────
• Waiting on file update..."""


if __name__ == '__main__':
    print('This file is not intended to be executed, execute the \'__main__.py\' file instead.')
