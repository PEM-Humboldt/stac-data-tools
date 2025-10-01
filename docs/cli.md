# {{ cli.title }}

{{ cli.description }}

## Commands

{% for cmd in cli.commands %}
---
### {{ cmd.name }} — {{ cmd.title }}

{{ cmd.description }}

#### Usage
```bash
{{ cmd.usage }}
```

#### Parameters
{% if cmd.params %}
{% for p in cmd.params -%}
- `{{ p.flags }}` {% if p.required %}(required){% else %}(optional){% endif %}: {{ p.desc }}
{% endfor %}
{% else %}
_No parameters_
{% endif %}

{% if cmd.examples %}
#### Examples
```bash
{% for ex in cmd.examples -%}
{{ ex }}
{% endfor -%}
```
{% endif %}

{% endfor %}
