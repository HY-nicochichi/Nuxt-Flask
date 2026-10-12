from typing import cast
from flask import Flask, Response, jsonify, g
from flask_jwt_extended import JWTManager
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from werkzeug.exceptions import HTTPException

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

class ResProcessor:
    class Res(Response):
        default_mimetype = None

    def __init__(self, app: Flask|None = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        app.register_error_handler(HTTPException, self.jsonify_http_exc)
        app.extensions['res_proc'] = self

    @staticmethod
    def jsonify_http_exc(e: HTTPException) -> tuple[Response, int]:
        return jsonify(msg=e.name), e.code or 500

orm = ORMapper()
jwt = JWTManager()
res_proc = ResProcessor()

extensions: tuple[ORMapper, JWTManager, ResProcessor] = (orm, jwt, res_proc)
