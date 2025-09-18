## Examples

### Basic Injection with Backup
```bash
python src/main.py inject -f my_folder
```

### Injection without Backup
```bash
python src/main.py inject -f my_folder --no-backup
```

Using full parameter names:
```bash
python src/main.py inject --folder my_folder --no-backup
```

## Notes

### Process Overview
The inject command:
1. Reads the `collection.json` from `input/<folder>`
2. Replaces the "items" section using the `.tif` files in that folder
3. Preserves all other collection information
4. Generates an updated `collection.json`

### File Requirements

- The collection folder must be in the `input` directory
- `.tif` files must include in their name either:

    - A year (e.g., `2005`)
    - A period (e.g., `2000_2005` or `2000-2005`)

- The folder must contain a valid `collection.json` file

### Command Behavior
- By default, creates a backup of the original `collection.json`
- Use `--no-backup` to skip backup creation
- Fails if duplicate years/periods are found in file names
- The resulting `collection.json` is ready for collection creation/update

### Best Practices
- Always review the generated `collection.json` after injection
- Keep backups of important collections
- Validate the collection after injection
- Use consistent naming patterns for your .tif files