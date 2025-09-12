# Readers

Holds various classes and functions with the same contract: Path -> pd.DataFrame
All exposed through the xlReader.py module (read_safely())
Standard Pandas read capabilities extended with:

    - ForceReader: converts invalid excel extensions to xlsx
    - DirReader: reads entire directory into a single data frame

##[Unreleased]

##[Changelog]
