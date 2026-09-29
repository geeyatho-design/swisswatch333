plugins { id("com.android.application") }
android {
    namespace = "com.example.raildial"
    compileSdk = 36
    buildToolsVersion = "35.0.0"
    defaultConfig {
        applicationId = "com.example.raildial"
        minSdk = 33
        targetSdk = 35
        versionCode = 3
        versionName = "1.0.2"
    }
    buildTypes {
        debug {
            isMinifyEnabled = true
            isShrinkResources = false
        }
        release {
            isMinifyEnabled = true
            isShrinkResources = false
        }
    }
}
