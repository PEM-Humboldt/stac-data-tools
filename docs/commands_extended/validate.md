## Examples

### Basic Validation
Using folder name only:
```bash
python src/main.py validate -f my_folder
```

Using full parameter names:
```bash
python src/main.py validate --folder my_folder
```

### Validation with Collection Name
```bash
python src/main.py validate -f my_folder -c my_collection
```

This will validate the collection files in `input/my_folder` without uploading them.

## Notes

### General Setup

- The collection folder must be placed in the `input` directory.
- The input folder must contain:

    - A `collection.json` file that describes the collection
    - The corresponding layer files (.tif)

- The `collection.json` must follow the specification described in `spec/collection.md`.

### Command Behavior
- This command validates without uploading or modifying any data.
- If no collection name is provided with `-c`, the `id` from collection.json will be used.
- The command performs comprehensive validation of the collection structure.
- Use this command before creating/updating collections to ensure data integrity.