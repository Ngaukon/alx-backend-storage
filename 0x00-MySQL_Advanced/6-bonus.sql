-- Creates a stored procedure AddBonus to add a new correction (score) 
-- for a student based on the project, inserting the project if it doesn't exist

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_id INT DEFAULT 0;

    -- Check if the project exists by counting the entries
    SELECT COUNT(id)
        INTO project_count
        FROM projects
        WHERE name = project_name;
        
    -- Insert the project if it doesn't exist
    IF project_count = 0 THEN
        INSERT INTO projects(name)
            VALUES(project_name);
    END IF;

    -- Retrieve the project ID
    SELECT id
        INTO project_id
        FROM projects
        WHERE name = project_name;
        
    -- Add the correction with the project ID and score
    INSERT INTO corrections(user_id, project_id, score)
        VALUES (user_id, project_id, score);
END $$
DELIMITER ;
