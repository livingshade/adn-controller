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

INSERT INTO t2 (income, age, deg) VALUES (100, 200, 'bs');

--processing--

INSERT INTO t1 SELECT * FROM input WHERE deg = 'bs';

INSERT INTO output SELECT * FROM t1; 

UPDATE t2 SET age = age + 1;

INSERT INTO output SELECT * FROM t2 WHERE age < 25;

DELETE FROM t1;
