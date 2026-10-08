-- 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS wellness
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE wellness;

-- ==========================================
-- 1. 사용자 및 인증 영역 (Users & Auth & Profiles)
-- ==========================================

-- 1. users (사용자 기본 정보) 테이블
CREATE TABLE users (
    user_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '사용자 고유 ID',
    login_id VARCHAR(50) NOT NULL UNIQUE COMMENT '로그인 ID',
    name VARCHAR(100) NOT NULL COMMENT '이름',
    email VARCHAR(255) NOT NULL UNIQUE COMMENT '이메일',
    phone_number VARCHAR(30) COMMENT '전화번호',
    gender ENUM('M', 'F') COMMENT '성별',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '계정 생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용자 기본 정보';

-- 2. user_auth (사용자 인증/로그인 정보) 테이블 
-- * 중복되는 login_id를 제거하고 users의 user_id를 1:1 PK/FK로 엄격히 관리
CREATE TABLE user_auth (
    user_id BIGINT PRIMARY KEY COMMENT '사용자 ID (외래 키이자 기본 키)',
    password_hash VARCHAR(255) NOT NULL COMMENT '비밀번호 해시',
    last_login_at DATETIME COMMENT '마지막 로그인 일시',
    failed_login_count INT DEFAULT 0 COMMENT '로그인 실패 횟수',
    locked_until DATETIME COMMENT '계정 잠금 해제 일시',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    CONSTRAINT fk_user_auth_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용자 인증 정보';

-- 3. profiles (프로필) 테이블
-- * user_id 타입을 BIGINT로 통일하여 users 테이블과 무결성 확보
CREATE TABLE profiles (
    profile_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '프로필 고유 ID',
    user_id BIGINT NOT NULL UNIQUE COMMENT '사용자 ID (1:1 관계)',
    nickname VARCHAR(50) COMMENT '닉네임',
    profile_image_url VARCHAR(255) COMMENT '프로필 이미지 URL',
    introduction TEXT COMMENT '자기소개',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '생성일시',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일시',
    CONSTRAINT fk_profiles_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용자 프로필';


-- ==========================================
-- 2. 사용자 건강 및 라이프스타일 영역
-- ==========================================

-- 4. health_metrics (건강 지표) 테이블
CREATE TABLE health_metrics (
    metric_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '건강 지표 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    height DECIMAL(5,2) COMMENT '키 (cm)',
    weight DECIMAL(5,2) COMMENT '체중 (kg)',
    measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '측정 일시',
    CONSTRAINT fk_health_metrics_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='건강 지표';

-- 5. constraints (건강 제약사항/알레르기 등) 테이블
CREATE TABLE constraints (
    constraint_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '제약사항 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    constraint_type VARCHAR(50) NOT NULL COMMENT '제약 유형 (예: 알레르기, 질환 등)',
    constraint_value VARCHAR(100) NOT NULL COMMENT '제약 값',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 일시',
    CONSTRAINT fk_constraints_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용자 제약사항';

-- 6. diet_plans (식단 및 추가 기능 계획) 테이블
CREATE TABLE diet_plans (
    plan_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '식단 플랜 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    plan_details JSON COMMENT '플랜 상세 정보 (루틴 백테스트, 건강 대체재 탐색, 동적 트렌드 알림, Vision AI 영양성분 역설계 등 추가 기능 데이터 포함)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 일시',
    CONSTRAINT fk_diet_plans_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='식단 플랜 및 AI 확장 기능';


-- ==========================================
-- 3. 시스템 로그 및 콘텐츠 영역
-- ==========================================

-- 7. activity_logs (활동 로그) 테이블
CREATE TABLE activity_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '로그 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    activity_category VARCHAR(50) COMMENT '활동 카테고리',
    activity_type VARCHAR(50) COMMENT '활동 유형',
    description TEXT COMMENT '활동 상세 설명',
    device_os VARCHAR(50) COMMENT '디바이스 운영체제',
    ip_address VARCHAR(45) COMMENT 'IP 주소',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '기록 일시',
    CONSTRAINT fk_activity_logs_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='사용자 활동 로그';

-- 8. news (뉴스/콘텐츠) 테이블
CREATE TABLE news (
    news_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '뉴스 고유 ID',
    category VARCHAR(50) COMMENT '카테고리',
    title VARCHAR(255) NOT NULL COMMENT '제목',
    content TEXT NOT NULL COMMENT '본문 내용',
    source_url VARCHAR(255) COMMENT '출처 URL',
    published_at TIMESTAMP NULL COMMENT '발행 일시',
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '수집 일시'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='건강/영양 뉴스 및 콘텐츠';


-- ==========================================
-- 4. 커뮤니케이션 (채팅) 영역
-- ==========================================

-- 9. chat_sessions (채팅 세션) 테이블
CREATE TABLE chat_sessions (
    session_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '세션 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID',
    title VARCHAR(100) COMMENT '채팅방 제목',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '생성 일시',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 일시',
    CONSTRAINT fk_chat_sessions_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='채팅 세션';

-- 10. chat_messages (채팅 메시지) 테이블
CREATE TABLE chat_messages (
    message_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '메시지 고유 ID',
    session_id BIGINT NOT NULL COMMENT '세션 ID',
    role VARCHAR(20) NOT NULL COMMENT '발화자 역할 (user, assistant 등)',
    content TEXT NOT NULL COMMENT '메시지 내용',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '전송 일시',
    deleted_at TIMESTAMP NULL COMMENT '삭제 일시 (Soft Delete)',
    CONSTRAINT fk_chat_messages_sessions FOREIGN KEY (session_id) REFERENCES chat_sessions(session_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='채팅 메시지';


-- ==========================================
-- 5. 음식, 음식점 및 주문 영역
-- ==========================================

-- 11. restaurants (음식점) 테이블
CREATE TABLE restaurants (
    restaurant_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '음식점 고유 ID',
    name VARCHAR(100) NOT NULL COMMENT '음식점 상호명',
    category VARCHAR(50) COMMENT '음식 카테고리',
    address VARCHAR(255) COMMENT '주소',
    latitude DECIMAL(10, 8) COMMENT '위도',
    longitude DECIMAL(11, 8) COMMENT '경도',
    phone_number VARCHAR(20) COMMENT '전화번호',
    price_range VARCHAR(20) COMMENT '가격대 정보'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='음식점 정보';

-- 12. foods (음식/식품) 테이블
CREATE TABLE foods (
    food_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '음식 고유 ID',
    food_name VARCHAR(100) NOT NULL COMMENT '음식 이름',
    category VARCHAR(50) COMMENT '식품 카테고리',
    spiciness INT COMMENT '매운맛 정도',
    sweetness INT COMMENT '단맛 정도',
    ingredients TEXT COMMENT '포함된 재료 목록'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='음식 및 영양 성분 정보';

-- 13. deliveries (배달 주문) 테이블
CREATE TABLE deliveries (
    delivery_id BIGINT AUTO_INCREMENT PRIMARY KEY COMMENT '배달 주문 고유 ID',
    user_id BIGINT NOT NULL COMMENT '사용자 ID (주문자)',
    address VARCHAR(255) NOT NULL COMMENT '배달 주소',
    phone_number VARCHAR(20) NOT NULL COMMENT '연락처',
    delivery_fee DECIMAL(10,2) DEFAULT 0.00 COMMENT '배달 요금',
    status VARCHAR(50) NOT NULL COMMENT '배달 상태',
    comments TEXT COMMENT '요청사항',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '주문 일시',
    CONSTRAINT fk_deliveries_users FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='배달 주문 정보';