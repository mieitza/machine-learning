#!/usr/bin/python

## @session_data_new.py
#  This file receives data (i.e. settings), including one or more dataset(s)
#      provided during the current session, and stores them into corresponding
#      database tables. The stored dataset(s) can later be retrieved from
#      'session_data_append.py', or 'session_generate_model.py'.
#
#  Note: this script is executed from 'load_logic.php', using the 'exec( ... )'
#        equivalent method when implemented via the web-interface. Since the
#        web-interface is an AJAX process, the shelled into python script requires
#        print statements, when data is needed to be returned to the client-end.
#
#  Note: the term 'dataset' used throughout various comments in this file,
#        synonymously implies the user supplied 'file upload(s)', and XML url
#        references.
import sys, json
from data_saver import Training
from data_validator import Validator
from converter_json import JSON

## Class: Data_New
class Data_New:

  ## constructor:
  def __init__(self, svm_data=None):
    self.svm_data       = svm_data
    self.flag_quit      = True
    self.response_validation = []

  ## validate_arg_none: check if class variable 'svm_data' is defined, and
  #                     define 'self.flag_quit', respectively.
  def validate_arg_none(self):
    if self.svm_data != None: self.flag_quit = False
    else: self.flag_quit = True
    return self.flag_quit

  ## validate_svm_settings: validate svm session settings (not dataset).
  def validate_svm_settings(self):
    validator = Validator( self.svm_data, 'training' )
    if validator.data_validation()['error'] != None:
      self.response_validation.append( validator.data_validation()['error'] )

  ## validate_mime_type: validate mime type for each dataset.
  def validate_mime_type(self):
    validator = Validator( self.svm_data, 'training' )
    self.response_mime_validation = validator.file_upload_validation( self.svm_data )
    if self.response_mime_validation['error']:
      self.response_validation.append( self.response_mime_validation['error'] )

  ## save_svm_entity: save entity information pertaining to new session.
  def save_svm_entity(self):
    svm_entity = {'title': json.loads( self.svm_data )['data']['settings'].get('svm_title', None), 'uid': 1}
    db_save    = Training( svm_entity, 'save_entity' )
    self.id_entity  = db_save.db_save_training()

  ## dataset_to_json: convert either csv, or xml dataset(s) to a uniform
  #                   json object.
  def dataset_to_json(self):
    flag_convert = False

    try:
      self.response_mime_validation['json_data']['file_upload']
      flag_convert = True
    except Exception as e:
      print e
      sys.exit()

    if ( flag_convert ):
      self.json_dataset = []
      svm_property      = self.svm_data

      for val in self.response_mime_validation['json_data']['file_upload']:
        # csv to json
        if val['type'] in ('text/plain', 'text/csv'):
          try:
            for dataset in val['filedata']['file_temp']:
              self.json_dataset.append({'id_entity': self.id_entity, 'svm_dataset': json.loads(JSON(dataset).csv_to_json())})
          except Exception as e:
            print e
            sys.exit()

        # xml to json
        elif val['type'] in ('application/xml', 'text/xml' ):
          try:
            self.json_dataset.append({'id_entity': self.id_entity, 'svm_dataset': json.loads(JSON(dataset).xml_to_json())})
          except Exception as e:
            print e
            sys.exit()

  ## validate_dataset_json: validate each dataset element.
  def validate_dataset_json(self):
    for val in self.json_dataset:
      json_validated = Validator( val )

      if json_validated.dataset_validation()['error'] != None:
        self.response_validation.append( json_validated.dataset_validation()['error'] )

  ## save_svm_dataset: save each dataset element into a database table.
  def save_svm_dataset(self):
    for val in self.json_dataset:
      db_save = Training( val, 'save_value' )
      db_save.db_save_training()

  ## validation_check_return: check if any validation failed.
  def validation_check_return(self):
    flag_quit = False

    if (self.response_mime_validation['status'] == False):
      flag_quit = True

    for value in self.response_validation:
      if value['status'] == False:
        print value['error']
        flag_quit = True

    if flag_quit == True:
      sys.exit()
