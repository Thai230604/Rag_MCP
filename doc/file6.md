# e-General Affairs System - 사용자 가이드

  

## 📋 목차

1. [시스템 개요](#시스템-개요)

2. [웹 애플리케이션 접근](#웹-애플리케이션-접근)

3. [데이터베이스 연결 정보](#데이터베이스-연결-정보)

4. [API 사용 가이드](#api-사용-가이드)

5. [테스트 계정](#테스트-계정)

6. [모니터링 도구](#모니터링-도구)

  

---

  

## 🎯 시스템 개요

  

**e-General Affairs**는 총무 업무를 지원하는 웹 애플리케이션입니다.

  

- **구분**: **[신규 구축]**

- **배포 환경**: Azure Kubernetes Service (AKS)

- **네임스페이스**: `legacy-general-affairs`

- **프론트엔드**: React (Vite)

- **백엔드**: Spring Boot 3.2.0 (Java 17)

- **데이터베이스**: MySQL 8.0

  

---

  

## 🌐 웹 애플리케이션 접근

  

### 메인 애플리케이션 **[신규 구축]**

- **URL**: https://ga.4.230.72.248.nip.io

- **프로토콜**: HTTPS (Let's Encrypt SSL 인증서)

- **접근 방법**: 웹 브라우저에서 직접 접속

  

### 주요 기능

1. **보안 관리**

   - ID 카드 신청/승인

   - 출장 관리

   - 방문자 관리

  

2. **업무 지원**

   - 비품 신청

   - IT 지원 요청

   - 차량 예약

  

3. **공간 관리**

   - 좌석 배정

   - 공용 오피스 예약

   - 출장자 숙소 예약

   - 사물함 관리

  

4. **컨시어지 서비스**

   - 골프장 예약

   - 기타 서비스 요청

  

5. **관리자 기능** (ADMIN 권한 필요)

   - 권한 관리

   - 활용도 평가 (로그인/메뉴 접근 이력)

  
[로그인 화면] 
![image.png](/.attachments/image-41240e69-48b1-4dbb-a53b-9b5e90f20cc7.png)

[홈 화면 - 사용자]
![image.png](/.attachments/image-d6583cde-4d98-4685-b87c-d4ab20eb56d8.png)

[출장자 숙소 예약 신청 - 사용자]
![image.png](/.attachments/image-395ac768-8d09-44bb-b6f2-981ecb7e5039.png)

[출장자 숙소 예약 현황 - 사용자]
![image.png](/.attachments/image-4e93d4f0-8b98-4db6-966f-164085d956e5.png)

[ID CARD 신청 - 사용자]
![image.png](/.attachments/image-5a3ab4f1-5512-4b3f-9aad-d27f6aa1d917.png)

[ID CARD 신청 현황 - 사용자]
![image.png](/.attachments/image-9cf0411d-0fe8-426c-b334-edcd45abded1.png)

[골프 예약 신청 - 임원]
![image.png](/.attachments/image-5ff971ef-724a-4c4c-9b37-df24ee350a8e.png)

[골프 예약 현황 - 임원]
![image.png](/.attachments/image-a0fea186-3038-43dd-a8bb-84259728ae6a.png)

[출장자 숙소 예약 승인 - 관리자]
![image.png](/.attachments/image-27229f54-60db-40ea-ada9-f51387dd2c27.png)

[ID CARD 신청 승인 - 관리자]
![image.png](/.attachments/image-8bdbb7b5-4005-45d9-8063-ddbb5990d77e.png)

[골프장 예약 승인 - 관리자]
![image.png](/.attachments/image-b9036fb4-ef6e-4856-a5cd-2292d61dffd4.png)

[활용도 평가 - 관리자] //실제 기능은 아직 아님.
![image.png](/.attachments/image-8aeeba44-05e7-4bb9-8322-f05c8da4cc77.png)

[권한 관리 - 관리자]
![image.png](/.attachments/image-693c21bc-9586-42f0-8ecd-26b575e1ffbf.png)

---

  

## 💾 데이터베이스 연결 정보

  

### PostgreSQL (legacy-postgres) - **[기존 레거시] HR 데이터베이스**

  

> [!NOTE]

> 기존 시스템에서 사용하던 HR 데이터 원본입니다. LoadBalancer를 통해 외부에서 접속 가능합니다.

  

| 항목 | 값 |
|------|-----|
| **External IP** | `4.230.64.191` |
| **Internal IP** | `10.0.237.251` |
| **Port** | `5432` |
| **Database** | `legacy_db` |
| **Admin 계정** | `legacy_admin` / `J8xz8ceak4kgt9c8eA` |

  

**연결 예시 (외부):**

```bash
psql -h 4.230.64.191 -p 5432 -U legacy_admin -d legacy_db
```

  

**연결 예시 (클러스터 내부):**

```bash
psql -h ga-db.legacy-general-affairs.svc.cluster.local -p 5432 -U legacy_admin -d legacy_db
```
  

---

  

### MySQL (egeneralaffairs-mysql) - **[신규 구축] 애플리케이션 DB**

  
> 이번 프로젝트에서 새로 구축한 DB입니다. 외부 접속 IP가 없으며, 클러스터 내부 또는 포트 포워딩을 통해서만 접속 가능합니다.

  

| 항목 | 값 |
|------|-----|
| **Internal IP** | `10.0.31.109` |
| **Port** | `3306` |
| **Database** | `egeneralaffairs` |
| **Root 계정** | `root` / `rootpassword` |

  

**연결 예시 (클러스터 내부):**

```bash

mysql -h egeneralaffairs-mysql.legacy-general-affairs.svc.cluster.local -P 3306 -u root -prootpassword egeneralaffairs

```

  

**연결 예시 (로컬에서 포트 포워딩):**

```bash
# 1. 포트 포워딩 설정

kubectl port-forward -n legacy-general-affairs svc/egeneralaffairs-mysql 3307:3306

  

# 2. 로컬에서 연결

mysql -h 127.0.0.1 -P 3307 -u root -prootpassword egeneralaffairs
```

  

**주요 테이블:**

- `users` - 사용자 정보 (148명)

- `accommodation` - 숙소 예약

- `golf_reservation` - 골프장 예약

- `idcard_request` - ID 카드 신청

- `login_log` - 로그인 이력

- `access_log` - 메뉴 접근 이력

- `task_status` - 작업 상태

  

---

  

## 🔌 API 사용 가이드

  

### Swagger UI 접근

- **URL**: https://ga.4.230.72.248.nip.io/swagger-ui/index.html

- **API Docs**: https://ga.4.230.72.248.nip.io/v3/api-docs

  

### 주요 API 엔드포인트


#### 1. 사용자 인증


**로그인**

```http

POST /api/users/login

Content-Type: application/json
  
{

  "userId": "emp006",

  "password": "1234"

}

```

  

**응답 예시:**

```json

{

  "success": true,

  "message": "로그인 성공",

  "user": {

    "userId": "emp006",

    "username": "20240006",

    "name": "김철수",

    "role": "MEMBER",

    "department": "개발팀"

  }

}

```

  

#### 2. 사용자 관리

  

**전체 사용자 조회**

```http

GET /api/users/list

```

  

**특정 사용자 조회**

```http

GET /api/users/{userId}

```

  

**사용자 통계**

```http

GET /api/users/stats

```

  

**응답 예시:**

```json

{

  "total": 148,

  "member": 120,

  "admin": 8,

  "executive": 20

}

```

  

#### 3. 권한 관리 (ADMIN 전용)

  

**사용자 권한 변경**

```http

PUT /api/users/{userId}/role

Content-Type: application/json

  

{

  "role": "ADMIN"

}

```

  

#### 4. 숙소 예약

  

**예약 신청**

```http

POST /api/accommodation/request

Content-Type: application/json

  

{

  "checkInDate": "2025-12-10",

  "checkOutDate": "2025-12-12",

  "purpose": "BUSINESS_TRIP",

  "requesterName": "김철수",

  "employeeId": "20240006",

  "phone": "010-1234-5678",

  "department": "개발팀"

}

```

  

**예약 현황 조회**

```http

GET /api/accommodation/status

```

  

**예약 승인 (ADMIN 전용)**

```http

PUT /api/accommodation/{id}/approve

```

  

#### 5. 골프장 예약

  

**예약 신청**

```http

POST /api/golf/request

Content-Type: application/json

  

{

  "reservationDate": "2025-12-15",

  "numberOfPeople": 4,

  "requesterName": "김철수",

  "phone": "010-1234-5678"

}

```

  

#### 6. ID 카드 신청

  

**신청**

```http

POST /api/idcard/request

Content-Type: application/json

  

{

  "employeeId": "20240006",

  "name": "김철수",

  "phone": "010-1234-5678",

  "department": "개발팀",

  "purpose": "출입증 발급"

}

```

  

**신청 현황 조회**

```http

GET /api/idcard/status

```

  

**승인 (ADMIN 전용)**

```http

PUT /api/idcard/{id}/approve

```

  

#### 7. 활용도 평가 (ADMIN 전용)

  

**로그인 이력 조회**

```http

GET /api/admin/login-history?startDate=2025-12-01&endDate=2025-12-31

```

  

**메뉴 접근 이력 조회**

```http

GET /api/admin/access-history?userId=emp006

```

  

### cURL 사용 예시

  

**로그인:**

```bash

curl -X POST https://ga.4.230.72.248.nip.io/api/users/login \

  -H "Content-Type: application/json" \

  -d '{"userId":"emp006","password":"1234"}'

```

  

**사용자 목록 조회:**

```bash

curl https://ga.4.230.72.248.nip.io/api/users/list

```

  

**숙소 예약 신청:**

```bash

curl -X POST https://ga.4.230.72.248.nip.io/api/accommodation/request \

  -H "Content-Type: application/json" \

  -d '{

    "checkInDate": "2025-12-10",

    "checkOutDate": "2025-12-12",

    "purpose": "BUSINESS_TRIP",

    "requesterName": "김철수",

    "employeeId": "20240006",

    "phone": "010-1234-5678",

    "department": "개발팀"

  }'

```

  

---

  

## 👥 테스트 계정

  

### 일반 사용자 (MEMBER)

  

| User ID | Username | Password | 이름 | 부서 |
|---------|----------|----------|------|------|
| emp006 | 20240006 | 1234 | 김철수 | 개발팀 |
| emp001 | 20010001 | 1234 | 이영희 | 인사팀 |
| emp050 | 20140050 | 1234 | 박민수 | 영업팀 |

  

### 관리자 (ADMIN)

  

| User ID | Username | Password | 이름 | 부서 |
|---------|----------|----------|------|------|
| emp122 | 20140122 | 1234 | 관리자 | 총무팀 |

  

### 임원 (EXECUTIVE)

  
| User ID | Username | Password | 이름 | 직급 |
|---------|----------|----------|------|------|
| emp100 | 20100100 | 1234 | 최대표 | 대표이사 |

  

> [!TIP]

> 모든 계정의 기본 비밀번호는 `1234`입니다.

  

---

  

## 📊 모니터링 도구 **[기존 레거시/공용]**

### 현재는 사용 안함!!!!  

### Grafana (성능 모니터링)

- **URL**: http://4.230.112.104:3000

- **용도**: 시스템 메트릭 및 대시보드

  

### Kibana (로그 분석)

- **URL**: http://20.249.153.149:5601

- **용도**: 애플리케이션 로그 검색 및 분석

  

### Prometheus (메트릭 수집)

- **URL**: http://20.249.160.173:9090

- **용도**: 메트릭 쿼리 및 알림

  

### Locust (부하 테스트)

- **URL**: http://4.230.112.161:8089

- **용도**: 성능 테스트 및 부하 테스트

  
---

  

## 🔧 개발자 정보

  

### 로컬 개발 환경

  

**프론트엔드 실행:**

```bash

cd mock-up/frontend

npm install

npm run dev

```

  

**백엔드 실행:**

```bash

cd mock-up/backend

./mvnw spring-boot:run

```

  

**Docker Compose로 전체 실행:**

```bash

cd mock-up

docker-compose up -d

```

  

### Kubernetes 배포

  

**백엔드 배포:**

```bash

# 이미지 빌드

docker build -t agenticaidevacr45141.azurecr.io/egeneralaffairs-backend:v1.2 ./backend

  

# ACR 로그인

az acr login --name agenticaidevacr45141

  

# 이미지 푸시

docker push agenticaidevacr45141.azurecr.io/egeneralaffairs-backend:v1.2

  

# 배포

kubectl apply -f kubernetes/backend-deployment.yaml

kubectl rollout status deployment/egeneralaffairs-backend -n legacy-general-affairs

```

  

**프론트엔드 배포:**

```bash

# 이미지 빌드

docker build -t agenticaidevacr45141.azurecr.io/egeneralaffairs-frontend:v1.0 ./frontend

  

# 이미지 푸시

docker push agenticaidevacr45141.azurecr.io/egeneralaffairs-frontend:v1.0

  

# 배포

kubectl apply -f kubernetes/frontend-deployment.yaml

```

  

### 유용한 kubectl 명령어

  

**Pod 상태 확인:**

```bash

kubectl get pods -n legacy-general-affairs

```

  

**로그 확인:**

```bash

# 백엔드 로그

kubectl logs -n legacy-general-affairs -l app=egeneralaffairs-backend --tail=100 -f

  

# 프론트엔드 로그

kubectl logs -n legacy-general-affairs -l app=egeneralaffairs-frontend --tail=100 -f

```

  

**서비스 확인:**

```bash

kubectl get svc -n legacy-general-affairs

```

  

**Ingress 확인:**

```bash

kubectl describe ingress ga-ingress -n legacy-general-affairs

```

  

---

  

## 🆘 문제 해결

  

### 로그인이 안 될 때

1. 브라우저 개발자 도구(F12)에서 Network 탭 확인

2. `/api/users/login` 요청의 응답 확인

3. 계정 정보가 올바른지 확인 (User ID: `emp006`, Password: `1234`)

  

### 데이터베이스 연결 실패

```bash

# MySQL Pod 상태 확인

kubectl get pods -n legacy-general-affairs -l app=egeneralaffairs-mysql

  

# MySQL 로그 확인

kubectl logs -n legacy-general-affairs -l app=egeneralaffairs-mysql

  

# 포트 포워딩으로 직접 연결 테스트

kubectl port-forward -n legacy-general-affairs svc/egeneralaffairs-mysql 3307:3306

mysql -h 127.0.0.1 -P 3307 -u root -prootpassword egeneralaffairs

```

  

### API 호출 실패 (403/404)

1. Swagger UI에서 API 스펙 확인: https://ga.4.230.72.248.nip.io/swagger-ui/index.html

2. 백엔드 로그 확인

3. Ingress 설정 확인

  

---
## 추가 기능
1. 📝 로그 파일 설정 (logback-spring.xml)
    로그 파일 위치: /var/log/egeneralaffairs/
  - application.log - 모든 로그 (일별 롤링, 30일 보관)
  - error.log - 에러 로그만 (일별 롤링, 90일 보관)
  - api.log - API 호출 로그 (일별 롤링, 30일 보관)

  2. 🧪 테스트 엔드포인트 (TestController)

  | 엔드포인트                        | 기능                                                    |
  |-----------------------------------|---------------------------------------------------------|
  | GET /api/test/logs                | 모든 로그 레벨 테스트 (TRACE, DEBUG, INFO, WARN, ERROR) |
  | GET /api/test/error/404           | 404 Not Found 에러                                      |
  | GET /api/test/error/500           | 500 Internal Server Error                               |
  | GET /api/test/error/null          | NullPointerException                                    |
  | POST /api/test/error/validation   | 400 Bad Request (validation)                            |
  | GET /api/test/error/random        | 랜덤 에러 발생                                          |
  | GET /api/test/slow                | 느린 응답 테스트 (3초 대기)                             |
  | GET /api/test/logs/bulk?count=100 | 대량 로그 생성                                          |

  3. 🔍 AuthController 로깅 개선

  - System.out.println → SLF4J Logger로 변경
  - 로그인 시도/성공/실패 상세 로그
  - IP 주소, Username, Role 정보 기록

  4. 🐳 Dockerfile 업데이트

  - 로그 디렉토리 자동 생성
  - Volume 마운트 지원

  사용 방법

  #로그 확인

  ## Pod에 접속
  kubectl exec -it <backend-pod> -n legacy-general-affairs -- sh

  ## 로그 파일 확인
  tail -f /var/log/egeneralaffairs/application.log
  tail -f /var/log/egeneralaffairs/error.log
  tail -f /var/log/egeneralaffairs/api.log

  ## 로그 테스트
  curl https://ga.4.230.72.248.nip.io/api/test/logs

  ## 404 에러
  curl https://ga.4.230.72.248.nip.io/api/test/error/404

  ## 500 에러
  curl https://ga.4.230.72.248.nip.io/api/test/error/500

  ## 랜덤 에러
  curl https://ga.4.230.72.248.nip.io/api/test/error/random

  ## 느린 응답 (3초)
  curl https://ga.4.230.72.248.nip.io/api/test/slow

  ## 대량 로그 생성
  curl https://ga.4.230.72.248.nip.io/api/test/logs/bulk?count=200

  #로그 파일 확인 (Pod 내부)

  ## Backend Pod 이름 확인
  kubectl get pods -n legacy-general-affairs

  ## Pod 접속
  kubectl exec -it egeneralaffairs-backend-xxx-xxx -n legacy-general-affairs -- sh

  ## 로그 파일 확인
  tail -f /var/log/egeneralaffairs/application.log
  tail -f /var/log/egeneralaffairs/error.log
  tail -f /var/log/egeneralaffairs/api.log

  또는 kubectl logs로 실시간 확인

  # 실시간 로그 보기
  kubectl logs -f -l app=egeneralaffairs-backend -n legacy-general-affairs
  
### 로깅·감사 추적(신규)

- **표준 로그 출력**: `kubectl logs`로 바로 확인 가능 (logback 컨트롤러 로거 INFO).
- **메뉴 접근**: `AccessLogInterceptor`가 요청마다 DB `access_log` 저장 + `userId/menu/uri` INFO 로그.
- **업무 액션 로그**
  - 골프 `GET /api/golf/*`, 생성/승인/거절 시 `id`, `requesterId`, `status` 로그
  - 숙소 `GET /api/accommodation/*`, 생성/승인/거절 시 `id`, `requesterId`, `location`, `status`
  - ID카드 목록/상태별 조회, 생성/승인/거절/완료, 상세 시 `id`, `requesterId`, `approverId`, `status`
  - 마이페이지 정보/결재현황 조회 시 `userId`
  - 통계/대시보드 조회 시 호출 로그
  - 사용자 목록/단건 조회, 권한변경/정보수정, 통계 조회, 로그인 시도/성공/실패(INFO/WARN/ERROR)
- **로그 파일 경로**: `/var/log/egeneralaffairs/application.log` (일반), `error.log` (ERROR 이상), `api.log` (컨트롤러). Docker Compose 사용 시 `backend/logs:/var/log/egeneralaffairs` 마운트하면 호스트에서 바로 확인.


## 📝 변경 이력

  
  ### v1.3 (2025-12-11)
  - ✅ **Azure DevOps CI/CD 파이프라인 구축**
    - Maven 빌드 자동화 (Java 17)
    - npm 빌드 자동화 (React + Vite)
    - Docker 이미지 빌드 및 ACR 푸시
    - AKS 자동 배포 (main 브랜치)
    - MySQL Recreate 전략 적용 (볼륨 충돌 방지)
  - ✅ **종합 로깅 시스템 추가**
    - Logback 설정 (일별 롤링 로그)
    - 파일 기반 로그: application.log, error.log, api.log
    - 로그 디렉토리: /var/log/egeneralaffairs/
    - AuthController SLF4J 로거 적용
  - ✅ **테스트 엔드포인트 추가**
    - GET /api/test/logs - 로그 레벨 테스트
    - GET /api/test/error/404 - 404 에러 테스트
    - GET /api/test/error/500 - 500 에러 테스트
    - GET /api/test/error/null - NullPointerException 테스트
    - POST /api/test/error/validation - Validation 에러 테스트
    - GET /api/test/error/random - 랜덤 에러 생성
    - GET /api/test/slow - 느린 응답 테스트 (3초)
    - GET /api/test/logs/bulk - 대량 로그 생성
  - ✅ **파이프라인 최적화**
    - Maven@4 사용 (deprecation 해결)
    - 테스트 결과 발행 개선
    - Kubernetes replicas 1로 조정

  ### v1.2 (2025-12-02)
  - ✅ CORS 설정 개선 (allowedOriginPatterns 사용)
  - ✅ OPTIONS 메서드 명시적 허용
  - ✅ Ingress rewrite-target 제거 (경로 보존)

  ### v1.1 (2025-12-02)
  - ✅ 프로덕션 도메인 CORS 허용 추가

  ### v1.0 (2025-12-01)
  - ✅ 초기 배포
  - ✅ MySQL 데이터 마이그레이션 (148 users)
  - ✅ HTTPS 인증서 적용

  

---

  

## 📞 지원

  

문제가 발생하거나 질문이 있으시면:

1. Swagger UI에서 API 문서 확인

2. 백엔드/프론트엔드 로그 확인

3. Kubernetes 리소스 상태 확인