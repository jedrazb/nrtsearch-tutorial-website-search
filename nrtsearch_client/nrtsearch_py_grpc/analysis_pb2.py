# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: yelp/nrtsearch/analysis.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dyelp/nrtsearch/analysis.proto\x12\x0cluceneserver\"\x85\x01\n\rNameAndParams\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\x06params\x18\x02 \x03(\x0b\x32\'.luceneserver.NameAndParams.ParamsEntry\x1a-\n\x0bParamsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"{\n\x16\x43onditionalTokenFilter\x12.\n\tcondition\x18\x01 \x01(\x0b\x32\x1b.luceneserver.NameAndParams\x12\x31\n\x0ctokenFilters\x18\x02 \x03(\x0b\x32\x1b.luceneserver.NameAndParams\"\x18\n\tIntObject\x12\x0b\n\x03int\x18\x01 \x01(\x05\"\xec\x02\n\x0e\x43ustomAnalyzer\x12\x30\n\x0b\x63harFilters\x18\x01 \x03(\x0b\x32\x1b.luceneserver.NameAndParams\x12.\n\ttokenizer\x18\x02 \x01(\x0b\x32\x1b.luceneserver.NameAndParams\x12\x31\n\x0ctokenFilters\x18\x03 \x03(\x0b\x32\x1b.luceneserver.NameAndParams\x12\x45\n\x17\x63onditionalTokenFilters\x18\x04 \x03(\x0b\x32$.luceneserver.ConditionalTokenFilter\x12\x1b\n\x13\x64\x65\x66\x61ultMatchVersion\x18\x05 \x01(\t\x12\x35\n\x14positionIncrementGap\x18\x06 \x01(\x0b\x32\x17.luceneserver.IntObject\x12*\n\toffsetGap\x18\x07 \x01(\x0b\x32\x17.luceneserver.IntObject\"`\n\x08\x41nalyzer\x12\x14\n\npredefined\x18\x01 \x01(\tH\x00\x12.\n\x06\x63ustom\x18\x02 \x01(\x0b\x32\x1c.luceneserver.CustomAnalyzerH\x00\x42\x0e\n\x0c\x41nalyzerTypeBR\n\x1e\x63om.yelp.nrtsearch.server.grpcB\rAnalysisProtoP\x01Z\x19github.com/Yelp/nrtsearch\xa2\x02\x03HLWb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'yelp.nrtsearch.analysis_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.yelp.nrtsearch.server.grpcB\rAnalysisProtoP\001Z\031github.com/Yelp/nrtsearch\242\002\003HLW'
  _NAMEANDPARAMS_PARAMSENTRY._options = None
  _NAMEANDPARAMS_PARAMSENTRY._serialized_options = b'8\001'
  _NAMEANDPARAMS._serialized_start=48
  _NAMEANDPARAMS._serialized_end=181
  _NAMEANDPARAMS_PARAMSENTRY._serialized_start=136
  _NAMEANDPARAMS_PARAMSENTRY._serialized_end=181
  _CONDITIONALTOKENFILTER._serialized_start=183
  _CONDITIONALTOKENFILTER._serialized_end=306
  _INTOBJECT._serialized_start=308
  _INTOBJECT._serialized_end=332
  _CUSTOMANALYZER._serialized_start=335
  _CUSTOMANALYZER._serialized_end=699
  _ANALYZER._serialized_start=701
  _ANALYZER._serialized_end=797
# @@protoc_insertion_point(module_scope)
