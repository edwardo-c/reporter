### [Unreleased]
- convert entire directory to single data frame safely
- Price List csv reader with YAML instruction
    - read env with dotenv
    - YAML must have place holders for safe directories
    - create the 700 csvs locally, move using robocopy

### [Released]
- SafeReader is no longer a class. State was not needed, can now be injected into any valid reader