SET last_ts = CUR_TS();
SET num_tokens = 1;
SET token_per_sec = 1;

--processing--

SET tokens = tokens + TIME_DIFF(CUR_TS(), last_ts)  * token_per_ms;
SET last_ts = CUR_TS();
SET limit = MIN(SELECT COUNT(*) FROM input, tokens);
SET tokens = tokens - limit;
CREATE TABLE output AS SELECT * FROM input LIMIT limit;


