-- Creates a view need_meeting that lists all students with a score 
-- strictly below 80 and who either have no recorded last meeting 
-- or had their last meeting more than 1 month ago

DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
    SELECT name
        FROM students
        WHERE score < 80 AND
            (
                last_meeting IS NULL
                OR last_meeting < SUBDATE(CURRENT_DATE(), INTERVAL 1 MONTH)
            );
