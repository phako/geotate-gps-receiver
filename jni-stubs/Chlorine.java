package com.geotate.locationengine;

public class Chlorine {

    private native int jniStartup(String a, String b, String c, String d);
    private native int jniWaitForNextProgressEvent(int a, int[] b, byte[] c, int[] d);
    private native int jniGetVersionInfo(int[] a);
    private native int jniGetCurrentUTCTimeAndDate(int[] dateTime);
    private native int jniPauseProcessing(int i);
}
