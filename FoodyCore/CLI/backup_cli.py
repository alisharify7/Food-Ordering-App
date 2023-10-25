# cli commands

import os
import datetime
from flask.cli import AppGroup
from FoodyAuth.model import User, Section
from FoodyAdmin.model import Admin, AdminLog
from FoodyOrder.model import Order, FoodList
from FoodyCore.extension import db
from FoodyConfig.config import BASE_DIR



backup_commands = AppGroup("backup", help="bckup operation commands.")


@backup_commands.command("all")
def backup_all_database():
    """
    this command make a full backup from data base and save
    """
    tables = db.metadata.tables.keys()

    backup_dir = BASE_DIR.joinpath("BackUp")
    today = str(datetime.date.today())
    backup_dir = backup_dir.joinpath(today)

    os.makedirs(backup_dir, exist_ok=True)

    for table_name in tables:
        table = db.metadata.tables[table_name]
        query = table.select()
        results = db.engine.execute(query)

        backup_file_path = os.path.join(backup_dir, f"{table_name}.csv")
        with open(backup_file_path, "w") as backup_file:
            headers = [column.name for column in table.columns]
            backup_file.write(",".join(headers) + "\n")

            for row in results:
                backup_file.write(",".join(str(value) for value in row) + "\n")

    print("Backup completed! ")

