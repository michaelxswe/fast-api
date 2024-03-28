from setup import create_app
from config.settings import Settings

app = create_app(settings=Settings())  # type: ignore
