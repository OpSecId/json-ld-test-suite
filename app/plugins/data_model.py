from pyld import jsonld
from app.plugins.allure import AllureReporter
from app.test_suites import validations as valid
import time
import json
from pprint import pprint


class DataModelSuite:
    """VC Data Model validation."""

    def __init__(
        self, vc: dict, project: str = "vc-test-suite", timeout: int = 100
    ) -> None:
        """Initialize new JsonLdProcessor instance."""
        jsonld.set_document_loader(jsonld.requests_document_loader(timeout=timeout))
        self.vc = vc
        self.reporter = AllureReporter()
        self.project = project
        self.suite = None
        self.test = None
        self.step = None

    def _timestamp(self):
        return int(time.time_ns() / 1000)

    def _create_suite(self, name):
        self.suite = self.reporter.create_suite(name)
        self.suite["start"] = self._timestamp()

    def _create_test(self, name):
        self.test, self.suite = self.reporter.create_test(name, self.suite)
        self.test["start"] = self._timestamp()

    def _end_test(self):
        self.test["stop"] = self._timestamp()
        self.reporter.tests.append(self.test)

    def _create_step(self, name, link=None):
        self.step, self.test = self.reporter.create_step(name, self.test, self.suite)
        self.step["links"].append(
            {
                "type": "link",
                "name": "Specification",
                "url": "https://www.w3.org/TR/vc-data-model-2.0",
            }
        )
        if link:
            self.step["links"].append({"type": "link", "name": "Section", "url": link})
        self.step["start"] = self._timestamp()

    def _assert_step(self, assertion, attachment=None):
        self.step["status"] = assertion
        self.step["stop"] = self._timestamp()
        self.step["stage"] = "finished"
        self.step = self.reporter.add_attachment("Credential", self.vc, self.step)
        if attachment:
            self.step = self.reporter.add_attachment(
                "Test Input", {"value": attachment}, self.step
            )
        self.reporter.steps.append(self.step)

    def _export_results(self):
        # End test suite
        self.suite["stop"] = self._timestamp()
        self.reporter.suites.append(self.suite)

        # Export results and generate new report
        self.reporter.send_results(self.project)

    def run(self):
        # Store a copy of the VC
        self.reporter.attachments.append(self.vc.copy())

        # Create a new test suite
        self._create_suite("VC Test Suite")

        # Test features
        self._test_contexts()
        self._test_identifiers()
        self._test_types()
        self._test_names_and_descriptions()
        self._test_issuer()
        self._test_credential_subject()
        self._test_validity_period()
        self._test_status()
        self._test_data_schemas()
        self._test_securing_mechanisms()
        self._test_verifiable_presentations()

        # End test suite, export results and generate new report
        self._export_results()
        results = {}
        for test in self.reporter.tests:
            results[test["name"]] = [
                {"statement": step["name"], "check": step["status"]}
                for step in self.reporter.steps
                if step["uuid"] in test["children"]
            ]
        return results

    # Contexts
    def _test_contexts(self):
        spec_link = "https://www.w3.org/TR/vc-data-model-2.0/#contexts"
        context = self.vc["@context"] if "@context" in self.vc else None
        self.reporter.attachments.append(context)
        self._create_test("Contexts")

        for test in [
            {
                "statement": "Verifiable credentials and verifiable presentations MUST include a @context property.",
                "assertion": "passed" if "@context" in self.vc else "failed",
            },
            {
                "statement": "Application developers MUST understand every JSON-LD context used by their application, at least to the extent that it affects the meaning of the terms used by their application.",
                "assertion": "skipped",
            },
            {
                "statement": "The value of the @context property MUST be an ordered set where the first item is a URL with the value https://www.w3.org/ns/credentials/v2.",
                "assertion": "passed"
                if (
                    "@context" in self.vc
                    and (
                        isinstance(self.vc["@context"], list)
                        and self.vc["@context"][0]
                        == "https://www.w3.org/ns/credentials/v2"
                    )
                )
                else "failed",
            },
            {
                "statement": "Subsequent items in the ordered set MUST be composed of any combination of URLs and objects, where each is processable as a JSON-LD Context.",
                "assertion": "passed"
                if (valid.context_item(item) for item in self.vc["@context"][1:])
                else "failed",
            },
        ]:
            self._create_step(name=test["statement"], link=spec_link)
            self._assert_step(assertion=test["assertion"], attachment=context)

        self._end_test()

    # Types
    def _test_types(self):
        spec_link = "https://www.w3.org/TR/vc-data-model-2.0/#types"
        types = self.vc["types"] if "types" in self.vc else None
        self.reporter.attachments.append(types)
        self._create_test("Types")

        for test in [
            {
                "statement": "Verifiable credentials and verifiable presentations MUST contain a type property with an associated value.",
                "assertion": "passed"
                if ("type" in self.vc and self.vc["type"])
                else "failed",
            },
            {
                "statement": "The value of the type property MUST be one or more terms and absolute URL strings.",
                "assertion": "passed"
                if (
                    "type" in self.vc
                    and (
                        "type" in valid.type_item(item)
                        for item in (
                            [self.vc["type"]]
                            if isinstance(self.vc["type"], str)
                            else self.vc["type"]
                        )
                    )
                )
                else "failed",
            },
            {
                "statement": "Verifiable credential object MUST have a type VerifiableCredential and, optionally, a more specific verifiable credential type.",
                "assertion": "passed"
                if (
                    "type" in self.vc
                    and (
                        "VerifiableCredential" in self.vc["type"]
                        if isinstance(self.vc["type"], list)
                        else self.vc["type"] == "VerifiableCredential"
                    )
                )
                else "failed",
            },
        ]:
            self._create_step(name=test["statement"], link=spec_link)
            self._assert_step(assertion=test["assertion"], attachment=types)

        self._end_test()

    def _test_identifiers(self):
        self._create_test("Identifiers")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self._end_test()

    def _test_names_and_descriptions(self):
        self._create_test("Names and Descriptions")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self._end_test()

    def _test_issuer(self):
        issuer = self.vc["issuer"] if "issuer" in self.vc else None
        self.reporter.attachments.append(issuer)
        self._create_test("Issuer")
        for test in [
            {
                "statement": "A verifiable credential MUST have an issuer property.",
                "assertion": "passed"
                if ("issuer" in self.vc and self.vc["issuer"])
                else "failed",
            }
        ]:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"], attachment=issuer)
        self._end_test()

    def _test_credential_subject(self):
        credential_subject = (
            self.vc["credentialSubject"] if "credentialSubject" in self.vc else None
        )
        self.reporter.attachments.append(credential_subject)
        self._create_test("Credential Subject")
        for test in [
            {
                "statement": "A verifiable credential MUST contain a credentialSubject property.",
                "assertion": "passed"
                if ("credentialSubject" in self.vc and self.vc["credentialSubject"])
                else "failed",
            }
        ]:
            self._create_step(name=test["statement"])
            self._assert_step(
                assertion=test["assertion"], attachment=credential_subject
            )
        self._end_test()

    def _test_validity_period(self):
        valid_from = self.vc["validFrom"] if "validFrom" in self.vc else None
        self.reporter.attachments.append(valid_from)
        valid_until = self.vc["validUntil"] if "validUntil" in self.vc else None
        self.reporter.attachments.append(valid_until)
        self._create_test("Validity Period")
        if "validFrom" in self.vc:
            self._create_step(
                name="If present, the value of the validFrom property MUST be a [XMLSCHEMA11-2] dateTimeStamp string value"
            )
            self._assert_step(
                assertion="passed"
                if isinstance(self.vc["validFrom"], str)
                and valid.xml_datetimestamp_value(self.vc["validFrom"])
                else "failed",
                attachment=valid_from,
            )
        if "validFrom" in self.vc and "validUntil" in self.vc:
            self._create_step(
                name="If a validUntil value also exists, the validFrom value MUST express a point in time that is temporally the same or earlier than the point in time expressed by the validUntil value."
            )
            self._assert_step(
                assertion="passed"
                if valid.is_before(self.vc["validFrom"], self.vc["validUntil"])
                else "failed"
            )
        if "validUntil" in self.vc:
            self._create_step(
                name="If present, the value of the validUntil property MUST be a [XMLSCHEMA11-2] dateTimeStamp string value"
            )
            self._assert_step(
                assertion="passed"
                if isinstance(self.vc["validUntil"], str)
                and valid.xml_datetimestamp_value(self.vc["validUntil"])
                else "failed",
                attachment=valid_until,
            )
        if "validFrom" in self.vc and "validUntil" in self.vc:
            self._create_step(
                name="If a validFrom value also exists, the validUntil value MUST express a point in time that is temporally the same or later than the point in time expressed by the validFrom value."
            )
            self._assert_step(
                assertion="passed"
                if valid.is_before(self.vc["validFrom"], self.vc["validUntil"])
                else "failed"
            )

        self._end_test()

    def _test_status(self):
        self._create_test("Status")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self.test["start"] = self._timestamp()
        self._end_test()

    def _test_data_schemas(self):
        self._create_test("Data Schemas")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self.test["start"] = self._timestamp()
        self._end_test()

    def _test_securing_mechanisms(self):
        self._create_test("Securing Mechanisms")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self.test["start"] = self._timestamp()
        self._end_test()

    def _test_verifiable_presentations(self):
        self._create_test("Verifiable Presentations")
        for test in []:
            self._create_step(name=test["statement"])
            self._assert_step(assertion=test["assertion"])
        self.test["start"] = self._timestamp()
        self._end_test()
