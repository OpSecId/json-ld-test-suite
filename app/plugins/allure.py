import uuid
import requests
from config import settings
import time
import base64
import json
from pprint import pprint


class AllureReporter:
    def __init__(self):
        self.endpoint = f"{settings.ALLURE_API}/allure-docker-service"
        self.headers = {"Content-Type": "application/json"}
        self.parent_suites = []
        self.suites = []
        self.sub_suites = []
        self.tests = []
        self.steps = []
        self.attachments = []

    def create_project(self, project_id):
        requests.post(
            f"{self.endpoint}/projects", headers=self.headers, json={"id": project_id}
        )

    def create_suite(self, name, parent=None):
        suite = {
            "uuid": str(uuid.uuid4()),
            "name": name,
            "children": [],
        }
        if parent:
            parent["children"].append(suite["uuid"])
            return suite, parent
        return suite

    def create_test(self, name, sub_suite, suite, parent_suite):
        test = {
            "uuid": str(uuid.uuid4()),
            "historyId": str(uuid.uuid5(uuid.NAMESPACE_DNS, name + "history")),
            "testCaseId": str(uuid.uuid5(uuid.NAMESPACE_DNS, name + "case")),
            "name": name,
            "fullName": name,
            "description": "",
            "descriptionHtml": "",
            "links": [],
            "labels": [
                {"name": "tag", "value": None},
                {
                    "name": "severity",
                    "value": None,
                },  # trivial, minor, normal, critical, blocker
                {"name": "owner", "value": None},  # Author
                {"name": "package", "value": name},
                {"name": "testClass", "value": name},
                {"name": "testMethod", "value": name},
                {"name": "parentSuite", "value": parent_suite},
                {"name": "suite", "value": suite},
                {"name": "subSuite", "value": sub_suite},
                {"name": "language", "value": "Python"},
                {"name": "framework", "value": "Custom"},
            ],
            "parameters": [
                {
                    "name": None,
                    "value": None,
                    "excluded": False,
                    "mode": "default",  # default, masked, hidden
                }
            ],
            "attachments": [
                {
                    "name": "",
                    "source": "",
                    "type": "application/json",
                }
            ],
            "status": "unknown",  # failed, passed, broken, skipped, unknown
            "statusDetails": {
                "known": False,
                "muted": False,
                "message": False,
                "trace": False,
                "flaky": False,
            },
            "stage": "pending",  # "scheduled", "running", "finished", "pending", "interrupted"
            "start": None,
            "stop": None,
            "steps": [],
            "parameters": [],
        }
        sub_suite['children'].append(test['uuid'])
        suite['children'].append(test['uuid'])
        parent_suite['children'].append(test['uuid'])
        return test, sub_suite, suite, parent_suite

    def create_step(self, name):
        step = {
            "name": name,
            "parameters": [],
            "attachments": [],
            "status": "unknown",  # failed, passed, broken, skipped, unknown
            "statusDetails": {
                "known": False,
                "muted": False,
                "message": False,
                "trace": False,
                "flaky": False,
            },
            "stage": "pending",  # "scheduled", "running", "finished", "pending", "interrupted"
            "start": None,
            "stop": None,
            "steps": [],
        }

    def _attachment_source(self, attachment):
        return f"{str(uuid.uuid5(uuid.NAMESPACE_DNS, json.dumps(attachment)))}-attachment.json"

    def _format_entry(self, entry, file_name):
        output = {
            "file_name": file_name,
            "content_base64": base64.b64encode(
                json.dumps(entry, indent=2).encode()
            ).decode("UTF-8"),
        }
        return output

    def send_results(self, project):
        results = []
        for step in self.steps:
            results.append(self._format_entry(step, step["uuid"] + "-result.json"))
        for test in self.tests:
            results.append(self._format_entry(test, test["uuid"] + "-container.json"))
        for suite in self.suites:
            results.append(self._format_entry(suite, suite["uuid"] + "-container.json"))
        for attachment in self.attachments:
            results.append(
                self._format_entry(attachment, self.attachment_source(attachment))
            )
        requests.post(
            f"{self.endpoint}/send-results?project_id={project}&force_project_creation=true",
            headers=self.headers,
            json={"results": results},
        )
        requests.get(
            f"{self.endpoint}/generate-report?project_id={project}",
            headers=self.headers,
        )
        # requests.get(f'{self.endpoint}/clean-results?project_id={project}', headers=self.headers)
