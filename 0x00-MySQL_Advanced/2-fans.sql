-- Ranks countries by the total number of fans of bands, ordered in descending order
SELECT origin, SUM(fans) AS nb_fans
    FROM metal_bands
    GROUP BY origin
    ORDER BY nb_fans DESC;
