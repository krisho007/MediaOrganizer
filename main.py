import os
import stat
from datetime import date, datetime
import tkinter as tk
from pathlib import Path
import exifread
import shutil

def getUserInput():
    sSourceDirectory = input("Enter Source Directory: ")
    if sSourceDirectory == "":
        sSourceDirectory = os.getcwd()

    sDestinationDirectory = input("Enter Destination Directory: ")

    return sSourceDirectory, sDestinationDirectory

def getExifDateTaken(filePath):
    with open(filePath, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        dateTaken = tags["EXIF DateTimeOriginal"]
        return datetime.strptime(str(dateTaken), '%Y:%m:%d %H:%M:%S').date()

def getImageTakenDate(filePath):
    fileStatsObj = os.stat(filePath)
    fileCreationTime = date.fromtimestamp( fileStatsObj [ stat.ST_CTIME ] )
    fileModificationTime = date.fromtimestamp( fileStatsObj [ stat.ST_MTIME ] )
    fileExifDate = getExifDateTaken(filePath)
    return min([fileCreationTime, fileModificationTime, fileExifDate])

def getImageSize(filePath):
    fileStatsObj = os.stat(filePath)
    return fileStatsObj.st_size

def getPayload(sSourceDirectory, sDestinationDirectory):
    # Get the list of all files in directory tree at given path
    listOfFiles = list()
    skippedFiles = list()
    targetDirectories = list()
    for (dirpath, _, filenames) in os.walk(sSourceDirectory):
        for file in filenames:
            # Skip non JPEG files
            if os.path.splitext(file)[1] not in ['.jpg', '.JPG']:
                continue
            filePath = os.path.join(dirpath, file)
            imageTakendate = getImageTakenDate(filePath)
            targetDirectory = f"{sDestinationDirectory}\\{imageTakendate.year}\\{imageTakendate.month:02}-{imageTakendate.strftime('%B')}"

            # Check if filename already exists
            if os.path.isfile(f"{targetDirectory}\\{file}"):
                # Check if file size is same
                if getImageSize(filePath) == getImageSize(f"{targetDirectory}\\{file}"):
                    skippedFiles += [filePath]
                else:
                    # Rename the target file to add current timestamp
                    targetDirectory = f"{targetDirectory}\\{os.path.splitext(file)[0]}{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}{os.path.splitext(file)[1]}"
                    listOfFiles += [{"currentFilePath": filePath, "targetDirectory":targetDirectory}]
                continue

            listOfFiles += [{"currentFilePath": filePath, "targetDirectory":targetDirectory}]
            targetDirectories += [targetDirectory]    
   
    # Remove duplicate target directories
    targetDirectories = list(dict.fromkeys(targetDirectories))
    # Create any target directories if not existing
    for direcoryTree in targetDirectories:
        Path(direcoryTree).mkdir(parents=True, exist_ok=True)  

    return listOfFiles, skippedFiles          

def main():
    
    # window = tk.Tk()
    # window.geometry("700x400+30+30") 

    # # Frame to hold source and destination directories
    # fSourceDirectory = tk.Frame(window)
    # fSourceDirectory.grid(row=0, column=0)
    # fDestinationDirectory = tk.Frame(window)
    # fDestinationDirectory.grid(row=1, column=0)

    # # Source directory
    # lSourceDirectoryLabel = tk.Label(fSourceDirectory, text="Source Directory")
    # lSourceDirectoryLabel.pack(padx=5, pady=10, side=tk.LEFT)
    # eSourceDirectoryPath = tk.Entry(fSourceDirectory, state = "disabled")
    # eSourceDirectoryPath.pack(padx=5, pady=20, side=tk.LEFT)
    # bChooseSourceDirectory = tk.Button(fSourceDirectory, text="Choose")
    # bChooseSourceDirectory.pack(padx=5, pady=50, side=tk.LEFT)

    # # Destination directory
    # lDestinationDirectoryLabel = tk.Label(fDestinationDirectory, text="Destination Directory")
    # lDestinationDirectoryLabel.pack(padx=5, pady=10, side=tk.LEFT)
    # eDestinationDirectoryPath = tk.Entry(fDestinationDirectory, state = "disabled")
    # eDestinationDirectoryPath.pack(padx=5, pady=20, side=tk.LEFT)
    # bChooseDestinationDirectory = tk.Button(fDestinationDirectory, text="Choose")
    # bChooseDestinationDirectory.pack(padx=5, pady=50, side=tk.LEFT)

    # window.mainloop()

    sSourceDirectory, sDestinationDirectory = getUserInput()      

    listOfFiles, skippedFiles = getPayload(sSourceDirectory, sDestinationDirectory)
        
    # Move the files    
    for singleFile in listOfFiles:
        shutil.move(singleFile["currentFilePath"], singleFile["targetDirectory"])    

    # Print skipped files
    for singleFile in skippedFiles:
        print(singleFile)
        
if __name__ == '__main__':
    main()    