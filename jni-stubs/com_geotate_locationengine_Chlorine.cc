#include <com_geotate_locationengine_Chlorine.h>

#include <jni.h>

#include <iostream>
#include <chrono>

JNIEXPORT jint JNICALL Java_com_geotate_locationengine_Chlorine_jniStartup(
    JNIEnv *env, jobject obj, jstring a, jstring b, jstring c, jstring d)
{
    if (a != nullptr) {
        std::cerr << __PRETTY_FUNCTION__ << "a: ";
        const char *cstr = env->GetStringUTFChars(a, nullptr);
        std::cerr << cstr;
        env->ReleaseStringUTFChars(a, cstr);
    }

    if (b != nullptr) {
        std::cerr << __PRETTY_FUNCTION__ << "b: ";
        const char *cstr = env->GetStringUTFChars(b, nullptr);
        std::cerr << cstr;
        env->ReleaseStringUTFChars(a, cstr);
    }

    if (c != nullptr) {
        std::cerr << __PRETTY_FUNCTION__ << "c: ";
        const char *cstr = env->GetStringUTFChars(c, nullptr);
        std::cerr << cstr;
        env->ReleaseStringUTFChars(a, cstr);
    }

    if (d != nullptr) {
        std::cerr << __PRETTY_FUNCTION__ << "d: ";
        const char *cstr = env->GetStringUTFChars(d, nullptr);
        std::cerr << cstr;
        env->ReleaseStringUTFChars(a, cstr);
    }

    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_locationengine_Chlorine_jniWaitForNextProgressEvent(
    JNIEnv *, jobject, jint, jintArray, jbyteArray, jintArray)
{
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_locationengine_Chlorine_jniGetVersionInfo(JNIEnv *,
                                                                                  jobject,
                                                                                  jintArray)
{
    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_locationengine_Chlorine_jniGetCurrentUTCTimeAndDate(
    JNIEnv *env, jobject, jintArray dateTime)
{
    std::cerr << __PRETTY_FUNCTION__ << std::endl;

    jint dateData[] = {2022, 11, 00, 15, 9, 07, 00, 00, 00};

    env->SetIntArrayRegion(dateTime, 0, 8, dateData);

    return 0;
}

JNIEXPORT jint JNICALL Java_com_geotate_locationengine_Chlorine_jniPauseProcessing(JNIEnv *,
                                                                                   jobject,
                                                                                   jint)
{
    return 0;
}
