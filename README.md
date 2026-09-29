# Rail Dial 1.0.2

**AOD 디자인을 항상 표시하는 별도 버전:** [Rail Dial AOD 1.0.0](aod/README.md). 기존 워치페이스와 함께 설치할 수 있습니다.

Wear OS 4 이상용 개인 워치페이스입니다. 흰 바탕, 검은 시침·분침, 붉은 원판 초침을 사용합니다.

- 절전 화면(AOD)은 검은 바탕과 얇은 회색 시침·분침만 표시합니다.
- 시각은 워치 시스템 시간을 사용합니다. 네트워크·위치·개인정보 권한은 요청하지 않습니다.
- 공식 Mondaine/SBB 제품이 아닙니다. 철도 시계의 2초 정지 동작은 구현하지 않았습니다.

## APK 빌드
이 파일과 `app/`, `.github/`, Gradle 설정을 저장소 최상단에 둡니다. 기본 브랜치 `main`에 반영하면 Actions의 **Build Wear OS APK**가 실행됩니다. 수동 실행도 가능합니다.
성공한 실행 화면 하단의 **rail-dial-1.0.2-apk**를 내려받으면 APK, 서명 검사 결과, 패키지 정보, SHA-256 해시가 들어 있습니다.
현재 빌드는 Android 개발용 키로 서명합니다. 실행 환경이 달라지면 키가 바뀔 수 있습니다. 향후 업데이트를 계속 배포하려면 별도 보관한 서명키를 사용해야 합니다.

## 설치 대상
이 APK는 갤럭시 워치4 이후 중 Wear OS 4 이상인 **워치에 직접 설치**합니다. 휴대전화에서 APK를 누르는 것으로 워치에 설치되지 않습니다. 워치 무선 디버깅에 연결해 `adb install -r rail-dial-1.0.2.apk`를 실행한 뒤, 워치의 시계 화면 선택 목록에서 **Rail Dial**을 선택합니다.

## 로컬 빌드
JDK 17, Gradle 8.11.1, Android SDK 플랫폼 36 및 빌드 도구 35.0.0이 필요합니다.
`gradle :app:assembleDebug`

## 확인 상태
GitHub Actions에서 2026-09-29에 최종 APK 빌드 및 APK Signature Scheme v2 서명 검사에 성공했습니다. 다운로드 후 SHA-256, ZIP 무결성, 실행 코드(DEX) 없음, XML·이미지 리소스 포함 여부를 확인했습니다. Google 공식 WFF v1 XSD를 XSD 1.1 검증기로 검사했고 통과했습니다. 미리보기는 직접 확인했습니다. 실제 갤럭시 워치 설치·실행은 아직 확인하지 못했습니다.

[검증된 1.0.2 빌드 기록](https://github.com/geeyatho-design/swisswatch333/actions/runs/36571149653)

## Windows에서 직접 설치
1. Google의 [SDK Platform-Tools](https://developer.android.com/tools/releases/platform-tools)에서 Windows용 도구를 내려받아 압축을 풉니다. 그 폴더에 `rail-dial-1.0.2.apk`도 둡니다.
2. 워치와 PC를 같은 Wi-Fi에 연결합니다. 워치 **설정 → 워치 정보 → 소프트웨어 정보 → 소프트웨어 버전**을 5회 눌러 개발자 옵션을 켭니다.
3. **개발자 옵션 → ADB 디버깅 / 무선 디버깅**을 켜고 **새 기기 페어링**에 표시되는 주소·포트·코드를 확인합니다.
4. 도구 폴더에서 터미널을 열고 아래 명령을 순서대로 실행합니다. `<...>`는 워치 화면의 실제 숫자로 바꿉니다. 페어링 포트와 연결 포트는 다릅니다.

```powershell
.\adb.exe pair <워치IP>:<페어링포트>
.\adb.exe connect <워치IP>:<연결포트>
.\adb.exe -s <워치IP>:<연결포트> install -r .\rail-dial-1.0.2.apk
```

첫 명령에서 코드를 물으면 워치의 페어링 코드를 입력합니다. `Success`가 나오면 워치의 시계 화면을 길게 눌러 **시계 화면 추가 → Rail Dial**을 선택합니다. 끝나면 워치의 ADB·무선 디버깅을 끕니다.

[삼성 공식 무선 연결 설명](https://developer.samsung.com/sdp/blog/en/2024/04/30/connect-galaxy-watch-to-android-studio-over-wi-fi)
