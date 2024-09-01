from app.test_suites.base_suite import BaseTestSuite
from app.test_suites import validations as valid
from .vc_data_model_tests import VcDataModelTests
from pprint import pprint


class VcDataModelTestSuite(BaseTestSuite):
    """
    VC Data Model Test Suite
    https://w3c.github.io/vc-data-model/
    """

    def run(self):
        # Store a copy of the VC
        self.assertions = VcDataModelTests(self.vc.copy())
        self.reporter.attachments.append(self.assertions.document)

        # Initialize and run Test Suite
        self._create_parent_suite("Verifiable Credentials Data Model v2.0")
        self._basic_concepts()
        # self._advanced_concepts()
        self.reporter.parent_suites.append(self.parent_suite)

        # End test suite, export results and generate new report
        # self._export_results()
        results = {}
        # print(self.reporter.tests)
        # for test in self.reporter.tests:
        #     pprint(test)
        #     results[test["name"]] = [
        #         {"statement": test["name"], "check": test["status"]}
        #         # for step in self.reporter.steps
        #         # if step["uuid"] in test["children"]
        #     ]
        for suite in self.reporter.sub_suites:
            results[suite["name"]] = [
                {"assertion": test["name"], "check": test["status"]}
                for test in self.reporter.tests
                if test["uuid"] in suite["children"]
            ]
        return results

    def _basic_concepts(self):
        self._create_suite("Basic Concepts")
        # self._verifiable_credentials()
        self._contexts()
        self._identifiers()
        self._types()
        # self._names_and_descriptions()
        self._issuer()
        # self._credential_subject()
        # self._validity_period()
        # self._status()
        # self._data_schemas()
        # self._securing_mechanisms()
        # self._verifiable_presentations()
        self.reporter.suites.append(self.suite)

    def _contexts(self):
        self._create_sub_suite("Contexts")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#contexts",
        }
        attachments = {
            "Document": self.vc,
            "$.@context": self.vc["@context"] if "@context" in self.vc else None,
        }
        self.reporter.attachments.append(attachments["$.@context"])

        self._create_test(
            "Verifiable credentials and verifiable presentations MUST include a @context property.",
            self.assertions.context_exists(),
        )

        self._create_test(
            "Application developers MUST understand every JSON-LD context used by their application, at least to the extent that it affects the meaning of the terms used by their application.",
            self.assertions.context_terms_are_understood(),
        )

        self._create_test(
            "The value of the @context property MUST be an ordered set where the first item is a URL with the value https://www.w3.org/ns/credentials/v2.",
            self.assertions.context_is_list_and_has_base_url(),
        )

        self._create_test(
            "Subsequent items in the ordered set MUST be composed of any combination of URLs and objects, where each is processable as a JSON-LD Context.",
            self.assertions.context_contains_only_strings_or_objects(),
        )
        self.reporter.sub_suites.append(self.sub_suite)

    def _identifiers(self):
        self._create_sub_suite("Identifiers")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#identifiers",
        }
        attachments = {"Document": self.vc}

        self._create_test(
            "If present, id property's value MUST be a single URL.",
            self.assertions.vc_has_valid_id(),
        )
        self.reporter.sub_suites.append(self.sub_suite)

    def _types(self):
        self._create_sub_suite("Types")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#types",
        }
        attachments = {"Document": self.vc}

        self._create_test(
            "Verifiable credentials and verifiable presentations MUST contain a type property with an associated value.",
            self.assertions.vc_type_exists(),
        )
        self._create_test(
            "The value of the type property MUST be one or more terms and absolute URL strings.",
            self.assertions.vc_type_is_valid(),
        )
        self._create_test(
            "Verifiable credential object MUST have a type VerifiableCredential and, optionally, a more specific verifiable credential type.",
            self.assertions.vc_type_includes_required_type(),
        )
        self.reporter.sub_suites.append(self.sub_suite)

    def _names_and_descriptions(self):
        self._create_sub_suite("Names and Descriptions")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#names-and-descriptions",
        }
        attachments = {"Document": self.vc}
        pass

    def _issuer(self):
        self._create_sub_suite("Issuer")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#issuer",
        }
        attachments = {
            "Document": self.vc,
            "$.issuer": self.vc["issuer"] if "issuer" in self.vc else None,
        }
        self._create_test(
            "A verifiable credential MUST have an issuer property.",
            self.assertions.vc_has_issuer(),
        )
        self._create_test(
            "The value of the issuer property MUST be either a URL or an object containing an id property whose value is a URL.",
            self.assertions.vc_issuer_is_valid(),
        )
        self.reporter.sub_suites.append(self.sub_suite)

    def _credential_subject(self):
        self._create_sub_suite("Credential Subject")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#credential-subject",
        }
        attachments = {
            "Document": self.vc,
            "$.credentialSubject": self.vc["credentialSubject"]
            if "credentialSubject" in self.vc
            else None,
        }
        pass

    def _validity_period(self):
        self._create_sub_suite("Validity Period")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#validity-period",
        }
        attachments = {
            "Document": self.vc,
            "$.validFrom": self.vc["validFrom"] if "validFrom" in self.vc else None,
            "$.validUntil": self.vc["validUntil"] if "validUntil" in self.vc else None,
        }
        pass

    def _status(self):
        self._create_sub_suite("Status")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#status",
        }
        attachments = {
            "Document": self.vc,
            "$.credentialStatus": self.vc["credentialStatus"]
            if "credentialStatus" in self.vc
            else None,
        }
        pass

    def _data_schemas(self):
        self._create_sub_suite("Data Schemas")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#data-schemas",
        }
        attachments = {
            "Document": self.vc,
            "$.credentialSchema": self.vc["credentialSchema"]
            if "credentialSchema" in self.vc
            else None,
        }
        pass

    def _securing_mechanisms(self):
        self._create_sub_suite("Securing Mechanisms")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _verifiable_presentations(self):
        self._create_sub_suite("Verifiable Presentations")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#verifiable-presentations",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _advanced_concepts(self):
        self._create_suite("Advanced Concepts")
        self._trust_model()
        self._extensibility()
        self._integrity_of_related_ressources()
        self._refreshing()
        self._terms_of_use()
        self._evidence()
        self._zero_knowledge_proofs()
        self._representing_time()
        self._authorization()
        self._reserved_extension_points()
        self._ecosystem_compatibility()
        self._verifiable_credential_graphs()
        self._securing_mechanisms_specifications()

    def _trust_model(self):
        self._create_sub_suite("Trust Model")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#trust-model",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _extensibility(self):
        self._create_sub_suite("Extensibility")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#extensibility",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _integrity_of_related_ressources(self):
        self._create_sub_suite("Integrity of Related Resources")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#integrity-of-related-resources",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _refreshing(self):
        self._create_sub_suite("Refreshing")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#refreshing",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _terms_of_use(self):
        self._create_sub_suite("Terms of Use")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#terms-of-use",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _evidence(self):
        self._create_sub_suite("Evidence")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#evidence",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _zero_knowledge_proofs(self):
        self._create_sub_suite("Zero-Knowledge Proofs")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _representing_time(self):
        self._create_sub_suite("Representing Time")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#representing-time",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _authorization(self):
        self._create_sub_suite("Authorization")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#authorization",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _reserved_extension_points(self):
        self._create_sub_suite("Reserved Extension Points")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#reserved-extension-points",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _ecosystem_compatibility(self):
        self._create_sub_suite("Ecosystem Compatibility")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#ecosystem-compatibility",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _verifiable_credential_graphs(self):
        self._create_sub_suite("Verifiable Credential Graphs")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#verifiable-credential-graphs",
        }
        attachments = {
            "Document": self.vc,
        }
        pass

    def _securing_mechanisms_specifications(self):
        self._create_sub_suite("Securing Mechanism Specifications")
        links = {
            "Specification": "https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanism-specifications",
        }
        attachments = {
            "Document": self.vc,
        }
        pass
