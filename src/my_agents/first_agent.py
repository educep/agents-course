from config.settings import settings


def main():
    print(settings.model_dump())
