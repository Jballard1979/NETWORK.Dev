#--
#-- *************************************************************************************************************:
#-- ********************************************** OPEN TELEMETRY ***********************************************:
#-- *************************************************************************************************************:
#-- Author:  JBALLARD (JEB)                                                                                      :
#-- Date:    2023.3.07                                                                                           :
#-- Script:  SYS-OPEN.TELEMETRY.py                                                                               :
#-- Purpose: A python script that scan a network for retrieves trace & metrics of a network.                     :
#-- Usage:   opentelemetry-instrument --traces_exporter console --metrics_exporter console flask --app server run:
#-- Web:     http://localhost:16686/
#-- Version: 1.0                                                                                                 :
#-- *************************************************************************************************************:
#-- *********************************************** ENV VARIABLES ***********************************************:
#-- *************************************************************************************************************:
#-- TODO: Variable should be set before process starts
#-- export﻿ AUTOWRAPT_BOOTSTRAP=helios 
#-- TODO: Replace value with API token from Helios. 
#-- export HS_TOKEN=<API_TOKEN>
#-- TODO: Replace value with service name.
#-- export HS_SERVICE_NAME=<SERVICE_NAME>
#--﻿TODO: Replace value with service environment.
#-- ﻿export HS_ENVIRONMENT="<ENVIRONMENT_NAME>"
#--
#-- *************************************************:
#-- DEFINE PARAMS, CONFIG PATHS, IMPORT CLASSES      :
#-- *************************************************:
#-- PYTHON -m PIP INSTALL Flask
#-- PYTHON -m PIP INSTALL opentelemetry-api
#-- PYTHON -m PIP INSTALL opentelemetry-sdk
#-- PYTHON -m PIP INSTALL opentelemetry-exporter-jaeger
#-- PYTHON -m PIP INSTALL helios-opentelemetry-sdk
#--
#-- HELIOS:
from helios import initialize 
initialize( 
 api_token=<API_TOKEN>,
 service_name=<SERVICE_NAME>, 
 enabled=True,
 environment=<ENVIRONMENT>,    
 commit_hash=<COMMIT_HASH>,
)
#--
#-- INSTALL JAEGER:
#-- docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14268:14268 -p 14250:14250 -p 9411:9411 jaegertracing/all-in-one:1.23
#--
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
#--
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(
  TracerProvider(
    resource=Resource.create({SERVICE_NAME: "my-python-service"})
  )
)
jaeger_exporter = JaegerExporter(
  agent_host_name="localhost",
  agent_port=6831,
)
trace.get_tracer_provider().add_span_processor(
  BatchSpanProcessor(jaeger_exporter)
)
#--
tracer = trace.get_tracer(name)
app = Flask(name)
#--
@app.route('/')
def index():
  with tracer.start_as_current_span("server_request"):
    return 'START TRACER AS CURRENT SPAN PORT:'
#-- 
app.run(host='10.165.3.18', port=8000)
#--
#-- *************************************************:
#-- END OF SCRIPT                                    :
#-- *************************************************: