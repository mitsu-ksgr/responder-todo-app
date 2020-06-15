
from sqlalchemy.exc import SQLAlchemyError

import app.db_helper
from app.api_helper import redirect_to, render_template
from app.models.user import User


# /users
class UsersController:
    # shows all users
    async def on_get(self, req, resp):
        session = app.db_helper.session()
        users = session.query(User).all()
        resp.html = render_template('users/index.html', users=users)

    # Add new user
    async def on_post(self, req, resp):
        session = app.db_helper.session()
        params = await req.media()

        # TODO add validation
        if not 'name' in params:
            users = session.query(User).all()
            resp.html = render_template('users/index.html',
                users=users, messages=["Name can't be blank"])
            return

        try:
            user = User(
                name = params["name"],
                profile = params.get('profile', ''))
            session.add(user)
            session.commit()
        except SQLAlchemyError as e:
            print(e)
            session.rollback()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
        # TODO: i want add flash message
        redirect_to(resp, '/users')

# /user/{idx}
class UserController:
    async def on_get(self, req, resp, *, idx):
        pass

    async def on_patch(self, req, resp, *, idx):
        pass

    async def on_delete(self, req, resp, *, idx):
        pass

