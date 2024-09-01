from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.models import web_requests as web
from app.plugins import JsonLdProcessor, DataModelSuite
from app.test_suites.w3c import VcDataModelTestSuite

router = APIRouter()

@router.post("/vc-data-model")
async def w3c_vc_data_model(request_body: web.VcDataModelRequest, project: str = 'vc-data-model'):
    document = request_body.model_dump(by_alias=True)
    vc_data_model_results = VcDataModelTestSuite(vc=document, project=project).run()
    # semantics = {
    #     "undefined_types": JsonLdProcessor(document).find_undefined_types(),
    #     "undefined_properties": JsonLdProcessor(document).find_undefined_properties(),
    # }
    return JSONResponse(
        status_code=200,
        content={
            "vc_data_model": vc_data_model_results
            # "semantics": semantics
        },
    )