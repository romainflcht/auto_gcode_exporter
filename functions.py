import os
import glob
import shutil

PATH = '3D'
MOUNTING_LETTER_RANGE = ('A','B','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z')
EXCLUDED_MOUNTING_LETTER = ('C', )


def detect_new_project():
    projects = glob.glob(os.path.join(PATH, '*'))
    
    for project in projects:
        # Create gcode folder for each projects.
        if os.path.exists(os.path.join(project, 'gcodes')):
            continue

        os.mkdir(os.path.join(project, 'gcodes'))



def detect_storage_plug() -> str:
    """
    Function that check if a storage volume is inserted and if 
    it is a 3D printer storage volume.

    :return: The mounting letter of the storage.
    """
    
    # Check look on every mounting letter to see if a new one is plugged in.
    for mounting_letter in MOUNTING_LETTER_RANGE:
        if not os.path.exists(os.path.join(f'{mounting_letter}:')):
            continue

        # A storage volume has been detected, check if it is a 3D printer one.
        if not os.path.isfile(os.path.join(f'{mounting_letter}:', 'usb_printer')):
            continue

        # The storage is a 3D printer storage, return the mounting letter
        print(f'export to {mounting_letter}:')
        return mounting_letter

    # No storage volume has been detected, return None. 
    return


def export(export_queue):
    """
    Function that handle the exportation of every gcode files that 
    wait to be exported. 

    :param export_queue: _description_
    :return: _description_
    """

    if export_queue == []:
        # export queue is empty, abort.
        return 1

    # Check if a storage volume is detected. 
    storage_mounting_letter = detect_storage_plug()
    if storage_mounting_letter is None:
        # No storage volume detected, abort.
        return 1
    
    for file_to_export in export_queue:
        shutil.copy(file_to_export, os.path.join(f'{storage_mounting_letter}:'))
    
    return 0