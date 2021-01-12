# Sylphid Core

# Templates

Sylphid's template system provides a very simple way of creating nested templates. This can be useful for defining
filesystem paths or scenegraph locations.

## Example

```python
import sylphid_core.context as syl_context
import sylphid_core.templates as syl_templates

context = syl_context.from_short_path("/aCoolProject/char")

templates = syl_templates.resolve_references(
    {
        "root": "/projects",
        "project": "<root>/{project}",
        "sequence": "<project>/sequences/{sequence}"
    }
)

project_root = templates["sequence"].format(**context)
```

## Parsing

Some systems offer parsing in their template systems, but personal experience has led me to believe this creates as many
problems as it solves. 

- Parsing gets complex quickly.
- Templates may change over time, meaning today's template may not work on yesterdays' path.
- Databases are better places for storing data.

Put simply if data is of production importance it should be in a database.