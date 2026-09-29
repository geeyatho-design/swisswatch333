# Rail Dial AOD 1.0.0

Rail Dial 1.0.2의 AOD 디자인을 일반 화면으로 사용하는 별도 워치페이스입니다.

- 검은 배경, 12개 회색 눈금, 얇은 회색 시침·분침을 그대로 사용합니다.
- 초침은 없으며, 일반 화면과 절전 화면(AOD)에 같은 디자인이 표시됩니다. 화면 밝기와 AOD 켜기 여부는 워치 설정을 따릅니다.
- 표시 이름: **Rail Dial AOD**
- 별도 앱 ID: `com.example.raildial.aod` — 기존 `com.example.raildial`과 함께 설치할 수 있습니다.
- Wear OS 4 이상. 갤럭시 워치에 직접 설치합니다.

## 빌드
저장소 Actions에서 **Build Rail Dial AOD APK**를 실행합니다. 완료 후 **rail-dial-aod-1.0.0-apk**를 내려받으면 APK와 서명·패키지 검사 결과가 들어 있습니다.

로컬 빌드: `gradle :aod:assembleDebug`

## 설치
워치에 이미 무선 연결된 PC라면, `adb.exe`와 APK가 있는 폴더에서 다음을 실행합니다.

```bat
adb install -r rail-dial-aod-1.0.0.apk
```

연결된 기기가 여러 대이면 `adb -s 워치IP:연결포트 install -r rail-dial-aod-1.0.0.apk`로 워치를 지정합니다. 설치 후 워치에서 **시계 화면 추가 → Rail Dial AOD**를 선택합니다.

아직 실제 워치 실행 검증은 수행하지 못했습니다. 개발용 서명을 사용하므로 향후 빌드에서 서명키가 바뀌면 이 별도 워치페이스를 삭제한 후 재설치해야 할 수 있습니다.
