# Copyright 2014 Rackspace
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#

import jsonschema
from testtools import TestCase
from trove.configuration.service import ConfigurationsController


class TestConfigurationController(TestCase):
    def setUp(self):
        super(TestConfigurationController, self).setUp()
        self.controller = ConfigurationsController()

    def test_validate_create_configuration(self):
        body = {
            "configuration": {
                "values": {},
                "name": "test",
                "datastore": {
                    "type": "test_type",
                    "version": "test_version"
                }
            }
        }
        schema = self.controller.get_schema('create', body)
        self.assertIsNotNone(schema)
        validator = jsonschema.Draft4Validator(schema)
        self.assertTrue(validator.is_valid(body))

    def test_validate_create_configuration_no_datastore(self):
        body = {
            "configuration": {
                "values": {},
                "name": "test"
            }
        }
        schema = self.controller.get_schema('create', body)
        self.assertIsNotNone(schema)
        validator = jsonschema.Draft4Validator(schema)
        self.assertTrue(validator.is_valid(body))

    def test_validate_create_invalid_values_param(self):
        body = {
            "configuration": {
                "values": '',
                "name": "test",
                "datastore": {
                    "type": "test_type",
                    "version": "test_version"
                }
            }
        }
        schema = self.controller.get_schema('create', body)
        self.assertIsNotNone(schema)
        validator = jsonschema.Draft4Validator(schema)
        self.assertFalse(validator.is_valid(body))
        errors = sorted(validator.iter_errors(body), key=lambda e: e.path)
        self.assertEqual(errors[0].message,
                         "'' is not of type 'object'")

    def test_validate_create_invalid_name_param(self):
        body = {
            "configuration": {
                "values": {},
                "name": "",
                "datastore": {
                    "type": "test_type",
                    "version": "test_version"
                }
            }
        }
        schema = self.controller.get_schema('create', body)
        self.assertIsNotNone(schema)
        validator = jsonschema.Draft4Validator(schema)
        self.assertFalse(validator.is_valid(body))
        errors = sorted(validator.iter_errors(body), key=lambda e: e.path)
        self.assertEqual(errors[0].message,
                         "'' is too short")

    def test_validate_edit_configuration(self):
        body = {
            "configuration": {
                "values": {}
            }
        }
        schema = self.controller.get_schema('edit', body)
        self.assertIsNotNone(schema)
        validator = jsonschema.Draft4Validator(schema)
        self.assertTrue(validator.is_valid(body))
