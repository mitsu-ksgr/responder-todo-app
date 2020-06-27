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

from app.helpers.session_helper import is_logged_in


def redirect_to(resp, location, status_code=301):
    resp.status_code = status_code
    resp.text = f"Redirecting to: {location}"  # TODO: to optional
    resp.headers.update({"Location": location})


def jinja2_template(resp, template_name):
    template_paths = [str(Path(os.path.abspath("app/templates")))]

    # see: https://responder.kennethreitz.org/en/latest/_modules/responder/api.html#API.template
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_paths, followlinks=True),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
    )
    template = jinja_env.get_template(template_name)

    # Add globals
    template.globals["isLogin"] = lambda: is_logged_in(resp)

    return template


def render_template(resp, template_name, **values):
    template = jinja2_template(resp, template_name)
    return template.render(**values)
