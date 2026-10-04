from typing import cast
from flask import Flask, Response, g
from flask_jwt_extended import JWTManager
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

class ORMapper:
    def __init__(self, app: Flask|None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        self.engine: Engine = create_engine(
            url=app.config['ORM_ENGINE_URL'], **app.config['ORM_ENGINE_OPTIONS']
        )
        self.sessionmaker: sessionmaker[Session] = sessionmaker(bind=self.engine)
        app.teardown_appcontext(self.remove_session)
        app.extensions['orm'] = self

    @property
    def session(self) -> Session:
        if 'orm_session' not in g:
            g.orm_session = self.sessionmaker()
        return cast(Session, g.orm_session)

    @staticmethod
    def remove_session(e: BaseException|None = None) -> None:
        session: Session|None = g.pop('orm_session', default=None)
        if session is not None:
            session.close()

class NoResBody:
    def __init__(self, app: Flask|None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.after_request(self.fix_headers)
        app.extensions['no_res_body'] = self

    @staticmethod
    def fix_headers(response: Response) -> Response:
        if response.status_code == 201 and response.get_data() == b'':
            response.headers.pop('Content-Type', default=None)
        if response.status_code == 204:
            response.headers.pop('Content-Type', default=None)
            response.headers.pop('Content-Length', default=None)
        return response

orm = ORMapper()
jwt = JWTManager()
no_res_body = NoResBody()

extensions: tuple[ORMapper, JWTManager, NoResBody] = (orm, jwt, no_res_body)
