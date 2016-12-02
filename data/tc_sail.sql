DROP TABLE IF EXISTS tc_sail;

CREATE TABLE tc_sail (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc_sail (startNode,endNode,label)
SELECT * FROM sail
UNION
SELECT * FROM tc2plus_sail
UNION
SELECT * FROM tc3plus_sail
UNION
SELECT * FROM tc5plus_sail;