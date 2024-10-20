-- Lists all bands with Glam rock as their primary style, ranked by their lifespan
-- Calculates lifespan as the difference between the split year (or current year if not split) and the formation year
SELECT band_name, (IFNULL(split, '2020') - formed) AS lifespan
    FROM metal_bands
    WHERE FIND_IN_SET('Glam rock', IFNULL(style, "")) > 0
    ORDER BY lifespan DESC;
