import os
import json

from db_manage.mysql_connector.db_connector import DBConnector
from db_manage.values import schemas_path



class Database:
    def __init__(self, name):
        self.name = name
        self.schemas = os.path.join(f"{schemas_path}", f"{name}.json")
        self.init()

    def init(self):
        with DBConnector() as db:
            db.create_db_if_doest_exist(self.name)
        with DBConnector(self.name) as db:
            db.create_tables_if_dont_exist(self.schemas)

    def add_object(self, object_type, data):
        with DBConnector(self.name) as db:
            id = db.write_row(object_type, data)
            return id

    def get_list_of_objects(self, object_type, conditions={}, inJson=False):
        objs = []
        with DBConnector(self.name) as db:
            rows = db.get_rows(object_type, conditions)
        if inJson:
            return rows
        command_str = self.create_class(object_type)
        for row in rows:
            exec(f"{command_str}\nobjs.append({object_type}(row))")
        return objs
    
    def get_filtered_list_of_objects(self, object_type, filter="", include_columns=[], exclude_columns=[], inJson=False):
        objs = []
        with DBConnector(self.name) as db:
            if include_columns:
                columns = include_columns
            else:
                columns = db.get_tables_columns(object_type)
                exclude_columns.append("id")
                for column in exclude_columns:
                    if column in columns:
                        columns.remove(column)
            rows = db.filter_table(object_type, columns, filter)
        if inJson:
            return rows
        command_str = self.create_class(object_type)
        for row in rows:
            exec(f"{command_str}\nobjs.append({object_type.title()}(row))")
        return objs

    def get_object_by_id(self, object_type, id, inJson=False):
        with DBConnector(self.name) as db:
            row = db.get_row(object_type, {"id": id})
        if inJson:
            return row
        if row:
            return self.get_class(object_type, row)
        return row
    
    def update_object(self, object_type, id, data):
        with DBConnector(self.name) as db:
            row = db.update_row(object_type, id, data)

    def delete_object(self, object_type, id):
        with DBConnector(self.name) as db:
            row = db.delete_row(object_type, id)


    def create_class(self, class_name):
        class_name = class_name
        command_str = f"class {class_name}:\n\t"
        command_str += f"def __init__(self, data):\n\t\t"
        with open(f"{self.schemas}", 'r') as f:
            object_schema = json.loads(f.read())[class_name]
        command_str += f"self.id = data[\"id\"]\n\t\t"
        for attr in object_schema.keys():
            command_str += f"self.{attr} = data[\"{attr}\"] if \"{attr}\" in data else None\n\t\t"
        return command_str
        

    def get_class(self, class_name, data):
        obj = []
        command_str = self.create_class(class_name)
        exec(f"{command_str}\nobj.append({class_name}(data))")
        return obj[0]