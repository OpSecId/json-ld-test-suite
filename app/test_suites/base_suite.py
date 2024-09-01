from pyld import jsonld
from app.plugins.allure import AllureReporter
from app.test_suites import validations as valid
import time
import json
import uuid
from pprint import pprint


class BaseTestSuite:
    """BaseTestSuite"""

    def __init__(
        self, vc: dict, project: str = "vc-test-suite", timeout: int = 100
    ) -> None:
        """Initialize new BaseTestSuite instance."""
        jsonld.set_document_loader(jsonld.requests_document_loader(timeout=timeout))
        self.vc = vc
        self.reporter = AllureReporter()
        self.project = project
        self.parent_suite = None
        self.suite = None
        self.sub_suite = None
        self.test = None
        self.assertions = None
        self.step = None

    def _timestamp(self):
        return int(time.time_ns() / 1000)

    def _create_parent_suite(self, name):
        self.parent_suite = self.reporter.create_suite(name)
        self.parent_suite["start"] = self._timestamp()

    def _create_suite(self, name):
        self.suite, self.parent_suite = self.reporter.create_suite(
            name, self.parent_suite
        )
        self.suite["start"] = self._timestamp()

    def _create_sub_suite(self, name):
        self.sub_suite, self.suite = self.reporter.create_suite(name, self.suite)
        self.sub_suite["start"] = self._timestamp()

    def _create_test(self, name, assertion):
        self.test, self.sub_suite, self.suite, self.parent_suite = self.reporter.create_test(name, self.sub_suite, self.suite, self.parent_suite)
        self.test["start"] = self._timestamp()
        self.test["status"] = assertion
        self.test["stop"] = self._timestamp()
        self.test["stage"] = "finished"
        self.reporter.tests.append(self.test)

    def _create_step(self, name, assertion):
        self.step, self.sub_suite = self.reporter.create_step(
            name, self.sub_suite, self.sub_suite
        )
        self.step["start"] = self._timestamp()
        self.step["status"] = assertion
        self.step["stop"] = self._timestamp()
        self.step["stage"] = "finished"
        self.reporter.steps.append(self.step)

    def _end_sub_suite(self):
        self.sub_suite["stop"] = self._timestamp()
        self.reporter.tests.append(self.sub_suite)

    def _add_link(self, links):
        self.step["links"].append(
            {"type": "link", "name": link, "url": links[link]} for link in links
        )

    def _add_attachment(self, name, attachment):
        self.step["attachments"].append(
            {"name": name, "source": self.reporter.attachment_source(attachment)}
        )

    def _export_results(self):
        # End test suite
        self.suite["stop"] = self._timestamp()
        self.reporter.suites.append(self.suite)

        # Export results and generate new report
        self.reporter.send_results(self.project)
