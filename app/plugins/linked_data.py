from deepdiff import DeepDiff, grep
from pyld import jsonld
from rfc3986_validator import validate_rfc3986
from pprint import pprint


class JsonLdProcessorException(Exception):
    """Base exception for JSON-LD Processor."""

    def __init__(self, error: dict):
        self.error = error


class JsonLdProcessor:
    """JSON-LD Processor."""

    def __init__(self, document: dict = None, timeout: int = 100) -> None:
        """Initialize new JsonLdProcessor instance."""
        jsonld.set_document_loader(jsonld.requests_document_loader(timeout=timeout))
        self.document = document

    def validate_context(self):
        try:
            self.compact()
            return True
        except JsonLdProcessorException as err:
            return err.error

    def find_undefined_terms(self):
        pass

    def find_undefined_properties(self):
        """Find undefined properties."""
        undefined_properties = list()
        try:
            diff = DeepDiff(self.document, self.compact())
        except JsonLdProcessorException as err:
            return err.error
        if "dictionary_item_removed" in diff:
            for item in diff["dictionary_item_removed"]:
                """
                Extract the last element of the path as the undefined property.
                """
                item = item.split("['")[-1].strip("']'")
                undefined_properties.append(item)

        if "type_changes" in diff:
            for item in diff["type_changes"]:
                """
                If a VC object only contains `id` and no other defined terms, 
                the object will be transformed into the id value.
                
                Here we detect if an object was changed from a dict 
                and drop the `id` value of the original dict to see which
                undefined properties were silently dropped if any.
                """
                if diff["type_changes"][item]["old_type"] == dict:
                    diff["type_changes"][item]["old_value"].pop("id", None)
                    for property in diff["type_changes"][item]["old_value"]:
                        undefined_properties.append(property)
        return undefined_properties

    def find_undefined_types(self):
        """Find undefined types."""
        undefined_types = list()
        try:
            type_query = self.expand() | grep("@type", verbose_level=2)
        except JsonLdProcessorException as err:
            return err.error

        if "matched_paths" in type_query:
            for type_entry in type_query["matched_paths"]:
                for item in (
                    [type_query["matched_paths"][type_entry]]
                    if isinstance(type_query["matched_paths"][type_entry], str)
                    else type_query["matched_paths"][type_entry]
                ):
                    if not validate_rfc3986(item):
                        """
                        We identify types that don't get compacted into a URI as undefined.
                        """
                        undefined_types.append(item)
        return undefined_types

    def compact(self):
        try:
            return jsonld.compact(self.document, self.document["@context"])
        except jsonld.JsonLdError as e:
            error = {}
            if e.cause:
                error["type"] = e.cause.type
                error["code"] = e.cause.code
            if "type" in error and error["type"] == "jsonld.InvalidUrl":
                error["url"] = e.cause.details["url"]
            elif "type" in error and error["type"] == "jsonld.SyntaxError":
                error["details"] = e.cause.details
            # else:
            #     error['details'] = e.cause.details
            raise JsonLdProcessorException(error=error)

    def expand(self):
        try:
            return jsonld.expand(self.document)
        except jsonld.JsonLdError as e:
            error = {}
            if e.cause:
                error["type"] = e.cause.type
                error["code"] = e.cause.code
            if "type" in error and error["type"] == "jsonld.InvalidUrl":
                error["url"] = e.cause.details["url"]
            elif "type" in error and error["type"] == "jsonld.SyntaxError":
                error["details"] = e.cause.details
            # else:
            #     error['details'] = e.cause.details
            raise JsonLdProcessorException(error=error)

    def flatten(self):
        try:
            return jsonld.flatten(self.document)
        except jsonld.JsonLdError as e:
            error = {}
            if type(e.cause) == jsonld.JsonLdError:
                error["type"] = e.cause.type
                error["code"] = e.cause.code
            raise JsonLdProcessorException()

    def frame(self, frame):
        try:
            return jsonld.frame(self.document, frame)
        except jsonld.JsonLdError as e:
            error = {}
            if type(e.cause) == jsonld.JsonLdError:
                error["type"] = e.cause.type
                error["code"] = e.cause.code
            raise JsonLdProcessorException()

    def normalize(self):
        return jsonld.normalize(
            self.document, {"algorithm": "URDNA2015", "format": "application/n-quads"}
        )
