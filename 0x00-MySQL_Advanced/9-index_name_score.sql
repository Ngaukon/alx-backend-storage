-- Creates an index idx_name_first_score on the names table, indexing the first letter of the name and the score column
CREATE INDEX idx_name_first_score ON names(name(1), score);
