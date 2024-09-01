RESULTS = {
    "parentSuites": [
        {
            "uuid": "e7a01ec3-c4b2-4cab-b335-3cb7dda08f99",
            "name": "Surefire suite",
            "start": 1582655012835,
            "stop": 1582655013167,
            "children": ["221fb2e8-7bd0-4ea1-b86c-961be98d9c9f"],
            "suites": [
                {
                    "uuid": "221fb2e8-7bd0-4ea1-b86c-961be98d9c9f",
                    "name": "Surefire test",
                    "start": 1582655012838,
                    "stop": 1582655013159,
                    "children": ["e8fa830a-25a2-462c-b7e8-2a7d732e8695"],
                    "subSuites": [
                        {
                            "uuid": "aeae716a-5677-4d24-a403-c3b12fe7b340",
                            "name": "com.allure.docker.FirstTest",
                            "start": 1582655012844,
                            "stop": 1582655013166,
                            "children": ["e8fa830a-25a2-462c-b7e8-2a7d732e8695"],
                            "steps": [
                                {
                                    "uuid": "e8fa830a-25a2-462c-b7e8-2a7d732e8695",
                                    "historyId": "7b52043cd91c023e7ee912b4d5d3f7e5",
                                    "fullName": "com.allure.docker.FirstTest.test1",
                                    "labels": [
                                        {
                                            "name": "package",
                                            "value": "com.allure.docker.FirstTest",
                                        },
                                        {
                                            "name": "testClass",
                                            "value": "com.allure.docker.FirstTest",
                                        },
                                        {"name": "testMethod", "value": "test1"},
                                        {
                                            "name": "parentSuite",
                                            "value": "Surefire suite",
                                        },
                                        {"name": "suite", "value": "Surefire test"},
                                        {
                                            "name": "subSuite",
                                            "value": "com.allure.docker.FirstTest",
                                        },
                                    ],
                                    "links": [],
                                    "name": "test1",
                                    "status": "passed",
                                    "statusDetails": {
                                        "known": False,
                                        "muted": False,
                                        "flaky": False,
                                    },
                                    "stage": "finished",
                                    "start": 1582655012942,
                                    "stop": 1582655013007,
                                    "attachments": [],
                                    "parameters": [],
                                },
                            ],
                        }
                    ],
                }
            ],
        }
    ]
}
