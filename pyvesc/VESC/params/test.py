import unittest
from .config_param import Param_UInt8, Param_Int8, Param_UInt16, Param_Int16, Param_UInt32, Param_Int32, Param_Double16, Param_Double32, Param_Double32_Auto

class TestConfigParam(unittest.TestCase):

    def assert_serialization(self, param_class, value, serialized_param, round_result=False):
        # Test serialization
        param = param_class(value=value)
        serialized = param.serialise()
        self.assertEqual(serialized, serialized_param)
        
        # Test deserialization
        param_deserialized = param_class()
        param_deserialized.deserialise(serialized_param)
        if round_result:
            self.assertEqual(param_deserialized.value, round(value))
        else:
            self.assertEqual(param_deserialized.value, value)

    def test_param_uint8(self):
        VALUE = 1
        SERIALIZED = b'\x01'
        self.assert_serialization(Param_UInt8, VALUE, SERIALIZED)

    def test_param_int8(self):
        VALUE = 2
        SERIALIZED = b'\x02'
        self.assert_serialization(Param_Int8, VALUE, SERIALIZED)

    def test_param_uint16(self):
        VALUE = 772
        SERIALIZED = b'\x03\x04'
        self.assert_serialization(Param_UInt16, VALUE, SERIALIZED)

    def test_param_int16(self):
        VALUE = 1286
        SERIALIZED = b'\x05\x06'
        self.assert_serialization(Param_Int16, VALUE, SERIALIZED)

    def test_param_uint32(self):
        VALUE = 117967114
        SERIALIZED = b'\x07\x08\x09\x0A'
        self.assert_serialization(Param_UInt32, VALUE, SERIALIZED)

    def test_param_int32(self):
        VALUE = 201891534
        SERIALIZED = b'\x0C\x08\x9E\xCE'
        self.assert_serialization(Param_Int32, VALUE, SERIALIZED)

    def test_param_double16(self):
        VALUE = 34.2
        SERIALIZED = b'\x00\x22'  # Example value, actual may vary
        self.assert_serialization(Param_Double16, VALUE, SERIALIZED, round_result=True)
        # Additional check for floating-point accuracy if necessary

    def test_param_double32(self):
        VALUE = 10.1
        SERIALIZED = b'\x00\x00\x00\x0A'
        self.assert_serialization(Param_Double32, VALUE, SERIALIZED, round_result=True)

    def test_param_double32_auto(self):
        VALUE = 1.0
        SERIALIZED = b'\x00\x00\x00\x3F'
        self.assert_serialization(Param_Double32_Auto, VALUE, SERIALIZED)

if __name__ == '__main__':
    unittest.main()
