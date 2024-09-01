from typing import Union, List, Dict
from pydantic import BaseModel, Field, BaseConfig


class VcDataModelRequest(BaseModel):
    context: Union[str, Dict[str, str]] = Field(
        example="https://www.w3.org/ns/credentials/v2"
    )

    class Config(BaseConfig):
        extra = "allow"


class VcDataIntegrityRequest(BaseModel):
    context: Union[str, Dict[str, str]] = Field(
        example="https://www.w3.org/ns/credentials/v2"
    )
    proof: Union[dict, List[dict]] = Field(
        example={
            "type": "DataIntegrityProof",
            "cryptosuite": "eddsa-rdfc-2022",
            "verificationMethod": "did:key:z6MkmiYjSToh5NdEf9xNuh5mDGXGYinzcAy1s4feRHtkEQJr#z6MkmiYjSToh5NdEf9xNuh5mDGXGYinzcAy1s4feRHtkEQJr",
            "proofPurpose": "assertionMethod",
            "proofValue": "",
        }
    )

    class Config(BaseConfig):
        extra = "allow"


class VcApiImplementation(BaseModel):
    id: str = Field(example="did:key:z6MkmiYjSToh5NdEf9xNuh5mDGXGYinzcAy1s4feRHtkEQJr")
    name: str = Field(example="Test Suite Agent")
    endpoint: str = Field(example="https://agent.test-suite.site/vc/credentials/issue")
    options: dict = Field(
        example={
            "type": "DataIntegrityProof",
            "cryptosuite": "eddsa-rdfc-2022",
        }
    )


class VcApiRequest(BaseModel):
    issuer: VcApiImplementation = Field(
        example={
            "id": "did:key:z6MkmiYjSToh5NdEf9xNuh5mDGXGYinzcAy1s4feRHtkEQJr",
            "name": "Test Suite Agent",
            "endpoint": "https://agent.test-suite.site/vc/credentials/issue",
            "options": {
                "type": "DataIntegrityProof",
                "cryptosuite": "eddsa-rdfc-2022",
            },
        }
    )
    verifier: VcApiImplementation = Field(
        example={
            "id": "did:key:z6MkmiYjSToh5NdEf9xNuh5mDGXGYinzcAy1s4feRHtkEQJr",
            "name": "Test Suite Agent",
            "endpoint": "https://agent.test-suite.site/vc/credentials/verify",
            "options": {},
        }
    )


class TestSuiteResponse(BaseModel):
    report: str = Field(example="https://reports.test-suite.site")
