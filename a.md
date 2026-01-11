# Chunking Results for file1.md

**Original file size:** 18,513 characters
**Total chunks:** 27
**Chunk size:** 1000 characters
**Chunk overlap:** 200 characters

---

## Chunk 1

**Size:** 619 characters

```
# SATIS (Sales And Tracking Information System) - 사용자 가이드

  

## 📋 목차

1. [시스템 개요](#시스템-개요)

2. [웹 애플리케이션 접근](#웹-애플리케이션-접근)

3. [데이터베이스 연결 정보](#데이터베이스-연결-정보)

4. [주요 기능](#주요-기능)

5. [테스트 계정](#테스트-계정)

6. [로컬 개발 환경](#로컬-개발-환경)

7. [Kubernetes 배포](#kubernetes-배포)

8. [문제 해결](#문제-해결)

  

---

  

## 🎯 시스템 개요

  

**SATIS (Sales And Tracking Information System)**는 석유 제품 영업 및 물류 업무를 지원하는 웹 애플리케이션입니다.

  

- **구분**: **[레거시 애플리케이션]**

- **배포 환경**: Azure Kubernetes Service (AKS)

- **네임스페이스**: `legacy-sales`

- **프레임워크**: Spring Boot 2.7.18 (Java 11)

- **뷰 엔진**: JSP/JSTL

- **데이터베이스**: Oracle Database XE 21c

  

---
```

---

## Chunk 2

**Size:** 775 characters

```
## 🌐 웹 애플리케이션 접근

  

### 메인 애플리케이션 **[프로덕션]**

- **URL**: https://sales.4.230.72.248.nip.io

- **프로토콜**: HTTPS (Let's Encrypt SSL 인증서)

- **접근 방법**: 웹 브라우저에서 직접 접속

  

### 로컬 개발 환경

- **URL**: http://localhost:8080

- **접근 방법**: Docker Compose 또는 Maven으로 실행

  

### 주요 기능

  

1. **대시보드**

   - 지역별 재고 통계

   - 품목별 재고 현황 (휘발유, 경유, 등유)

   - 재고율 시각화

   - 실시간 데이터 업데이트

  

2. **재고 현황 관리**

   - 재고 상세 조회 (지역, 물류센터, 품목별)

   - 날짜 범위 검색

   - 페이지네이션 및 정렬

   - Excel 다운로드

  

3. **송유/배선 계획**

   - 송유관 주문 조회

   - 상태별 필터링 (Planned, Confirmed, Completed, Cancelled)

   - Excel 다운로드

  

4. **물류센터 관리**

   - 재고/출하 상세조회

   - 물류센터별 상세 정보

  

5. **관리자 기능** (ADMIN 권한 필요)

   - 사용자 관리 (역할 변경, 상태 변경)

   - 권한 관리 (역할별 메뉴 권한 설정)

   - 활용도 평가 (로그인/메뉴 접근 이력)

   - 코드 관리

  

---
```

---

## Chunk 3

**Size:** 920 characters

```
## 💾 데이터베이스 연결 정보

  

### Oracle XE 21c (satis-oracle) **[애플리케이션 DB]**

  

> [!IMPORTANT]

> 클러스터 내부 또는 포트 포워딩을 통해서만 접속 가능합니다.

  
| 항목 | 값 |
|------|-----|
| **Internal IP** | `oracle-db.legacy-sales.svc.cluster.local` |
| **Port** | `1521` |
| **SID** | `xepdb1` |
| **Username** | `SYSTEM` |
| **Password** | `satis` |

  

**연결 예시 (클러스터 내부):**

```bash

sqlplus SYSTEM/satis@oracle-db.legacy-sales.svc.cluster.local:1521/xepdb1

```
  

**연결 예시 (로컬에서 포트 포워딩):**

```bash

# 1. 포트 포워딩 설정

kubectl port-forward -n legacy-sales svc/oracle-db 1522:1521

  

# 2. 로컬에서 연결

sqlplus SYSTEM/satis@localhost:1522/xepdb1

```

  

**주요 테이블:**

- `SATIS_USERS` - 사용자 정보 (42명)

- `INVENTORY` - 재고 정보 (15개 샘플 데이터)

- `PIPELINE_ORDER` - 송유관 주문 (50개 샘플 데이터)

- `MENU_PERMISSIONS` - 메뉴 권한

- `USER_ACTIVITY_LOG` - 사용자 활동 로그

  

**데이터 초기화:**

- `DataLoader.java`: 사용자 데이터 자동 생성

- `DataInitializer.java`: 재고, 권한 데이터 자동 생성

  

---
```

---

## Chunk 4

**Size:** 693 characters

```
## 📌 주요 기능

  

### 1. 대시보드 (Dashboard)

  

**접근 경로:** `/dashboard`

  

**API 엔드포인트:**

```http

GET /api/dashboard/stats?region={region}

```

  

**파라미터:**

- `region`: 지역 필터 (전국, 수도권, 강원, 충청, 호남, 영남, 제주)

  

**응답 예시:**

```json

{

  "totalStock": 450000,

  "totalCapacity": 600000,

  "utilizationRate": 75.0,

  "stockByRegion": {

    "수도권": 150000,

    "강원": 80000,

    "충청": 70000,

    "호남": 60000,

    "영남": 90000

  },

  "stockByItem": {

    "휘발유": 200000,

    "경유": 180000,

    "등유": 70000

  },

  "recentOrders": 15000,

  "recentShipments": 12000

}

```

  

**cURL 예시:**

```bash

curl "https://sales.4.230.72.248.nip.io/api/dashboard/stats?region=전국"

```

  

---
```

---

## Chunk 5

**Size:** 998 characters

```
### 2. 재고 현황 관리 (Inventory Management)

  

**접근 경로:** `/detail`

  

**API 엔드포인트:**

```http

GET /api/inventory/search?region={region}&centerName={centerName}&itemType={itemType}&startDate={startDate}&endDate={endDate}&page={page}&size={size}

```

  

**파라미터:**

- `region`: 지역 필터 (선택사항)

- `centerName`: 물류센터명 필터 (선택사항)

- `itemType`: 품목 필터 (선택사항)

- `startDate`: 시작일 (yyyy-MM-dd, 선택사항)

- `endDate`: 종료일 (yyyy-MM-dd, 선택사항)

- `page`: 페이지 번호 (기본값: 0)

- `size`: 페이지 크기 (기본값: 10)

  

**응답 예시:**

```json

{

  "content": [

    {

      "id": 1,

      "region": "수도권",

      "centerName": "서울물류센터",

      "itemType": "휘발유",

      "currentStock": 45000,

      "capacity": 60000,

      "orderAmount": 3000,

      "shipmentAmount": 2500,

      "updatedAt": "2024-01-15T10:30:00"

    }

  ],

  "totalElements": 15,

  "totalPages": 2,

  "size": 10,

  "number": 0

}

```

  

**Excel 다운로드:**

```http

GET /api/inventory/excel?region={region}&centerName={centerName}&itemType={itemType}
```

---

## Chunk 6

**Size:** 445 characters

```
"totalElements": 15,

  "totalPages": 2,

  "size": 10,

  "number": 0

}

```

  

**Excel 다운로드:**

```http

GET /api/inventory/excel?region={region}&centerName={centerName}&itemType={itemType}

```

  

**cURL 예시:**

```bash

# 재고 검색

curl "https://sales.4.230.72.248.nip.io/api/inventory/search?region=수도권&itemType=휘발유&page=0&size=10"

  

# Excel 다운로드

curl -O "https://sales.4.230.72.248.nip.io/api/inventory/excel?region=수도권"

```

  

---
```

---

## Chunk 7

**Size:** 934 characters

```
### 3. 송유/배선 계획 (Pipeline Order)

  

**접근 경로:** `/pipeline-order`

  

**API 엔드포인트:**

```http

GET /api/pipeline/search?region={region}&status={status}&page={page}&size={size}

```

  

**파라미터:**

- `region`: 지역 필터 (선택사항)

- `status`: 상태 필터 (Planned, Confirmed, Completed, Cancelled, 선택사항)

- `page`: 페이지 번호 (기본값: 0)

- `size`: 페이지 크기 (기본값: 10)

  

**응답 예시:**

```json

{

  "content": [

    {

      "id": 1,

      "orderDate": "2024-01-15",

      "region": "수도권",

      "pipelineName": "Pipeline-1",

      "itemType": "휘발유",

      "quantity": 5000,

      "status": "Confirmed"

    }

  ],

  "totalElements": 50,

  "totalPages": 5,

  "size": 10,

  "number": 0

}

```

  

**Excel 다운로드:**

```http

GET /api/pipeline/excel?region={region}&status={status}

```

  

**cURL 예시:**

```bash

# 주문 검색

curl "https://sales.4.230.72.248.nip.io/api/pipeline/search?region=수도권&status=Confirmed&page=0&size=10"

  

# Excel 다운로드
```

---

## Chunk 8

**Size:** 257 characters

```
```

  

**cURL 예시:**

```bash

# 주문 검색

curl "https://sales.4.230.72.248.nip.io/api/pipeline/search?region=수도권&status=Confirmed&page=0&size=10"

  

# Excel 다운로드

curl -O "https://sales.4.230.72.248.nip.io/api/pipeline/excel?status=Confirmed"

```

  

---
```

---

## Chunk 9

**Size:** 999 characters

```
### 4. 사용자 관리 (User Management) - ADMIN 전용

  

**접근 경로:** `/user-management`

  

**API 엔드포인트:**

  

**사용자 목록 조회:**

```http

GET /api/users

```

  

**응답 예시:**

```json

[

  {

    "id": 1,

    "empId": "EMP001",

    "empNo": "20010001",

    "username": "20010001",

    "name": "박태준",

    "department": "대표이사",

    "role": "ADMIN",

    "email": "ceo@company.com",

    "phone": "010-1000-0001",

    "status": "ACTIVE",

    "lastLogin": "2024-01-15T09:30:00",

    "loginCount": 50

  }

]

```

  

**사용자 역할 변경:**

```http

PUT /api/users/{id}/role

Content-Type: application/json

  

{

  "role": "MANAGER"

}

```

  

**사용자 상태 변경:**

```http

PUT /api/users/{id}/status

Content-Type: application/json

  

{

  "status": "INACTIVE"

}

```

  

**cURL 예시:**

```bash

# 사용자 목록 조회

curl "https://sales.4.230.72.248.nip.io/api/users"

  

# 역할 변경

curl -X PUT "https://sales.4.230.72.248.nip.io/api/users/1/role" \

  -H "Content-Type: application/json" \

  -d '{"role":"MANAGER"}'
```

---

## Chunk 10

**Size:** 311 characters

```
# 역할 변경

curl -X PUT "https://sales.4.230.72.248.nip.io/api/users/1/role" \

  -H "Content-Type: application/json" \

  -d '{"role":"MANAGER"}'

  

# 상태 변경

curl -X PUT "https://sales.4.230.72.248.nip.io/api/users/1/status" \

  -H "Content-Type: application/json" \

  -d '{"status":"INACTIVE"}'

```

  

---
```

---

## Chunk 11

**Size:** 877 characters

```
### 5. 권한 관리 (Permission Management) - ADMIN 전용

  

**접근 경로:** `/permission-management`

  

**API 엔드포인트:**

  

**권한 목록 조회:**

```http

GET /api/permissions?role={role}

```

  

**응답 예시:**

```json

[

  {

    "id": 1,

    "role": "ADMIN",

    "menuId": "dashboard",

    "canRead": true,

    "canWrite": true

  },

  {

    "id": 2,

    "role": "ADMIN",

    "menuId": "inventory",

    "canRead": true,

    "canWrite": true

  }

]

```

  

**권한 수정:**

```http

PUT /api/permissions/{id}

Content-Type: application/json

  

{

  "canRead": true,

  "canWrite": false

}

```

  

**cURL 예시:**

```bash

# 권한 목록 조회

curl "https://sales.4.230.72.248.nip.io/api/permissions?role=MANAGER"

  

# 권한 수정

curl -X PUT "https://sales.4.230.72.248.nip.io/api/permissions/5" \

  -H "Content-Type: application/json" \

  -d '{"canRead":true,"canWrite":false}'

```

  

---
```

---

## Chunk 12

**Size:** 999 characters

```
### 6. 활용도 평가 (Usage Evaluation) - ADMIN 전용

  

**접근 경로:** `/usage-evaluation`

  

**API 엔드포인트:**

  

**활동 로그 조회:**

```http

GET /api/usage/logs?userId={userId}&startDate={startDate}&endDate={endDate}

```

  

**응답 예시:**

```json

[

  {

    "id": 1,

    "userId": 1,

    "action": "LOGIN",

    "menuPath": null,

    "menuName": null,

    "ipAddress": "192.168.1.100",

    "createdAt": "2024-01-15T09:00:00"

  },

  {

    "id": 2,

    "userId": 1,

    "action": "MENU_ACCESS",

    "menuPath": "/dashboard",

    "menuName": "대시보드",

    "ipAddress": "192.168.1.100",

    "createdAt": "2024-01-15T09:01:00"

  }

]

```

  

**사용 통계 조회:**

```http

GET /api/usage/stats?startDate={startDate}&endDate={endDate}

```

  

**응답 예시:**

```json

{

  "totalLogins": 150,

  "activeUsers": 38,

  "averageDailyLogins": 25,

  "topMenu": "dashboard",

  "menuAccessStats": {

    "dashboard": 200,

    "inventory": 150,

    "pipeline": 100,

    "user": 50

  }

}

```

  

**cURL 예시:**
```

---

## Chunk 13

**Size:** 446 characters

```
"averageDailyLogins": 25,

  "topMenu": "dashboard",

  "menuAccessStats": {

    "dashboard": 200,

    "inventory": 150,

    "pipeline": 100,

    "user": 50

  }

}

```

  

**cURL 예시:**

```bash

# 활동 로그 조회

curl "https://sales.4.230.72.248.nip.io/api/usage/logs?userId=1&startDate=2024-01-01&endDate=2024-01-31"

  

# 사용 통계 조회

curl "https://sales.4.230.72.248.nip.io/api/usage/stats?startDate=2024-01-01&endDate=2024-01-31"

```

  

---
```

---

## Chunk 14

**Size:** 867 characters

```
## 👥 테스트 계정

  

### 관리자 (ADMIN)

  

| 사번 | 직원번호 | 비밀번호 | 이름 | 부서 |
|------|----------|----------|------|------|
| EMP001 | 20010001 | password123 | 박태준 | 대표이사 |
| EMP002 | 20120002 | password123 | 김상훈 | 경영지원본부 |

  

### 매니저 (MANAGER)

  

| 사번 | 직원번호 | 비밀번호 | 이름 | 부서 |
|------|----------|----------|------|------|
| EMP003 | 20120003 | password123 | 이정민 | 사업본부 |
| EMP004 | 20120004 | password123 | 최기영 | 기술본부 |
| EMP019 | 20100019 | password123 | 김지은 | 생산1팀 |

  

### 일반 사용자 (USER)

  
| 사번 | 직원번호 | 비밀번호 | 이름 | 부서 |
|------|----------|----------|------|------|
| EMP006 | 20240006 | password123 | 이민지 | 데이터팀 |
| EMP012 | 20160012 | password123 | 한준호 | 구매팀 |
| EMP013 | 20170013 | password123 | 류수빈 | 고객서비스팀 |

  

> [!TIP]

> - 로그인 시 직원번호(empNo)를 사용합니다

> - 모든 계정의 기본 비밀번호는 `password123`입니다

> - 총 42명의 사용자 계정이 있습니다 (ADMIN: 2명, MANAGER: 8명, USER: 32명)

  

---
```

---

## Chunk 15

**Size:** 801 characters

```
## 🔧 로컬 개발 환경

  

### 사전 요구사항

- Java 11

- Maven 3.6+

- Docker Desktop

- Docker Compose

  

### 방법 1: Docker Compose (권장)

  

**전체 스택 실행:**

```bash

# 프로젝트 디렉토리로 이동

cd legacy-sales

  

# Docker Compose로 실행

docker-compose up -d

  

# 로그 확인

docker-compose logs -f app

  

# 접속: http://localhost:8080

```

  

**종료:**

```bash

docker-compose down

  

# 볼륨까지 삭제 (데이터 초기화)

docker-compose down -v

```

  

### 방법 2: Maven 직접 실행

  

**Oracle DB 실행:**

```bash

docker run -d --name oracle-xe \

  -p 1521:1521 \

  -e ORACLE_PASSWORD=satis \

  gvenzl/oracle-xe:21-slim

```

  

**애플리케이션 빌드 및 실행:**

```bash

# 빌드

mvn clean package -DskipTests

  

# 실행

mvn spring-boot:run

  

# 또는 WAR 파일 직접 실행

java -jar target/sales-0.0.1-SNAPSHOT.war

  

# 접속: http://localhost:8080

```

  

---
```

---

## Chunk 16

**Size:** 202 characters

```
## ☸️ Kubernetes 배포

  

### 자동 배포 (deploy.sh)

  

```bash

./deploy.sh

```

  

스크립트가 자동으로 수행하는 작업:

1. WAR 파일 빌드

2. Docker 이미지 빌드

3. Azure Container Registry에 푸시

4. Kubernetes 리소스 배포

5. 배포 상태 확인
```

---

## Chunk 17

**Size:** 929 characters

```
### 수동 배포

  

**1. 이미지 빌드 및 푸시:**

```bash

# ACR 로그인

az acr login --name agenticaidevacr45141

  

# 애플리케이션 이미지 빌드

docker build -t agenticaidevacr45141.azurecr.io/satis-app:latest .

  

# ACR에 푸시

docker push agenticaidevacr45141.azurecr.io/satis-app:latest

```

  

**2. Kubernetes 리소스 배포:**

```bash

# AKS 자격증명 가져오기

az aks get-credentials --resource-group <resource-group> --name <aks-cluster-name>

  

# Namespace 생성

kubectl create namespace legacy-sales

  

# Oracle DB 배포

kubectl apply -f kubernetes/oracle-deployment.yaml

  

# 애플리케이션 배포

kubectl apply -f kubernetes/app-deployment.yaml

  

# Ingress 배포

kubectl apply -f kubernetes/ingress.yaml

```

  

**3. 배포 상태 확인:**

```bash

# Pod 상태 확인

kubectl get pods -n legacy-sales

  

# 서비스 확인

kubectl get svc -n legacy-sales

  

# Ingress 확인

kubectl get ingress -n legacy-sales

  

# 로그 확인

kubectl logs -n legacy-sales -l app=satis-app --tail=100 -f

```
```

---

## Chunk 18

**Size:** 992 characters

```
### 유용한 kubectl 명령어

  

**Pod 관리:**

```bash

# Pod 목록

kubectl get pods -n legacy-sales

  

# 특정 Pod 로그 확인

kubectl logs -n legacy-sales <pod-name> --tail=100 -f

  

# Pod 재시작

kubectl rollout restart deployment/satis-app -n legacy-sales

  

# Pod 상세 정보

kubectl describe pod <pod-name> -n legacy-sales

```

  

**서비스 관리:**

```bash

# 서비스 목록

kubectl get svc -n legacy-sales

  

# 서비스 상세 정보

kubectl describe svc satis-app -n legacy-sales

```

  

**데이터베이스 관리:**

```bash

# Oracle Pod 접속

kubectl exec -it -n legacy-sales <oracle-pod-name> -- bash

  

# Oracle SQL*Plus 접속

kubectl exec -it -n legacy-sales <oracle-pod-name> -- sqlplus SYSTEM/satis@xepdb1

  

# 데이터베이스 백업

kubectl exec -n legacy-sales <oracle-pod-name> -- \

  exp SYSTEM/satis@xepdb1 file=/tmp/backup.dmp full=y

```

  

**문제 해결:**

```bash

# 이벤트 확인

kubectl get events -n legacy-sales --sort-by='.lastTimestamp'

  

# 리소스 사용량 확인

kubectl top pods -n legacy-sales

kubectl top nodes

  

# ConfigMap/Secret 확인
```

---

## Chunk 19

**Size:** 279 characters

```
**문제 해결:**

```bash

# 이벤트 확인

kubectl get events -n legacy-sales --sort-by='.lastTimestamp'

  

# 리소스 사용량 확인

kubectl top pods -n legacy-sales

kubectl top nodes

  

# ConfigMap/Secret 확인

kubectl get configmap -n legacy-sales

kubectl get secret -n legacy-sales

```

  

---
```

---

## Chunk 20

**Size:** 600 characters

```
## 🆘 문제 해결

  

### 1. 로그인이 안 될 때

  

**증상:** 로그인 페이지에서 인증 실패

  

**확인 사항:**

```bash

# 1. 애플리케이션 로그 확인

kubectl logs -n legacy-sales -l app=satis-app --tail=50

  

# 2. 데이터베이스 연결 확인

kubectl exec -it -n legacy-sales <oracle-pod-name> -- \

  sqlplus SYSTEM/satis@xepdb1 <<EOF

SELECT COUNT(*) FROM SATIS_USERS WHERE username='20010001';

EOF

  

# 3. 세션 설정 확인 (application.properties)

server.servlet.session.timeout=30m

server.servlet.session.cookie.http-only=true

```

  

**해결 방법:**

1. 직원번호(empNo)를 정확하게 입력했는지 확인 (예: 20010001)

2. 비밀번호가 `password123`인지 확인

3. 브라우저 쿠키를 삭제하고 다시 시도

  

---
```

---

## Chunk 21

**Size:** 654 characters

```
### 2. 데이터베이스 연결 실패

  

**증상:** 애플리케이션이 데이터베이스에 연결하지 못함

  

**확인 사항:**

```bash

# 1. Oracle Pod 상태 확인

kubectl get pods -n legacy-sales -l app=oracle-db

  

# 2. Oracle 로그 확인

kubectl logs -n legacy-sales -l app=oracle-db --tail=100

  

# 3. Service DNS 확인

kubectl run -it --rm debug --image=busybox --restart=Never -n legacy-sales -- \

  nslookup oracle-db

  

# 4. 포트 연결 테스트

kubectl run -it --rm debug --image=busybox --restart=Never -n legacy-sales -- \

  telnet oracle-db 1521

```

  

**해결 방법:**

1. Oracle Pod가 Running 상태인지 확인

2. Service가 올바르게 설정되어 있는지 확인

3. application.properties의 JDBC URL 확인

4. Oracle이 완전히 시작될 때까지 2-3분 대기

  

---
```

---

## Chunk 22

**Size:** 867 characters

```
### 3. Excel 다운로드가 되지 않을 때

  

**증상:** Excel 다운로드 버튼 클릭 시 오류 발생

  

**확인 사항:**

```bash

# 애플리케이션 로그 확인 (POI 관련 오류)

kubectl logs -n legacy-sales -l app=satis-app | grep -i "poi\|excel"

  

# 메모리 사용량 확인

kubectl top pods -n legacy-sales

```

  

**해결 방법:**

1. 검색 결과 데이터가 너무 많은 경우 필터링 조건 추가

2. 애플리케이션 Pod 메모리 부족 시 리소스 증설

3. Apache POI 라이브러리 버전 확인 (pom.xml)

  

---

  

### 4. 페이지 로딩이 느릴 때

  

**증상:** 페이지 로드 시간이 10초 이상 소요

  

**확인 사항:**

```bash

# 1. Pod 리소스 사용량 확인

kubectl top pods -n legacy-sales

  

# 2. 데이터베이스 쿼리 성능 확인

# Oracle에서 실행 계획 확인

EXPLAIN PLAN FOR SELECT * FROM INVENTORY WHERE region='수도권';

SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);

  

# 3. 네트워크 레이턴시 확인

curl -w "@curl-format.txt" -o /dev/null -s https://sales.4.230.72.248.nip.io

```

  

**해결 방법:**

1. 데이터베이스 인덱스 추가

2. 쿼리 최적화 (N+1 문제 확인)

3. 페이지 크기를 줄여서 조회 (size 파라미터 조정)

  

---
```

---

## Chunk 23

**Size:** 599 characters

```
### 5. Ingress 접속 실패 (502/503)

  

**증상:** 외부에서 HTTPS 접속 시 502 Bad Gateway 또는 503 Service Unavailable

  

**확인 사항:**

```bash

# 1. Ingress Controller 상태 확인

kubectl get pods -n ingress-nginx

  

# 2. Ingress 리소스 확인

kubectl describe ingress satis-ingress -n legacy-sales

  

# 3. 애플리케이션 Service 확인

kubectl get svc satis-app -n legacy-sales

  

# 4. TLS 인증서 확인

kubectl get certificate -n legacy-sales

```

  

**해결 방법:**

1. Ingress Controller Pod가 Running 상태인지 확인

2. Service의 Endpoint가 올바르게 설정되어 있는지 확인

3. TLS 인증서가 유효한지 확인 (Let's Encrypt 인증서는 90일 유효)

4. 애플리케이션 Pod가 정상 작동 중인지 확인

  

---
```

---

## Chunk 24

**Size:** 515 characters

```
### 6. 한글이 깨져서 표시될 때

  

**증상:** JSP 페이지에서 한글이 깨짐

  

**확인 사항:**

```bash

# application.properties 확인

cat src/main/resources/application.properties | grep encoding

```

  

**설정 확인:**

```properties

# application.properties

server.servlet.encoding.charset=UTF-8

server.servlet.encoding.force=true

spring.jpa.database-platform=org.hibernate.dialect.Oracle12cDialect

```

  

**해결 방법:**

1. JSP 파일 상단에 `<%@ page contentType="text/html; charset=UTF-8" %>` 추가

2. Oracle NLS_LANG 설정 확인

3. 애플리케이션 재시작

  

---
```

---

## Chunk 25

**Size:** 899 characters

```
## 📊 모니터링 및 로깅

  

### 애플리케이션 로그 확인

  

**실시간 로그:**

```bash

kubectl logs -n legacy-sales -l app=satis-app -f

```

  

**최근 100줄 로그:**

```bash

kubectl logs -n legacy-sales -l app=satis-app --tail=100

```

  

**에러 로그만 필터링:**

```bash

kubectl logs -n legacy-sales -l app=satis-app | grep -i "error\|exception"

```

  

### 데이터베이스 모니터링

  

**Oracle 세션 확인:**

```sql

-- 활성 세션 수

SELECT COUNT(*) FROM v$session WHERE status='ACTIVE';

  

-- 세션별 SQL 확인

SELECT s.username, s.status, q.sql_text

FROM v$session s, v$sql q

WHERE s.sql_id = q.sql_id(+)

AND s.username IS NOT NULL;

```

  

**테이블 스페이스 확인:**

```sql

SELECT tablespace_name, bytes/1024/1024 AS "Size(MB)",

       maxbytes/1024/1024 AS "MaxSize(MB)"

FROM dba_data_files;

```

  

### 리소스 모니터링

  

**Pod 리소스 사용량:**

```bash

kubectl top pods -n legacy-sales

```

  

**노드 리소스 사용량:**

```bash

kubectl top nodes

```

  

---
```

---

## Chunk 26

**Size:** 892 characters

```
## 📝 API 테스트

  

### Postman Collection

  

주요 API를 테스트할 수 있는 Postman Collection 예시:

  

**1. 로그인 테스트:**

```http

POST https://sales.4.230.72.248.nip.io/login

Content-Type: application/x-www-form-urlencoded

  

username=20010001&password=password123

```

  

**2. 대시보드 통계:**

```http

GET https://sales.4.230.72.248.nip.io/api/dashboard/stats?region=전국

```

  

**3. 재고 검색:**

```http

GET https://sales.4.230.72.248.nip.io/api/inventory/search?region=수도권&itemType=휘발유&page=0&size=10

```

  

**4. 송유관 주문 검색:**

```http

GET https://sales.4.230.72.248.nip.io/api/pipeline/search?status=Confirmed&page=0&size=10

```

  

---

  

## 🔐 보안 고려사항

  

### 세션 관리

- 세션 타임아웃: 30분

- HttpOnly 쿠키 사용

- CSRF 보호 활성화

  

### 비밀번호 정책

- 초기 비밀번호: `password123` (변경 권장)

- 비밀번호 변경 기능 (향후 구현 예정)

  

### 권한 체크

- PermissionInterceptor를 통한 메뉴별 권한 체크

- 역할 기반 접근 제어 (ADMIN, MANAGER, USER)

  

---
```

---

## Chunk 27

**Size:** 898 characters

```
## 📞 지원

  

문제가 발생하거나 질문이 있으시면:

1. 애플리케이션 및 데이터베이스 로그 확인

2. Kubernetes 리소스 상태 확인

3. 네트워크 연결 상태 확인

4. README.md 및 MIGRATION_PLAN.md 참고

  

---

  

## 📈 성능 최적화 팁

  

### 데이터베이스 인덱스

```sql

-- 재고 테이블 인덱스

CREATE INDEX idx_inventory_region ON INVENTORY(region);

CREATE INDEX idx_inventory_item_type ON INVENTORY(item_type);

CREATE INDEX idx_inventory_updated_at ON INVENTORY(updated_at);

  

-- 주문 테이블 인덱스

CREATE INDEX idx_pipeline_region ON PIPELINE_ORDER(region);

CREATE INDEX idx_pipeline_status ON PIPELINE_ORDER(status);

CREATE INDEX idx_pipeline_order_date ON PIPELINE_ORDER(order_date);

```

  

### JPA 쿼리 최적화

- Lazy Loading 설정 확인

- N+1 문제 방지 (Fetch Join 사용)

- 페이징 쿼리 최적화

  

### 캐싱 전략

- 대시보드 통계 데이터 캐싱 (향후 구현)

- 정적 리소스 브라우저 캐싱

- CDN 활용 (향후 검토)

  

---

  

**문서 버전:** 1.0

**최종 업데이트:** 2024년 1월

**네임스페이스:** legacy-sales

**프로덕션 URL:** https://sales.4.230.72.248.nip.io
```

---


## Summary Statistics

- **Total characters:** 18,513
- **Total chunks:** 27
- **Average chunk size:** 685 characters
- **Largest chunk:** 999 characters
- **Smallest chunk:** 202 characters
