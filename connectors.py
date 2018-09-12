from sqlalchemy import create_engine


class Connector:
    engine = None

    def __init__(self, theme, host, port, user, password, database):
        self.connection_string = '{}://{}:{}@{}:{}/{}'.format(theme, user, password, host, port, database)

    def get_engine(self):
        if self.engine is None:
            self.engine = create_engine(self.connection_string)
        return self.engine

