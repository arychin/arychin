import time

import jwt
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware

from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES

from projectservice.config import x_user_id
from projectservice.config import settings


tracer = Tracer(
    exporter=AzureExporter(
        connection_string=f'InstrumentationKey={settings.azure_instrument_key}'),
    sampler=ProbabilitySampler(1.0),
)

HTTP_URL = COMMON_ATTRIBUTES['HTTP_URL']
HTTP_HOST = COMMON_ATTRIBUTES['HTTP_HOST']
HTTP_PATH = COMMON_ATTRIBUTES['HTTP_PATH']
HTTP_ROUTE = COMMON_ATTRIBUTES['HTTP_ROUTE']
HTTP_METHOD = COMMON_ATTRIBUTES['HTTP_METHOD']
HTTP_STATUS_CODE = COMMON_ATTRIBUTES['HTTP_STATUS_CODE']


class TimeAndLogItMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        xuid_token = None

        if 'authorization' in request.headers:
            _, auth_token = request.headers['authorization'].split(' ')
            jwt_payload = jwt.decode(auth_token, options={"verify_signature": False})
            xuid_token = x_user_id.set(jwt_payload['uid'])

        with tracer.span("main") as span:
            span.span_kind = SpanKind.SERVER
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_HOST,
                attribute_value=request.url.hostname
                )
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_METHOD,
                attribute_value=request.method
                )
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_URL,
                attribute_value=str(request.url)
                )
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_PATH,
                attribute_value=request.url.path
                )
            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_ROUTE,
                attribute_value=str(request.url.path)
                )

            response = await call_next(request)

            if xuid_token:
                x_user_id.reset(xuid_token)

            tracer.add_attribute_to_current_span(
                attribute_key=HTTP_STATUS_CODE,
                attribute_value=response.status_code
                )

            process_time = time.time() - start_time
            response.headers['X-Process-Time'] = str(process_time)

        return response
