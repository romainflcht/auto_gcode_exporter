# Absolute path to the folder that contain every projects. 
PROJECTS_FOLDER_PATH = 'C:/Users/Romain/OneDrive - ESME/Developpement/PythonProjects/auto_gcode_exporter/3D'

# Activate the DEBUG using True and desactivate it using False. 
DEBUG = False

# Name of the file that need to be created inside of it to ignore it. 
IGNORE_FILENAME = '.ignore'

# File extension of timestamp file that keep track of file modifications. 
TIMESTAMP_FILE_EXTENSION = 'timestamp'

# Gcode extensions that are currently supported, you can add yours.
GCODE_EXTENTION = ('.gcode', '.gco', '.g', '.bgcode', '.bgc', '.ngc')

# Mounting letter that doesn't need to be checked to save some CPU cycle. 
# Add every drive that are always connected to your computer such as 
# external drives or optic disc drives here. 
EXCLUDED_MOUNTING_LETTER = ('C', )


if __name__ == '__main__':
    print('This file is not intended to be executed, execute the \'__main__.py\' file instead.')
