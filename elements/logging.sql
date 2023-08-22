--init@hello.proto--
--hellorequest--
-- Logging

/*
Internal state:
    rpc_events: A table to store rpc events
*/
CREATE TABLE rpc_events_file (
  event_type VARCHAR(50),
  source VARCHAR(50),
  destination VARCHAR(50),
  content VARCHAR(50)
);

--processing--

/*
  Processing Logic:
  1. Insert an event for each RPC
  2. Forward all RPCs
*/
INSERT INTO rpc_events_file (event_type, source, destination, content)
SELECT meta_type, meta_src, meta_dst, name
FROM input;

INSERT INTO output
SELECT * FROM input;
