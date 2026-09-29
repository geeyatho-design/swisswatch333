# Rail Dial 1.0.1

갤럭시 워치4 이후 Wear OS 워치용 개인 시안입니다. 흰 다이얼, 굵은 검은 시침·분침, 붉은 원판 초침을 사용합니다. 공식 MONDAINE/SBB 제품이나 라이선스 제품이 아닙니다.

## 빌드 및 설치
1. Android Studio에서 이 폴더를 엽니다. Android SDK 36과 Gradle 동기화를 마칩니다.
2. 워치의 개발자 옵션에서 무선 디버깅을 켜고 Android Studio의 Wear OS 기기로 연결합니다.
3. `app` 모듈을 빌드해 APK를 설치하거나 Android Studio의 Run으로 실행합니다.
4. 워치의 시계 화면 선택 화면에서 **Rail Dial**을 선택합니다.

`app/src/main/res/raw/watchface.xml`은 Watch Face Format 1 형식입니다. 초침은 운영체제 시각에 따라 움직입니다. 철도역 시계의 2초 정지 동작은 구현하지 않았습니다. 화면 항상 켜기 여부와 절전 화면 밝기는 워치 설정 및 Wear OS가 제어합니다.

이 실행 환경에는 Android SDK가 없어 APK 빌드·실기기 검증은 수행하지 못했습니다. XML 파싱과 이미지 크기 검사는 수행했습니다.

## 휴대폰만으로 APK 빌드하기
GitHub 모바일 웹에서 새 저장소를 만들고 이 압축파일의 **내용물**을 저장소 최상단에 올립니다. Actions 탭에서 **Build Wear OS APK → Run workflow**를 누릅니다. 완료되면 실행 기록 아래 **rail-dial-debug-apk** 아티팩트를 내려받아 압축을 풀면 `app-debug.apk`가 있습니다. APK는 휴대전화용 앱이 아니라 **워치에 설치**하는 앱입니다. 워치에 설치할 때는 무선 디버깅으로 연결하거나 워치 앱 설치 도구를 사용해야 합니다. 이 경로는 아직 실제 실행으로 검증하지 못했습니다.
