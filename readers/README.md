# xlReader.safe_reader()

Safe Reader is the solution to
- performance issues on network file reading
- preservation of original file
- invalid extension, unable to read files

safe_reader copies a file or entire directory to
local temp folder and reads from there. if unable
to read a file (csv and xlsx supported through pandas)
safe_reader will attempt to open and save the file as
xlsx in a temp location and read from there.

single file: safe_reader will return pd.Dataframe
dir: safe_reader will return list of frames OR 
single pd.Dataframe if stack = True

## How to use

from xlReader import safe_reader

1. for all files in a directory 

2. for single file

Features:
    - force reader(convert invalid file types to xlsx, then read)


##[Unreleased]
- Stack frames
- Cfg for pandas arg options
- 

##[Changelog]
