mysql -u root
SET PASSWORD FOR root@localhost=PASSWORD('');
create database fx;
GRANT ALL PRIVILEGES ON *.* TO root@'192.168.%' IDENTIFIED BY '' WITH GRANT OPTION;