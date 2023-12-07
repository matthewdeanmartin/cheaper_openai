"""
One off functions
"""
import json
import os
from typing import Any
import markpickle
from pydantic import BaseModel


def write_json_to_logs(obj, kind: str):
    """Write json to logs folder, with a prefix of 0001 for first run, 0002 for second run, etc."""
    base_file_name = f"logs/{str(len(os.listdir('logs'))).zfill(4)}_{kind}.json"
    file_name = os.path.join(os.path.dirname(__file__), base_file_name)
    with open(file_name, "w", encoding="utf-8", errors="backslashreplace") as f:
        if hasattr(obj, "model_dump_json"):
            dictified = json.loads(obj.model_dump_json())
            dictified = {k: v for k, v in dictified.items() if v}
            f.write(json.dumps(dictified, indent=2, cls=SetEncoder))
        else:
            dictified = json.loads(json.dumps(obj, cls=SetEncoder))
            if isinstance(dictified, dict):
                dictified = {k: v for k, v in dictified.items() if v}
            f.write(json.dumps(dictified, indent=2, cls=SetEncoder))
    if isinstance(obj, BaseModel):
        pydantic_model_to_pretty_md(obj, base_file_name.replace(".json", ".md"))
    else:
        with open(base_file_name.replace(".json", ".md"), "w", encoding="utf-8", errors="backslashreplace") as md_file:
            markpickle.dump(obj, md_file)


def show_json(obj:BaseModel):
    """Dump a pydantic model"""
    dictified = obj.model_dump()
    map_of_dict = obj.model_dump()
    for key, value in map_of_dict.items():
        if not value:
            dictified.pop(key)
    print(json.dumps(dictified, indent=2, cls=SetEncoder))


def format_pydantic_value(model_instance: BaseModel) -> str:
    """MessageContentText"""
    md_content = f"# {model_instance.__class__.__name__} Instance\n\n"
    dictified = model_instance.model_dump()
    for field_name, model_field in dictified.items(): # model_instance.__class__.model_fields.items():
        # value = getattr(model_instance, field_name)
        value = model_field
        if value:
            formatted_value = format_value(value)
            md_content += f"- **{field_name}**: {formatted_value}\n"
    return md_content


def format_value(value: Any) -> str:
    if isinstance(value, (list, tuple)):
        return ', '.join(format_value(item) for item in value)
    elif isinstance(value, dict):
        return ', '.join(f"{k}: {format_value(v)}" for k, v in value.items())
    elif isinstance(value, BaseModel):
        return format_pydantic_value(value)
    else:
        return str(value)


def pydantic_model_to_pretty_md(model_instance: BaseModel, file_name: str):
    md_content = f"# {model_instance.__class__.__name__} Instance\n\n"

    for field_name, model_field in model_instance.__class__.model_fields.items():
        value = getattr(model_instance, field_name)
        if value:
            formatted_value = format_value(value)
            md_content += f"- **{field_name}**: {formatted_value}\n"

    with open(file_name, 'w', encoding="utf-8", errors="backslashreplace") as md_file:
        md_file.write(md_content)


class SetEncoder(json.JSONEncoder):
    # https://stackoverflow.com/a/8230505/33264
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)