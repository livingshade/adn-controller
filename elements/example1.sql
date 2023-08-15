--init@example.proto--
CREATE TABLE t1 (
  income INT,
  age INT,
  deg VARCHAR(5)
);

CREATE TABLE t2 (
  income INT,
  age INT,
  deg VARCHAR(5)
);

--processing--

INSERT INTO t1 SELECT * FROM input 
WHERE deg = 'bs';

INSERT INTO t2 SELECT * FROM t1 
WHERE income > 1000 AND age < 20; 

INSERT INTO output SELECT * FROM t1 
WHERE age < 25;

DELETE FROM t1;