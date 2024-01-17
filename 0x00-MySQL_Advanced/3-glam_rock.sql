-- Script that lists all bands with Glam rock
-- as their main style ranked by their logevity

SELECT band_name, (IFNULL(split, 2022) - formed) lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;
