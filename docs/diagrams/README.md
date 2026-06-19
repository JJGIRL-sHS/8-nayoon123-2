# 다이어그램 에셋

`issue-2-거리-기반-자동-제어-시스템.md` 문서에 쓰이는 다이어그램입니다.
본문에는 Mermaid 코드 블록이 그대로 들어가 GitHub에서 자동 렌더되고,
여기 있는 `.svg` / `.png` 는 결과보고서(.hwpx)나 발표자료에 붙여 넣기 위한 별도 에셋입니다.

| 파일 | 종류 | 내용 |
| --- | --- | --- |
| `01-system-architecture` | flowchart | 전체 시스템 아키텍처 · 데이터 흐름 (아두이노 ↔ Streamlit) |
| `02-message-protocol` | sequence | JSON 메시지 송수신 시퀀스 (sonar / led) |
| `03-sensor-timing` | sequence | 초음파 센서 측정 타이밍 (Trig → Echo → 거리 계산) |
| `04-data-pipeline` | flowchart | `fetch_data()` 데이터 수집 · 필터링 파이프라인 |
| `05-auto-control-flow` | flowchart | `control_traffic()` 자동 제어 판단 흐름도 |
| `06-app-structure` | flowchart | Streamlit 앱 구조 (app.py → dashboard.py / control.py) |
| `07-wiring-diagram` | 연결도(수기 SVG) | 회로 배선도 — Arduino Uno ↔ HC-SR04 ↔ 신호등 LED 모듈 핀 연결 |

01~06번 다이어그램은 `*.mmd`(Mermaid 소스) → `*.svg`(벡터) → `*.png`(2배 해상도) 세 가지로 제공됩니다.
07번 회로 배선도는 Mermaid로 표현이 어려워 **손수 작성한 SVG**(`.mmd` 없음)에서 PNG를 뽑았습니다.

## 다시 렌더링하기

`.mmd` 소스를 수정한 뒤, 이 폴더에서 아래를 실행하면 SVG/PNG가 갱신됩니다.

```bash
for f in 01-system-architecture 02-message-protocol 03-sensor-timing \
         04-data-pipeline 05-auto-control-flow 06-app-structure; do
  npx -y @mermaid-js/mermaid-cli@latest -i "$f.mmd" -o "$f.svg" -p .puppeteer.json -c .mermaid.json -b white
  npx -y @mermaid-js/mermaid-cli@latest -i "$f.mmd" -o "$f.png" -p .puppeteer.json -c .mermaid.json -b white -s 2
done
```

07번 회로 배선도는 `.svg` 를 직접 수정한 뒤 PNG만 다시 뽑으면 됩니다.

```bash
rsvg-convert -z 2 07-wiring-diagram.svg -o 07-wiring-diagram.png
```

- `.mermaid.json` : 한글 폰트(Apple SD Gothic Neo)와 보라색(`#8917E0`) 테마 설정
- `.puppeteer.json` : 헤드리스 Chromium 실행 옵션
- 본문 Mermaid 블록을 수정했다면 해당 `.mmd` 도 같이 맞춰 주세요(내용 동일).
