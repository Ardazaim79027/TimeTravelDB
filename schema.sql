USE timetravel;

DROP TRIGGER IF EXISTS after_user_insert;

CREATE TRIGGER after_user_insert
AFTER INSERT ON users
FOR EACH ROW
INSERT INTO users_history
(
user_id,
operation_type,
new_name,
new_email
)
VALUES
(
NEW.id,
'INSERT',
NEW.name,
NEW.email
);

DROP TRIGGER IF EXISTS after_user_update;

CREATE TRIGGER after_user_update
AFTER UPDATE ON users
FOR EACH ROW
INSERT INTO users_history
(
user_id,
operation_type,
old_name,
new_name,
old_email,
new_email
)
VALUES
(
OLD.id,
'UPDATE',
OLD.name,
NEW.name,
OLD.email,
NEW.email
);
