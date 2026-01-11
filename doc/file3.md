# Legacy Sales MCP Server - 사용자 가이드

  

영업 시스템의 재고, 파이프라인(주문), 리포트 조회 및 사용자 목록 조회 기능을 MCP(Model Context Protocol) 툴로 제공합니다. AI 에이전트가 자연어로 영업 현황을 파악하고 데이터를 추출할 수 있도록 돕습니다.

  

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

  

---

  

## 시스템 개요

- **대상 시스템**: legacy-sales (Spring Boot, 세션 기반 인증)

- **용도**: 재고 현황 조회, 영업 파이프라인 추적, 관리자용 리포트 추출

- **특징**: `PermissionInterceptor`로 인해 모든 API 접근 시 세션 로그인(JSESSIONID) 필수

  

## 웹 애플리케이션 접근

- **메인 URL**: `https://sales.4.230.72.248.nip.io`

- **프로토콜**: HTTPS

- **접근 방법**: 브라우저 접속 후 `/login` 폼 로그인

- **테스트 계정**: `20010001` / `password123` (Admin)

  

## 주요 기능

1. **재고 검색**: 지역, 물류센터, 품목 유형별 실시간 재고 조회

2. **파이프라인 검색**: 영업 기회 및 주문 현황 조회

3. **데이터 추출**: 전체 재고 및 파이프라인 데이터 엑셀 다운로드용 API 제공 (Admin/Manager)

4. **사용자 조회**: 전체 영업 시스템 사용자 목록 (Admin)

  

## 서버 정보

- **서버 이름**: Sales System MCP Server

- **서버 ID**: `771a18ddd8c74a73af24388a613b9d75`

- **Slug**: `sales-system-mcp-server`

- **Transport**: SSE (Server-Sent Events)

- **내부 URL**: `http://legacy-mcp-sales-server.legacy-mcp.svc.cluster.local:8000/sse`

- **Namespace**: `legacy-mcp`

- **Service**: `legacy-mcp-sales-server`

- **Port**: 8000

- **Dify URL**: `https://mcp-gateway.koreacentral.cloudapp.azure.com/sse?server_id=771a18ddd8c74a73af24388a613b9d75`

  

## 제공 툴

- **인증**: `login`

- **재고**: `search_inventory`, `get_inventory_report`

- **영업**: `search_pipeline`, `get_pipeline_report`

- **관리**: `get_sales_users`

  

## 툴 상세 설명

  

### 1) 인증 (선택 사항)

- `login(username?, password?)`

    - 시스템에 로그인합니다.

    - 인자를 생략하면 기본 관리자 계정(`20010001`)으로 로그인합니다.

    - 대부분의 다른 툴은 호출 시 자동으로 로그인을 수행하므로, 명시적으로 사용자를 변경하고 싶을 때 사용합니다.

  

### 1) 재고 관리

- `search_inventory(region?, center_name?, item_type?)`

    - 특정 조건으로 재고를 검색합니다.

    - 예: "서울 지역 전자제품 재고 보여줘" -> `search_inventory(region="Seoul", item_type="Electronics")`

- `get_inventory_report()`

    - (관리자용) 전체 재고 리스트를 JSON 형태로 추출합니다.

  

### 2) 파이프라인(영업) 관리

- `search_pipeline(region?, status?)`

    - 영업 주문(파이프라인) 상태를 조회합니다.

    - 예: "배송 중인 주문 찾아줘" -> `search_pipeline(status="Shipped")`

- `get_pipeline_report()`

    - (관리자용) 전체 파이프라인 리스트를 JSON 형태로 추출합니다.

  

### 3) 사용자 관리

- `get_sales_users()`

    - (관리자용) 시스템에 등록된 모든 사용자 정보를 조회합니다.

  

## API 사용 가이드

- **인증 방식**: MCP Server가 내부적으로 `/login`을 호출하여 세션을 맺고 유지합니다. 사용자는 별도 인증이 필요 없습니다.

- **연결**: Legacy System의 `PermissionInterceptor`를 통과하기 위해, MCP Server는 `requests.Session`을 사용하여 쿠키를 관리합니다.

  

## 배포 및 등록

  

### Docker 이미지 빌드 및 푸시

```bash

docker build -t agenticaidevacr45141.azurecr.io/legacy-mcp-sales:v1.0 .

az acr login --name agenticaidevacr45141

docker push agenticaidevacr45141.azurecr.io/legacy-mcp-sales:v1.0

```

  

### Kubernetes 배포

```bash

# deployment.yaml 파일이 존재한다고 가정 (혹은 Helm 차트 사용)

kubectl apply -f k8s/deployment.yaml

kubectl apply -f k8s/service.yaml

```

  

### MCP Gateway 등록

```bash

./register_to_gateway.sh

```

스크립트 실행 후 출력되는 **Server ID**를 확인하여 기록해두세요. 재등록 시에도 Gateway가 이름(`Sales System MCP Server`)을 기준으로 식별하여 ID를 유지하거나 갱신합니다.

  

## 환경 변수

- `API_BASE_URL`: Legacy Sales App URL (기본: `http://sales-app-service.legacy-sales.svc.cluster.local`)

- `SALES_ADMIN_USER`: 관리자 ID (기본: `20010001`)

- `SALES_ADMIN_PASSWORD`: 관리자 비밀번호 (기본: `password123`)

- `PORT`: MCP 서버 포트 (기본: `8000`)