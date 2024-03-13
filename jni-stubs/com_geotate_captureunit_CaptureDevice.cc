#include <com_geotate_captureunit_CaptureDevice.h>

#include <jni.h>

#include <iostream>

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniOpenDevice(JNIEnv *env,
                                                                                jobject object,
                                                                                jint a,
                                                                                jstring b)
{
    auto *clazz = env->GetObjectClass(object);
    auto *fid = env->GetFieldID(clazz, "devHandle", "I");
    env->SetIntField(object, fid, 915); // FIXME: Something non-zero for now

    if (b != nullptr) {
        std::cerr << "jniOpenDevice parameter b: ";
        const char *cstr = env->GetStringUTFChars(b, nullptr);
        std::cerr << cstr;
        env->ReleaseStringUTFChars(b, cstr);
    }

    return 0;
}

// Return the battery charge in %
JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetBatteryStatus(
    JNIEnv *env, [[maybe_unused]] jobject obj, jintArray array)
{
    constexpr jint BATTERY_FULL = 100;

    env->SetIntArrayRegion(array, 0, 1, &BATTERY_FULL);
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetDeviceInfo(JNIEnv *,
                                                                                   jobject,
                                                                                   jintArray,
                                                                                   jobjectArray)
{
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetTrackCount(JNIEnv *env,
                                                                                   jobject,
                                                                                   jintArray arr)
{
    jint value = 1;
    env->SetIntArrayRegion(arr, 0, 1, &value);

    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetCaptureCount(
    JNIEnv *env, jobject, jint track, jintArray outCount)
{
    jint value = 1;
    env->SetIntArrayRegion(outCount, 0, 1, &value);

    return 0;
}


// captureDefinition: array of two, first id, second size
// date: 8 shorts
JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetCaptureInfo(
    JNIEnv *env, jobject, jint track, jint position, jintArray captureDefinition, jshortArray date)
{
    jshort dateData[] = {2009, 0, 1, 10, 11, 12, 13, 14};
    jint info[] = {0, 5};

    env->SetIntArrayRegion(captureDefinition, 0, 2, info);
    env->SetShortArrayRegion(date, 0, 8, dateData);

    return 0;
}
JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetAvailableMemory(JNIEnv *,
                                                                                        jobject,
                                                                                        jintArray)
{
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetRTC(JNIEnv *env,
                                                                            jobject,
                                                                            jshortArray date)
{
    // YYYY, M, DOW, D, H, M, S?, MS?
    jshort dateData[] = {2009, 1, 10, 19, 12, 13, 14, 15};

    env->SetShortArrayRegion(date, 0, 8, dateData);
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniSetRTC(JNIEnv *env,
                                                                            jobject,
                                                                            jshortArray date)
{
    jsize len = env->GetArrayLength(date);
    auto *params = env->GetShortArrayElements(date, nullptr);
    std::cerr << __PRETTY_FUNCTION__ << "Parameters passed:" << std::endl;
    for (int i = 0; i < len; i++) {
        std::cerr << " i: " << i << ", param: " << params[i] << std::endl;
    }

    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniGetConfig(JNIEnv *,
                                                                               jobject,
                                                                               jintArray)
{
    // Index 5 of array is the capture delay in milliseconds
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_captureunit_CaptureDevice_jniSetConfig(JNIEnv *env,
                                                                               jobject,
                                                                               jintArray arr)
{
    // Index 5 of array is the capture delay in milliseconds
    jsize len = env->GetArrayLength(arr);
    jint *params = env->GetIntArrayElements(arr, nullptr);
    std::cerr << __PRETTY_FUNCTION__ << "Parameters passed:" << std::endl;
    for (int i = 0; i < len; i++) {
        std::cerr << " i: " << i << ", param: " << params[i] << std::endl;
    }
    return 0;
}
