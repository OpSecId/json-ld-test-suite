from app.test_suites import validations as valid
from rfc3986_validator import validate_rfc3986


class VcDataModelTests:
    def __init__(self, document):
        self.document = document

    def context_exists(self):
        return "passed" if "@context" in self.document else "failed"

    def context_terms_are_understood(self):
        return "unknown"

    def context_is_list_and_has_base_url(self):
        return (
            "passed"
            if (
                "@context" in self.document
                and (
                    isinstance(self.document["@context"], list)
                    and self.document["@context"][0] == "https://www.w3.org/ns/credentials/v2"
                )
            )
            else "failed"
        )

    def context_contains_only_strings_or_objects(self):
        return (
            "passed"
            if (
                "@context" in self.document 
                and (valid.context_item(item)
                for item in self.document["@context"][1:])
            )
            else "failed"
        )
        
    def has_type(self):
        return True if 'type' in self.document else False
    
    def type_to_array(self):
        return self.document['type'] if isinstance(self.document['type'], list) else [self.document['type']]
        
    def vc_has_valid_id(self):
        return self.valid_id_value(self.document['id']) if 'id' in self.document else 'skipped'
        
    def valid_id_value(self, object_id):
        return (
            'passed'
            if (isinstance(object_id, str)
            and
            validate_rfc3986(object_id))
            else 'failed'
        )
        
    def vc_type_exists(self):
        return (
            'passed'
            if ('type' in self.document and self.document['type'])
            else 'failed'
        )
        
    def vc_type_is_valid(self):
        if not self.has_type():
            return 'failed'
        vc_types = self.type_to_array()
        return (
            'passed'
            if (isinstance(item, str) for item in self.document['type'])
            else 'failed'
        )
        
    def valid_type(self, object_type):
        object_types = object_type if isinstance(object_type, list) else [object_type]
        return (
            'passed'
            if (isinstance(item, str) for item in object_types)
            else 'failed'
        )
        
    def vc_type_includes_required_type(self):
        if not self.has_type():
            return 'failed'
        vc_types = self.type_to_array()
        return (
            'passed'
            if 'VerifiableCredential' in vc_types
            else 'failed'
        )
        
    def issuer_to_id(self):
        if 'issuer' not in self.document:
            return None
        issuer = self.document['issuer']
        if isinstance(issuer, str):
            return issuer
        elif isinstance(issuer, dict):
            return issuer['id'] if 'id' in issuer else None
        return None
        
    def vc_has_issuer(self):
        return (
            'passed'
            if 'issuer' in self.document
            else 'failed'
        )
        
    def vc_issuer_is_valid(self):
        issuer = self.issuer_to_id()
        if issuer:
            return (
                'passed'
                if validate_rfc3986(issuer)
                else 'failed'
            )
        return 'failed'
