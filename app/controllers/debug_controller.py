from config import app_config


# /debug
class DebugController:
    async def on_get(self, req, resp):
        txt = ""
        txt += "* Environtment\n"
        txt += f"Env: {app_config.env}\n"
        txt += "\n"
        txt += "* Database Connection\n"
        txt += f"Dialect: {app_config.get('db', 'dialect')}\n"
        txt += f"Driver: {app_config.get('db', 'driver')}\n"
        txt += f"Host: {app_config.get('db', 'host')}\n"
        txt += f"Port: {app_config.get('db', 'port')}\n"
        txt += f"User Name: {app_config.get('db', 'username')}\n"
        txt += f"URL: {app_config.get('db', 'url')}\n"
        txt += "\n"
        txt += "* Requests\n"
        txt += f"session = {req.session}\n"
        txt += f"cookies = {req.cookies}\n"
        txt += "\n"
        txt += "* Response\n"
        txt += f"session = {resp.session}\n"
        txt += f"cookies = {resp.cookies}\n"
        txt += "\n"
        resp.text = txt
