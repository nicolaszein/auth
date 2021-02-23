import datetime
import uuid

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, String, Table)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapper, relationship

from auth.infrastructure.database.database import Database
from auth.infrastructure.entity.activation import Activation
from auth.infrastructure.entity.session import Session
from auth.infrastructure.entity.user import User

db = Database()

user_table = Table(
    'user',
    db.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('full_name', String(255), nullable=False),
    Column('email', String(255), nullable=False, unique=True),
    Column('password', String(), nullable=False),
    Column('is_active', Boolean(), nullable=False, default=False),
    Column(
        'created_at',
        DateTime(),
        nullable=False,
        default=datetime.datetime.utcnow
    ),
    Column(
        'updated_at',
        DateTime(),
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow
    ),
)

mapper(User, user_table, properties={
    'activations': relationship(Activation, lazy='joined', innerjoin=True)
})

activation_table = Table(
    'activation',
    db.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False, index=True),
    Column('code', String(255), nullable=False, unique=True),
    Column(
        'created_at',
        DateTime(),
        nullable=False,
        default=datetime.datetime.utcnow
    ),
)

mapper(Activation, activation_table, properties={
    'user': relationship(User, lazy='joined', innerjoin=True)
})

session_table = Table(
    'session',
    db.metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('user_id', UUID(as_uuid=True), ForeignKey('user.id'), nullable=False, index=True),
    Column('refresh_token', String(1000), nullable=False, unique=True, index=True),
    Column(
        'created_at',
        DateTime(),
        nullable=False,
        default=datetime.datetime.utcnow
    ),
)

mapper(Session, session_table, properties={
    'user': relationship(User, lazy='joined', innerjoin=True)
})
