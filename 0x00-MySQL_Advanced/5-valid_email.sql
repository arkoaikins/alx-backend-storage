--  script that creates a trigger that resets the attribute
-- valid_email only when the email has been changed.


CREATE TRIGGER email_reset AFTER UPDATE ON users
FOR EACH ROW
BEGIN
    IF OLD.email != NEW.email THEN
        UPDATE users SET NEW.valid_email = 0
    END IF;
END;
