DROP TABLE IF EXISTS tc_fish;

CREATE TABLE tc_fish (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc_fish (startNode,endNode,label)
SELECT * FROM fish
UNION
SELECT * FROM tc2plus_fish
UNION
SELECT * FROM tc3plus_fish
UNION
SELECT * FROM tc5plus_fish;