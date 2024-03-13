package com.geotate.captureunit;

public class CaptureLibrary {
    public native int jniGetDllVersion();
    public native int jniOpenLibrary();
    public native int jniSetEventHandler(boolean b);
    public native boolean jniIsConnected();
}
