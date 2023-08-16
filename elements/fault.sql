--init@none--
/*
Initialization:
*/
SET probability = 0.9;

--processing--

/*
  Processing Logic: Drop requests based on the preset probability
*/
INSERT INTO output (src, dst, type, payload)
SELECT * FROM input WHERE random() < probability;
