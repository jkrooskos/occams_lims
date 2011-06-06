from sqlalchemy import *
from migrate import *


metadata = MetaData()

new_columns = (
    Column(
        'from_state_id',
        ForeignKey('specimen_aliquot_term.id', ondelete='CASCADE'),
        nullable=False,
        ),
    Column(
        'to_state_id',
        ForeignKey('specimen_aliquot_term.id', ondelete='CASCADE'),
        nullable=False,
        ),
    Column('action_date', DateTime, nullable=False),
    Column('create_date', DateTime, nullable=False),
    Column('create_name', Unicode, nullable=False)
    )

old_columns = (
    Column(
        'state_id',
        ForeignKey('specimen_aliquot_term.id', ondelete='CASCADE'),
        nullable=False,
        ),
    Column('action_date', DateTime, nullable=False),
    Column('to', Unicode, nullable=False)
    )


def upgrade(migrate_engine):
    """ Introduces new changes to the specimen/aliquot/terms table necessary
        for inventory processing.
    """
    metadata.bind = migrate_engine
    vocabulary_table = Table('specimen_aliquot_term', metadata, autoload=True)
    history_table = Table('aliquot_history', metadata, autoload=True)

    for column in old_columns:
        column.drop(history_table)
    for column in new_columns:
        column.create(history_table)


def downgrade(migrate_engine):
    metadata.bind = migrate_engine
    vocabulary_table = Table('specimen_aliquot_term', metadata, autoload=True)
    history_table = Table('aliquot_history', metadata, autoload=True)

    for column in new_columns:
        column.drop(history_table)
    for column in old_columns:
        column.create(history_table)
