DROP TABLE IF EXISTS g;

CREATE TABLE g (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO g select * from fish;

INSERT INTO g 
SELECT g1.startNode, g2.endNode, '2.3'
FROM g as g1, g as g2
WHERE g1.label = '2' AND g2.label = '3'
AND g1.endNode = g2.startNode;

INSERT INTO g 
SELECT g1.startNode, g2.endNode, '2.3.5'
FROM g as g1, g as g2
WHERE g1.label = '2.3' AND g2.label = '5'
AND g1.endNode = g2.startNode;

SELECT g.startNode, g.endNode, g.label
FROM g
WHERE g.label = '2.3.5';
