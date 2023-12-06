import asyncio
import random
import re

from mysql_mimic import (
    MysqlServer,
    IdentityProvider,
    NativePasswordAuthPlugin,
    Session,
    User,
)


class SecretSauceMaker:
    """
    Substitute this for an ML model, optimization function, etc.
    """
    def make_sauce(self, foo, bar):
        dates = [f'2024-{i:02d}-01' for i in range(1, 12)]
        revenue = 1000000
        out = []
        for date in dates:
            seed = date + str(foo) + str(bar)
            random.seed(seed)
            revenue += random.randrange(0, 100000)
            out.append((int(foo), bar, date, revenue))
        return out


class CustomIdentityProvider(IdentityProvider):
    def __init__(self, passwords):
        # For demonstration purposes only. See source for caveats:
        # https://github.com/kelsin/mysql-mimic/blob/main/examples/auth_native_password.py
        self.passwords = passwords

    def get_plugins(self):
        return [NativePasswordAuthPlugin()]

    async def get_user(self, username):
        password = self.passwords.get(username)
        if password:
            return User(
                name=username,
                auth_string=NativePasswordAuthPlugin.create_auth_string(password),
                auth_plugin=NativePasswordAuthPlugin.name,
            )
        return None


class SessionFactory(Session):
    def __init__(self, *args, **kwargs):
        self.sauce_maker = SecretSauceMaker()
        super().__init__(*args, **kwargs)

    async def query(self, expression, sql, attrs):
        # This is a very naive and fragile implementation, due to time constraints.
        # `expression` is a sqlglot expression, which could be parsed resiliently.
        # Please *DO NOT* parse SQL with RegEx in production.
        # For more info: https://github.com/tobymao/sqlglot
        m_foo = re.search(r'(?<=foo = )\d', str(expression))
        m_bar = re.search(r'(?<=bar = \').*(?=\')', str(expression))
        foo = m_foo.group() if m_foo else ''
        bar = m_bar.group() if m_bar else ''
        return self.sauce_maker.make_sauce(foo, bar), ["foo", "bar", "date", "revenue"]


    async def schema(self):
        return {
            "poc2": {
                "foo": "INT",
                "bar": "VARCHAR(255)",
                "date": "DATE",
                "revenue": "FLOAT",
            }
        }


if __name__ == "__main__":
    identity_provider = CustomIdentityProvider(passwords={"looker": "does_not_matter"})
    server = MysqlServer(identity_provider=identity_provider, session_factory=SessionFactory)
    asyncio.run(server.serve_forever())
