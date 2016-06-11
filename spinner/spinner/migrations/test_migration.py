from playhouse.migrate import *  # @UnusedWildImport
from spinner.models import db

# SQLite example:

migrator = SqliteMigrator(db)

origin_id = IntegerField(null=True)

with db.transaction():
    migrate(
        #migrator.add_column('spideritem', 'origin_id', origin_id),
        migrator.drop_column('spideritem', 'region_id'),    
    )   