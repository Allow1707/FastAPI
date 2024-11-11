from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    db_url: str


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        db_url=env("DB_URL")
    )