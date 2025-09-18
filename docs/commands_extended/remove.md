## Examples

### Remove by Collection Name
```bash
python src/main.py remove -c my_collection
```

Using full parameter name:
```bash
python src/main.py remove --collection my_collection
```

This will remove the collection `my_collection` from both STAC and Azure storage.

## Notes

### Command Behavior

- This command removes the collection from both:

    - The STAC catalog
    - Azure Blob Storage

- The operation cannot be undone
- The collection name parameter (-c/--collection) is required
- Make sure to have proper backup before removing collections
- Ensure you have the correct permissions in both STAC and Azure

### Best Practices
- Validate the collection name before removal
- Consider creating a backup before removing important collections
- Double-check the collection name to avoid accidental deletions