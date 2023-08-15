--init@example.proto--
CREATE TABLE t1 (
  income INT,
  age INT,
  deg VARCHAR(5),
);

--processing--

INSERT INTO t1 SELECT * FROM input WHERE deg = "bs";

UPDATE t1 SET deg = "phd", age = age + 5; 

INSERT INTO output SELECT * FROM t1;

DELETE FROM t1;