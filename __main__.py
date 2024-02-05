import os
import glob
from functions import export

PATH = '3D'
TS_EXT = 'timestamp'
GCODE_EXT = ('.gcode', '.gco', '.g', '.bgcode', '.bgc', '.ngc')



export_queue = []




def fill_export_queue():
    """
    Function that find every files that need to be exported and add them to
    the export queue.
    """

    # Fetch every project.
    projects = glob.glob(os.path.join(PATH, '*'))
    
    for project in projects:
        # Get the project name to create folder in storage volume later 
        # and loop through each gcode project files.
        project_name = os.path.basename(project)
        gcode_folder_path = os.path.join(project, 'gcodes')

        for file in glob.glob(os.path.join(gcode_folder_path, '*')):

            # Get the filename, file extension.
            filename , file_extension = os.path.splitext(os.path.basename(file))

            # Ignore all ts_file to not create ts_file of ts_files. 
            if file_extension.lower() not in GCODE_EXT:
                #print("HERE")
                continue

            # Create the timestamp_file path.
            ts_file_path = os.path.join(gcode_folder_path, f'.{filename}.{TS_EXT}')

            

            # If a gcode file doesn't have ts_file, then it's new and need to be exported.
            if not os.path.isfile(ts_file_path): 
                # Create the ts_file. 
                with open(ts_file_path, 'w') as ts_file:
                    ts_file.write(f'{int(os.stat(file).st_mtime)}')

                # Add the file to the export queue. 
                export_queue.append((project_name, file))

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
                
                # Else: Nothing need to be done. 
    return




while (1):
    fill_export_queue()
    