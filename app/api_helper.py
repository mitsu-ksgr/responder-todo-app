#
# API Helper
#
# Provides functions similer to part of responder.api without depending an api instance.
#
# - https://responder.kennethreitz.org/en/latest/_modules/responder/api.html
#

import os
from pathlib import Path

import jinja2


def redirect_to(resp, location):
    resp.status_code = 301
    resp.text = f"Redirecting to: {location}"  # TODO: to optional
    resp.headers.update({"Location": location})


def render_template(template_name, **values):
    # TODO: read app_config
    template_paths = [str(Path(os.path.abspath("app/templates")))]

    # see: https://responder.kennethreitz.org/en/latest/_modules/responder/api.html#API.template
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_paths, followlinks=True),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    template = jinja_env.get_template(template_name)
    return template.render(**values)
