CREATE DATABASE IF NOT EXISTS hongwai DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hongwai;

CREATE TABLE IF NOT EXISTS users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(64) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  nickname VARCHAR(64) DEFAULT '',
  status TINYINT NOT NULL DEFAULT 1 COMMENT '1=正常,0=禁用',
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  UNIQUE KEY uk_username (username)
);

CREATE TABLE IF NOT EXISTS persons (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  name VARCHAR(64) NOT NULL,
  gender VARCHAR(10) DEFAULT '男',
  age INT DEFAULT 0,
  phone1 VARCHAR(20) DEFAULT '',
  phone2 VARCHAR(20) DEFAULT '',
  phone3 VARCHAR(20) DEFAULT '',
  relative_phone VARCHAR(20) DEFAULT '',
  id_card VARCHAR(32) DEFAULT '',
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  INDEX idx_user_id (user_id),
  INDEX idx_name (name),
  INDEX idx_phone1 (phone1),
  CONSTRAINT fk_persons_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS system_settings (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  serial_no VARCHAR(64) DEFAULT '1009Z0YGVM28',
  device_model VARCHAR(64) DEFAULT 'IR-TD-206',
  version VARCHAR(32) DEFAULT 'v1.0.74',
  report_type VARCHAR(32) DEFAULT '无',
  expire_time VARCHAR(32) DEFAULT '无',
  report_total INT DEFAULT 0,
  report_xiyi INT DEFAULT 0,
  report_zhongyi INT DEFAULT 0,
  report_mianzhen INT DEFAULT 0,
  report_danxiang INT DEFAULT 0,
  image_save_path VARCHAR(255) DEFAULT 'qa/qa_thermal',
  reverse_portrait_image TINYINT DEFAULT 0,
  report_count_hint INT DEFAULT 20,
  report_day_hint INT DEFAULT 10,
  screen_capture_enable TINYINT DEFAULT 0,
  typec_camera_enable TINYINT DEFAULT 0,
  qr_code_url VARCHAR(255) DEFAULT '',
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  UNIQUE KEY uk_user_id (user_id),
  CONSTRAINT fk_settings_user FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE ON UPDATE CASCADE
);
