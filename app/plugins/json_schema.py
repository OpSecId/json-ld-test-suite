from jsonschema import validate
import requests


class JsonSchemaValidator:
    def test_schema(document, schema):
        checks = {}
        schemas = (
            document["credentialsSchema"]
            if isinstance(document["credentialsSchema"], list)
            else [document["credentialsSchema"]]
        )
        for schema in schemas:
            r = requests.get(schema["id"])
            schema = r.json()
            checks[schema["id"]] = validate(instance=document, schema=schema)
        return checks
