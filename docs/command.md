# {{ command().title }}

{{ command().description }}

{% if command().examples %}
## Ejemplos

{% for example in command().examples %}
---
### {{ example.name }}

{% for description in example.descriptions %}

{% if description.text %}

{{ description.text }}

{% endif %}

{% if description.cmd %}

```sh
{{ description.cmd }}
```

{% if description.footer %}

{{ description.footer }}

{% endif %}

{% endif %}

{% endfor %}

{% endfor %}

{% endif %}

{% if command().notes %}

## Notas

{% for note in command().notes %}

### {{ note.title }}

{{ note.description }}

{% endfor %}

{% endif %}