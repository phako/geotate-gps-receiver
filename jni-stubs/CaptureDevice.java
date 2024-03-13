package com.geotate.captureunit;

public class CaptureDevice {
    public native int jniOpenDevice(int i, String s);
    public native int jniGetBatteryStatus(int[] i);
    public native int jniGetDeviceInfo(int[] i, java.lang.String[] s);

    public native int jniGetTrackCount(int[] i);
    public native int jniGetCaptureCount(int i, int[] j);
    public native int jniGetCaptureInfo(int i, int j, int[] k, short[] l);

    public native int jniGetAvailableMemory(int[] i);
    public native int jniGetRTC(short[] s);
    public native int jniSetRTC(short[] s);

    public native int jniGetConfig(int[] i);
    public native int jniSetConfig(int[] i);
}
