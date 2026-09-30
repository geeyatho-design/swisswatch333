plugins { id("com.android.application") }
android {
    namespace = "com.example.raildial"
    compileSdk = 36
    buildToolsVersion = "35.0.0"
    defaultConfig {
        applicationId = "com.example.raildial"
        minSdk = 33
        targetSdk = 35
        versionCode = 4
        versionName = "1.1.0"
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
