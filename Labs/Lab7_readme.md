# Lab 7 - Working with 7-Zip Archives

Hi, today I'll show you how to use py7zr, a python package for 7zip file archiving, in python.
Remember to replace "/path/to/file" with the actual file path you want to archive, and ensure you adapt the paths and filenames to your specific desire.

## Step 1. Set Up a Virtual Environment

 - Create a virtual environment named "7zipper" by running the following commands. You can choose the name that best suits your project:

         virtualenv ~/venv/7zipper
         .\~\venv\7zipper\Scripts\activate
         pip install py7zr
    

## Step 2.  Python Environment Setup

 - Enter the Python environment by typing `python` in your terminal.

## Step 3: Create a 7-Zip Archive

 - Use the `py7zr` library to create a 7-Zip archive. Replace "/path/to/file" with the actual file you want to archive:

        from py7zr import SevenZipFile
        import os
        archive_name = os.path.expanduser("~/Documents/testZip.7z")
        with SevenZipFile(archive_name, 'w') as archive:
	        archive.write("/path/to/file")

 - Press `Enter` once reaching the ellipse to complete the operation

## Step 4: Extract the 7-Zip Archive

 - Extract the contents of the 7-Zip archive to a target directory:

        target_directory = os.path.join(os.path.expanduse("~/Documents"), "ExtractedFiles") 
        with SevenZipFile(archive_name, 'r') as archive:
	        archive.extractall(path=target_directory)

 - Again, press`Enter` once reaching the ellipse to complete the operation

## Step 5: Retrieve Archive Information
- Obtain information about the 7-Zip archive, such as the file name, compression details, and more:

      with SevenZipFile(archive_name, 'r') as archive: archive_info = archive.list()
        fileInfo = dir(archive_info)
        print(fileInfo.fileName)
        print(fileInfo.compressed)
        print(fileInfo.uncompressed)

 - Again, press`Enter` once reaching the ellipse to complete the operation

## Step 6: Deactivate the Virtual Environment

- After you have completed your work, deactivate the virtual environment:
`deactivate
`
