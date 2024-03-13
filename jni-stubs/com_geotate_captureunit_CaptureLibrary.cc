#include <com_geotate_captureunit_CaptureLibrary.h>

#include <jni.h>

constexpr unsigned long MINIMUM_LIBRARY_VERSION = 0x26000000;

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureLibrary_jniGetDllVersion(JNIEnv *env,
                                                                                    jobject object)
{
    return MINIMUM_LIBRARY_VERSION;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureLibrary_jniOpenLibrary(JNIEnv *env,
                                                                                  jobject object)
{
    auto clazz = env->GetObjectClass(object);
    auto fid = env->GetFieldID(clazz, "libHandle", "I");
    env->SetIntField(object, fid, 815); // FIXME: Something non-zero for now

    fid = env->GetFieldID(clazz, "eventAppRef", "I");
    env->SetIntField(object, fid, 0);

    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureLibrary_jniSetEventHandler(JNIEnv *env,
                                                                                      jobject object,
                                                                                      jboolean flag)
{
    return 0;
}

JNIEXPORT jboolean JNICALL Java_com_geotate_captureunit_CaptureLibrary_jniIsConnected(JNIEnv *,
                                                                                      jobject)
{
    return JNI_TRUE;
}
