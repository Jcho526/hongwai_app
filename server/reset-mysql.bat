@echo off
REM 停止MySQL服务
net stop MySQL80

REM 启动MySQL时跳过权限验证
REM 找到MySQL的bin目录
for /f "tokens=*" %%a in ('where mysql') do (
    set MYSQL_BIN_DIR=%%~dpa
)

echo MySQL bin目录: %MYSQL_BIN_DIR%

REM 用--skip-grant-tables启动mysqld
start "MySQL" "%MYSQL_BIN_DIR%mysqld" --skip-grant-tables

REM 等待MySQL启动
timeout /t 3

REM 连接并重置密码
mysql -u root --skip-password < reset-password.sql

REM 重启MySQL正常模式
net stop MySQL80
net start MySQL80

echo 密码重置完成！
