import importlib

from db_manage.mysql_connector.database import Database


def write_pipeline_to_db(pipeline_info):
    db = Database("Pipeline")
    pipeline_type = pipeline_info["pipeline_type"]
    del pipeline_info["pipeline_type"]
    pipeline_instance_id = db.add_object(pipeline_type, pipeline_info)
    pipeline_id = db.add_object("Pipeline", {"pipeline_type": pipeline_type,
                                             "pipeline_id": pipeline_instance_id})
    return pipeline_id

def create_pipeline(pipeline_id, service):
    pipeline = get_pipeline_obj(pipeline_id)
    pipeline.create_pipeline(service)
    return pipeline_id

def trigger_pipeline(pipeline_id, pipeline_name):
    pipeline = get_pipeline_obj(pipeline_id)
    pipeline.trigger_pipeline(pipeline_name)

def get_host(pipeline_id):
    pipeline = get_pipeline_obj(pipeline_id)
    return pipeline.connector["host"]


#############

def get_pipeline_obj(pipeline_id):
    db = Database("Pipeline")
    pipeline_info = db.get_object_by_id("Pipeline", pipeline_id)
    pipeline_type = pipeline_info.pipeline_type
    module = importlib.import_module(f"service_arms.pipeline.pipeline_types.{pipeline_type}")
    pipeline = getattr(module, pipeline_type)(pipeline_info.pipeline_id)
    return pipeline