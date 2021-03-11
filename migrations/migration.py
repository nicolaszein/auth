from alembic import command
from alembic.config import Config

from auth.settings import DATABASE_URL


def handle(event, context):
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', '.')
    alembic_cfg.set_main_option('sqlalchemy.url', DATABASE_URL)
    command.upgrade(alembic_cfg, 'head')
