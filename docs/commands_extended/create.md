## Examples

### Creating a New Collection

Using the command with a collection name:
```bash
python src/main.py create -f my_folder -c my_collection
```

Alternative syntax with full parameter names:
```bash
python src/main.py create --folder my_folder --collection my_collection
```

This will create a collection named `my_collection` using the files in `input/my_folder`.

### Overwriting an Existing Collection

To overwrite an existing collection, use the `-o` or `--overwrite` flag:

```bash
python src/main.py create -f my_folder -o
```

With a specific collection name:
```bash
python src/main.py create -f my_folder -c my_collection -o
```

Using full parameter names:
```bash
python src/main.py create --folder my_folder --collection my_collection --overwrite
```

These commands will overwrite the existing collection if it already exists, using the files from `input/my_folder`.

## Notes

### General Setup

- The collection folder must be placed in the `input` directory.
- The input folder must contain:

    - A `collection.json` file that describes the collection
    - The corresponding layer files (.tif)

- The `collection.json` must follow the specification described in `spec/collection.md`.
- Use `collection.example.json` as a template for creating your collection configuration.

### Command Behavior
- If no collection name is provided with `-c`, the `id` from collection.json will be used.
- Without the `-o` flag, the command will fail if the collection already exists.
- With `-o` flag, any existing collection with the same name will be completely replaced.
- The folder must contain valid STAC assets.
- This command does not validate items, only the collection structure.
- You can combine this command with validate after creation for consistency checks.

