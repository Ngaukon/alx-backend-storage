-- Creates a stored procedure ComputeAverageWeightedScoreForUsers to compute 
-- and update the average weighted score for all students based on their corrections 
-- and the weights of the associated projects

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    -- Temporarily add columns for total weighted score and total weight to the users table
    ALTER TABLE users ADD total_weighted_score INT NOT NULL;
    ALTER TABLE users ADD total_weight INT NOT NULL;

    -- Update the total weighted score for each user by summing the product of correction scores and project weights
    UPDATE users
        SET total_weighted_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    -- Update the total weight for each user by summing the weights of all associated projects
    UPDATE users
        SET total_weight = (
            SELECT SUM(projects.weight)
            FROM corrections
                INNER JOIN projects
                    ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    -- Calculate and update the average score for each user, setting it to 0 if total weight is 0
    UPDATE users
        SET users.average_score = IF(users.total_weight = 0, 0, users.total_weighted_score / users.total_weight);

    -- Remove the temporary columns from the users table
    ALTER TABLE users
        DROP COLUMN total_weighted_score;
    ALTER TABLE users
        DROP COLUMN total_weight;
END $$
DELIMITER ;
