# Purchasing MCP Server - 사용자 가이드

  

구매요청, 계약, 공급업체, 품목, 입고(기성), 권한 관리 기능을 MCP(Model Context Protocol) 툴로 제공합니다. AI 에이전트가 자연어로 구매 업무를 처리할 수 있도록 돕습니다.

  

## 목차

1. [시스템 개요](#시스템-개요)

2. [웹 애플리케이션 접근](#웹-애플리케이션-접근)

3. [주요 기능](#주요-기능)

4. [서버 정보](#서버-정보)

5. [제공 툴](#제공-툴)

6. [툴 상세 설명](#툴-상세-설명)

7. [API 사용 가이드](#api-사용-가이드)

8. [배포 및 등록](#배포-및-등록)

9. [환경 변수](#환경-변수)

10. [테스트 계정](#테스트-계정)

11. [모니터링 & 트러블슈팅](#모니터링--트러블슈팅)

13. [개발 정보](#개발-정보)

14. [기술 스택](#기술-스택)

15. [변경 이력](#변경-이력)

16. [지원](#지원)

  

---

  

## 시스템 개요

- **대상 시스템**: legacy-purchasing (Spring Boot JSP, 세션 기반 인증)

- **용도**: 구매요청/계약/공급업체/품목/입고 관리 및 권한 관리

- **특징**: HTML 테이블 파싱 기반, 세션 로그인 후 쿠키 유지

  

## 웹 애플리케이션 접근

- **메인 URL**: `https://purchasing.20.196.109.91.nip.io`

- **프로토콜**: HTTPS

- **접근 방법**: 브라우저 접속 후 `/login` 폼 로그인(세션 쿠키)

  

## 주요 기능

1. 구매요청 목록 조회, 승인/반려(ADMIN)

2. 계약/공급업체/품목/입고(기성) 목록 조회

3. 금액 합계 기반 공급업체 순위 집계

4. 사용자 권한 변경(ADMIN)

## Dify에서 로그인 함수 호출 후 사용
![image.png](/.attachments/image-938e4d2b-d73d-49cd-83b6-efb825d294db.png) 

## 서버 정보

- **서버 이름**: Legacy Purchasing MCP Server

- **서버 ID**: `378d574261974f14b29ee234946a8ba0`

- **Slug**: `legacy-purchasing-mcp-server`

- **Transport**: SSE (Server-Sent Events)

- **상태**: Active & Reachable

- **내부 URL**: `http://legacy-purchasing-mcp-server.legacy-mcp.svc.cluster.local:8000/sse`

- **Namespace**: `legacy-mcp`

- **Service**: `legacy-purchasing-mcp-server`

- **Port**: 8000

- **dify URL**: `https://mcp-gateway.koreacentral.cloudapp.azure.com/sse?server_id=378d574261974f14b29ee234946a8ba0`

  

## 제공 툴

- **인증**: `login`

- **구매요청**: `list_requests`, `approve_request`, `reject_request`

- **계약/공급/품목/입고**: `list_contracts`, `list_suppliers`, `list_items`, `list_receivings`

- **권한/집계**: `update_user_role`(ADMIN), `top_suppliers`(기본 최소 1억)

  

## 툴 상세 설명

  

### 1) 로그인

- `login(username?, password?)`

- 세션 쿠키(JSESSIONID) 확보. 미입력 시 `PURCHASING_USERNAME`/`PURCHASING_PASSWORD` 사용.

```

사용자: 로그인해 줘

AI: [login 호출] -> {"success": true}

```

  

### 2) 구매요청

- `list_requests()`: 요청자/금액/상태 등 목록 파싱.

- `approve_request(req_id)` (ADMIN): 구매요청 승인.

- `reject_request(req_id)` (ADMIN): 구매요청 반려.

```

사용자: REQ123 승인해줘

AI: [approve_request 호출] req_id=REQ123

```

  

### 3) 계약/공급/품목/입고

- `list_contracts()`: 계약ID, 공급업체, 금액, 통화, 상태, 승인자 등.

- `list_suppliers()`: 사업자번호, 담당자, 이메일, 전화, 국가.

- `list_items()`: 품목ID, 코드, 규격, 단위, MTG.

- `list_receivings()`: 입고/기성 ID, 회사, 상태, 계약ID, 품목, 플랜트.

```

사용자: 공급업체 목록 보여줘

AI: [list_suppliers 호출]

```

  

### 4) 권한 & 집계

- `update_user_role(user_id, role_code)` (ADMIN): 역할 변경. `ADMIN/USER/EXECUTIVE`.

- `top_suppliers(min_amount=100000000)`: 계약 금액 합계 기준 상위 공급업체(내림차순), 담당자/연락처 포함.

```

사용자: 2억 이상 공급업체 순위 알려줘

AI: [top_suppliers 호출] min_amount=200000000

```

  

## API 사용 가이드

- 별도 공개 REST API 없음. MCP 툴은 서버 HTML을 파싱하여 동작.

- 인증: `/login` 폼 POST 후 세션 쿠키 유지.

- CSRF: 비활성 전제. 활성화 시 토큰 추출 로직 추가 필요.

  

### 주요 테이블

- 웹 파싱 결과 기반으로 추정: 구매요청/계약/공급업체/품목/입고 관련 테이블 존재. 정확한 스키마는 DB 확인 후 업데이트 필요.

  

## 배포 및 등록

  

### 이미지 빌드

```bash

docker build -t agenticaidevacr45141.azurecr.io/legacy-purchasing-mcp-server:v1.0 .

```

  

### ACR 푸시

```bash

az acr login --name agenticaidevacr45141

docker push agenticaidevacr45141.azurecr.io/legacy-purchasing-mcp-server:v1.0

```

  

### Kubernetes 배포/업데이트

```bash

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

  

# 기존 배포 이미지 교체 시

kubectl set image deployment/legacy-purchasing-mcp-server \

  mcp-server=agenticaidevacr45141.azurecr.io/legacy-purchasing-mcp-server:v1.0 \

  -n legacy-mcp

```

  

### MCP Gateway 등록/확인

```bash

./register_to_gateway.sh  # 등록 (Git Bash 권장)

kubectl port-forward -n mcp-gateway svc/mcp-gateway 4444:4444

curl http://localhost:4444/gateways | grep "Legacy Purchasing MCP Server"

```

  

## 환경 변수

- `PURCHASING_BASE_URL`: 기본 `https://purchasing.20.196.109.91.nip.io`

- `PURCHASING_USERNAME`: 기본 로그인 ID (login 미입력 시 사용)

- `PURCHASING_PASSWORD`: 기본 비밀번호 (login 미입력 시 사용)

- `PORT`: MCP 서버 포트 (기본 8000)

  

## 테스트 계정

- 로그인 계정은 환경변수로 주입 권장. 공개 테스트 계정은 별도 제공되지 않음.

  

## 모니터링 & 트러블슈팅

- Pod 상태: `kubectl get pods -n legacy-mcp`

- 로그: `kubectl logs -f deployment/legacy-purchasing-mcp-server -n legacy-mcp`

- Gateway 등록 확인: `kubectl get pods -n mcp-gateway` / `curl http://localhost:4444/gateways`

- 화면 파서 주의: HTML 테이블 컬럼/구조 변경 시 파서 수정 필요

- CSRF 활성 시: 토큰 추출/전달 로직 추가 필요

- 관리자 권한 필요: `approve_request`, `reject_request`, `update_user_role`

  

## 개발 정보

- **Namespace**: `legacy-mcp`

- **Service**: `legacy-purchasing-mcp-server`

- **Gateway Registration**: MCP Gateway (`mcp-gateway` namespace)

  

## 기술 스택

- **Framework**: FastMCP 2.13.2

- **Language**: Python 3.11

- **Transport**: SSE

- **Container**: Docker

- **Orchestration**: Kubernetes (AKS)

- **Registry**: agenticaidevacr45141.azurecr.io

  

## 변경 이력

- v1.0 (2025-12-08): 초기 배포, 로그인/구매요청/계약/공급/품목/입고/권한/집계 툴 제공, Gateway 등록 완료 (ID: `378d574261974f14b29ee234946a8ba0`)

  

## 지원

- 문의/이슈: MCP Gateway 등록 상태 및 Pod 로그 확인 후 담당자에게 공유