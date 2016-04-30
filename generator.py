# -*- coding: utf-8 -*-
import sys
import os
import re
sys.path.append('../')  # noqa

from jinja2 import Template

from cli_bdd.core.steps import (
    command,
    environment,
    file as file_steps,
)


BASE_PATH = os.path.dirname(os.path.normpath(__file__))
TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates')


STEPS_MODULES = [
    command,
    environment,
    file_steps,
]


def _prepare_docstring(value):
    if not value:
        return ''
    remove_spaces = 0
    for line in value.split('\n')[1:]:
        if line:
            for char in line:
                if char != ' ':
                    break
                else:
                    remove_spaces += 1
            break

    return re.sub(
        r'^ {%s}' % remove_spaces,
        '',
        unicode(value),
        flags=re.MULTILINE
    ).strip()


def _render_and_save_template(path, dest, context):
    template_path = os.path.join(TEMPLATES_PATH, path + '.tpl')
    destination_path = os.path.join(BASE_PATH, dest + '.md')
    with open(destination_path, 'wt') as dest_file:
        dest_file.write(
            Template(open(template_path).read()).render(context)
        )


def generate_api_reference():
    generate_steps_reference()


def generate_steps_reference():
    steps_by_types = []

    for step_module in STEPS_MODULES:
        name = step_module.__name__.split('.')[-1]
        steps_by_types.append({
            'name': name,
            'module': step_module.__name__,
            'base_steps': step_module.base_steps
        })

    steps_dir = os.path.join(BASE_PATH, 'steps/')
    if not os.path.exists(steps_dir):
        os.makedirs(steps_dir)

    for step_type in steps_by_types:
        _render_and_save_template(
            'steps',
            'steps/' + step_type['name'],
            {
                'step_type': step_type,
                'prepare_docstring': _prepare_docstring
            }
        )
