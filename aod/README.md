# Rail Dial AOD 1.0.1

Rail Dial 1.0.2의 AOD 디자인을 일반 화면으로 사용하는 별도 워치페이스입니다.

- 검은 배경, 12개 회색 눈금, 얇은 회색 시침·분침을 그대로 사용합니다.
- 초침은 없으며, 일반 화면과 절전 화면(AOD)에 같은 디자인이 표시됩니다. 화면 밝기와 AOD 켜기 여부는 워치 설정을 따릅니다.
- 표시 이름: **Rail Dial AOD**
- 별도 앱 ID: `com.example.raildial.aod` — 기존 `com.example.raildial`과 함께 설치할 수 있습니다.
- Wear OS 4 이상. 갤럭시 워치에 직접 설치합니다.

## 빌드
저장소 Actions에서 **Build Rail Dial AOD APK**를 실행합니다. 완료 후 **rail-dial-aod-1.0.1-unsigned-build**에는 서명 전 APK와 패키지 검사 결과가 들어 있습니다. 설치는 별도로 제공된 최종 서명 APK를 사용하세요.

로컬 서명 전 빌드: `gradle :aod:assembleRelease`

## 설치
워치에 이미 무선 연결된 PC라면, `adb.exe`와 APK가 있는 폴더에서 다음을 실행합니다.

```bat
adb install -r rail-dial-aod-1.0.1.apk
```

연결된 기기가 여러 대이면 `adb -s 워치IP:연결포트 install -r rail-dial-aod-1.0.1.apk`로 워치를 지정합니다. 설치 후 워치에서 **시계 화면 추가 → Rail Dial AOD**를 선택합니다.

### 1.0.1 변경 사항
시침·분침을 정수 시각·분 데이터에만 연결해 분 단위로 갱신하고, 바늘의 투명 여백을 줄였습니다. 기존 검은색 AOD 디자인을 유지합니다. 라이트/다크 선택과 굵은 바늘을 원하면 기본형 Rail Dial 1.1.0을 사용하세요.

실제 워치 배터리 소모 원인과 절감률은 아직 확인하지 못했습니다. 설치 후 무선 디버깅과 ADB 디버깅을 꺼 주세요.

이번 배포부터 고정 배포용 키를 별도로 보관합니다. 이전 1.0.0 개발용 APK와 서명이 달라 **기존 Rail Dial AOD를 한 번 삭제한 뒤 설치**해야 합니다. 기본형 Rail Dial에는 영향을 주지 않습니다. 새 개인 키와 비밀번호는 공개 저장소에 올리지 않습니다.
