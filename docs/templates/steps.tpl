{% for step_type in steps_by_types %}
# {{ step_type.name | capitalize }}

Module: `{{ step_type.module }}`

{% for step in step_type.base_steps %}
### {{ step.func_name }}

{{ prepare_docstring(step.class.__doc__) }}

Matcher:
```
{{ step.class.sentence }}
```

{% endfor %}

{% endfor %}
