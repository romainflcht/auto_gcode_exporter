from settings import *
from acsii_art import START_MENU, LOG_STARTUP
import sys
import os
import glob
import time
import shutil
import win32con
import win32api
import win10toast


MOUNTING_LETTER_RANGE = ('A','B','D','E','F','G','H','I',
                        'J','K','L','M','N','O','P','Q',
                        'R','S','T','U','V','W','X','Y','Z')


def detect_new_project() -> None:
    """
    Function that detect every project directories that doesn't have a gcodes
    folder and create it. 
    """
    projects = glob.glob(os.path.join(PROJECTS_FOLDER_PATH, '*'))
    
    for project in projects:
        # Create gcode folder for each projects.
        if os.path.isfile(os.path.join(project, IGNORE_FILENAME)):
            continue

        if os.path.exists(os.path.join(project, 'gcodes')):
            continue

        os.mkdir(os.path.join(project, 'gcodes'))


def fill_export_queue(export_queue: list) -> None:
    """
    Function that find every files that need to be exported and add them to
    the export queue.
    """

    # Fetch every project.
    projects = glob.glob(os.path.join(PROJECTS_FOLDER_PATH, '*'))
    
    for project in projects:
        # Ignore each folder that contain .a_g_e_ignore file. 
        if os.path.isfile(os.path.join(project, IGNORE_FILENAME)):
            continue

        # Get the project name to create folder in storage volume later 
        # and loop through each gcode project files.
        project_name = os.path.basename(project)
        gcode_folder_path = os.path.join(project, 'gcodes')

        for file in glob.glob(os.path.join(gcode_folder_path, '*')):

            # Get the filename, file extension.
            filename, file_extension = os.path.splitext(os.path.basename(file))

            # Ignore all ts_file to not create ts_file of ts_files. 
            if file_extension.lower() not in GCODE_EXTENTION:
                continue

            # Create the timestamp_file path.
            ts_file_path = os.path.join(gcode_folder_path, f'.{filename}.{TIMESTAMP_FILE_EXTENSION}')

            

            # If a gcode file doesn't have ts_file, then it's new and need to be exported.
            if not os.path.isfile(ts_file_path): 
                # Create the ts_file. 
                with open(ts_file_path, 'w') as ts_file:
                    ts_file.write(f'{int(os.stat(file).st_mtime)}')

                # Hide the file. 
                # Hidding the file create a PermissionError when accessing the file. 
                #! win32api.SetFileAttributes(ts_file_path, win32con.FILE_ATTRIBUTE_HIDDEN)

                # Add the file to the export queue. 
                export_queue.append((project_name, file))

                if DEBUG:
                    message = f'• [{file}] Added in the export queue.'
                    
                    if len(file) > 29: 
                        message = f'• [{file[0:26]}...] Added in the export queue.'
                        
                    print(message)


                # Check the next file. 
                continue
            
            # If the ts_file exist, then compare timestamps. 
            with open(ts_file_path, 'r') as ts_file:
                previous_ts = int(ts_file.read().rstrip('\n'))
                current_ts = int(os.stat(file).st_mtime)

                # If the file is newer, then export it.
                if previous_ts < current_ts:
                    # Update the ts_file. 
                    with open(ts_file_path, 'w') as ts_file:
                        ts_file.write(f'{int(os.stat(file).st_mtime)}')

                    # Add the file to the export queue.
                    export_queue.append((project_name, file))
                    
                    if DEBUG:
                        message = f'• [{file}] Added in the export queue.'
                        
                        if len(file) > 29: 
                            message = f'• [{file[0:26]}...] Added in the export queue.'
                            
                        print(message)
                
                # Else: Nothing need to be done. 
    return


def detect_storage_plug() -> str:
    """
    Function that check if a storage volume is inserted and if 
    it is a 3D printer storage volume.

    :return: The mounting letter of the storage.
    """

    # Check look on every mounting letter to see if a new one is plugged in.
    for mounting_letter in MOUNTING_LETTER_RANGE:
        # Exclude every excluded mounting letter. 
        if mounting_letter in EXCLUDED_MOUNTING_LETTER:
            continue

        if not os.path.exists(os.path.join(f'{mounting_letter}:')):
            continue

        # A storage volume has been detected, check if it is a 3D printer one.
        if not os.path.isfile(os.path.join(f'{mounting_letter}:', 'usb_printer')):
            continue

        # The storage is a 3D printer storage, return the mounting letter
        return mounting_letter

    # No storage volume has been detected, return None. 
    return


def export_files(export_queue: list) -> int:
    """
    Function that handle the exportation of every gcode files that 
    wait to be exported. 

    :return: Exit code (1: Error, 0: Executed). 
    """

    if export_queue == []:
        # export queue is empty, abort.
        return 1

    # Check if a storage volume is detected. 
    storage_mounting_letter = detect_storage_plug()
    if storage_mounting_letter is None:
        # No storage volume detected, abort.
        return 1
    
    if DEBUG:
        message = f'• Storage detected on {storage_mounting_letter}:\ starting exporting {len(export_queue)} files...'
        
        if len(message) > 60: 
            message = message[0:57] + '...'
        
        print(message)
    
    for file_to_export in export_queue:
        # Export the file to a folder named after the project name that the file belong to. 
        project_name, filename = file_to_export
        export_path = os.path.join(f'{storage_mounting_letter}:', project_name)

        if not os.path.isdir(export_path):
            os.mkdir(export_path)

        # Export the file. 
        shutil.copy(filename, export_path)
    
    return 0

def send_toast_export_finished(export_time: float) -> None:
    """
    Function that send a windows notification when export finished.

    :param export_time: time that the export has taken in second.
    """
    # Init toast notification object.
    toast = win10toast.ToastNotifier()

    # Send the notification. 
    toast.show_toast('auto_gcode_exporter',
                    f'Export finished in {export_time:.4f} sec.',
                    duration = 5,
                    # icon_path = 'icon.ico',
                    threaded = True,
    )

    if DEBUG:
        print(f'• Export finished in {export_time:.4f}sec.\n\n• Waiting on file update...')


def main() -> None:
    """
    Function that run the whole program. 
    """

    # Create the export queue list. 
    export_queue = []
    print(os.getcwd())

    print(START_MENU)

    if DEBUG:
        print(LOG_STARTUP)

    # Run indefinitly. 
    while True:

        # Catch the KeyboarInterrupt and print a goodbye message. 
        try: 
            # Execute the program. 
            detect_new_project()
            fill_export_queue(export_queue)

            # Start a timer to get the export time. 
            start_timer = time.time()

            # Check if an export has been done, in this case clear the export 
            # queue and show the export finished notification. 
            if export_files(export_queue) == 0:
                export_queue.clear()
                send_toast_export_finished(time.time() - start_timer)
        
        except KeyboardInterrupt:
            # Print a nice goodbye message. 
            print('\n' * 255 + 'Au revoir :)')
            sys.exit(0)


if __name__ == '__main__':
    print('This file is not intended to be executed, execute the \'__main__.py\' file instead.')
