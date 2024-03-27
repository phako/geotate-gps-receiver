project('taggr-native-stubs', ['java', 'cpp'], version: '0.1')
java = import('java')

jni_dep = dependency('jni', version : '>=1.8', modules: ['jvm', 'awt'])

chlorine_native_headers = java.generate_native_headers(
  'Chlorine.java',
  package: 'com.geotate.locationengine',
  classes: ['Chlorine']
)

chlorine_native_headers_include = include_directories('.')

chlorine = shared_module(
  'Chlorine',
  [chlorine_native_headers, 'com_geotate_locationengine_Chlorine.cc'],
  dependencies : [jni_dep],
  include_directories: chlorine_native_headers_include
)


capture_native_headers = java.generate_native_headers(
  ['CaptureLibrary.java', 'CaptureDevice.java'],
  package: 'com.geotate.captureunit',
  classes: ['CaptureLibrary', 'CaptureDevice']
)
capture_native_headers_include = include_directories('.')

capture_device = shared_module(
  'CaptureUnit',
  [
    capture_native_headers,
    'com_geotate_captureunit_CaptureLibrary.cc',
    'com_geotate_captureunit_CaptureDevice.cc'
  ],
  dependencies : [jni_dep],
  include_directories: capture_native_headers_include
)
