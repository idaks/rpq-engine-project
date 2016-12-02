DROP TABLE IF EXISTS tc2plus_sail;

CREATE TABLE tc2plus_sail (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc2plus_sail (startNode,endNode,label)
WITH RECURSIVE tc2sail(X,Y,L) AS (
            SELECT sail.startNode as X, sail.endNode as Y, '2+' as L
            FROM sail
            WHERE label = 2
        UNION
            SELECT tc2sail.X as X, sail.endNode as Y, '2+' as L
            FROM tc2sail, sail
            WHERE sail.label = 2
            AND tc2sail.Y = sail.startNode
)
SELECT * FROM tc2sail;




DROP TABLE IF EXISTS tc3plus_sail;

CREATE TABLE tc3plus_sail (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc3plus_sail (startNode,endNode,label)
WITH RECURSIVE tc3sail(X,Y,L) AS (
            SELECT sail.startNode as X, sail.endNode as Y, '3+' as L
            FROM sail
            WHERE label = 3
        UNION
            SELECT tc3sail.X as X, sail.endNode as Y, '3+' as L
            FROM tc3sail, sail
            WHERE sail.label = 3
            AND tc3sail.Y = sail.startNode
)
SELECT * FROM tc3sail;




DROP TABLE IF EXISTS tc5plus_sail;

CREATE TABLE tc5plus_sail (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc5plus_sail (startNode,endNode,label)
WITH RECURSIVE tc5sail(X,Y,L) AS (
            SELECT sail.startNode as X, sail.endNode as Y, '5+' as L
            FROM sail
            WHERE label = 5
        UNION
            SELECT tc5sail.X as X, sail.endNode as Y, '5+' as L
            FROM tc5sail, sail
            WHERE sail.label = 5
            AND tc5sail.Y = sail.startNode
)
SELECT * FROM tc5sail;




DROP TABLE IF EXISTS tc2plus_fish;

CREATE TABLE tc2plus_fish (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc2plus_fish (startNode,endNode,label)
WITH RECURSIVE tc2fish(X,Y,L) AS (
            SELECT fish.startNode as X, fish.endNode as Y, '2+' as L
            FROM fish
            WHERE label = 2
        UNION
            SELECT tc2fish.X as X, fish.endNode as Y, '2+' as L
            FROM tc2fish, fish
            WHERE fish.label = 2
            AND tc2fish.Y = fish.startNode
)
SELECT * FROM tc2fish;




DROP TABLE IF EXISTS tc3plus_fish;

CREATE TABLE tc3plus_fish (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc3plus_fish (startNode,endNode,label)
WITH RECURSIVE tc3fish(X,Y,L) AS (
            SELECT fish.startNode as X, fish.endNode as Y, '3+' as L
            FROM fish
            WHERE label = 3
        UNION
            SELECT tc3fish.X as X, fish.endNode as Y, '3+' as L
            FROM tc3fish, fish
            WHERE fish.label = 3
            AND tc3fish.Y = fish.startNode
)
SELECT * FROM tc3fish;




DROP TABLE IF EXISTS tc5plus_fish;

CREATE TABLE tc5plus_fish (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc5plus_fish (startNode,endNode,label)
WITH RECURSIVE tc5fish(X,Y,L) AS (
            SELECT fish.startNode as X, fish.endNode as Y, '5+' as L
            FROM fish
            WHERE label = 5
        UNION
            SELECT tc5fish.X as X, fish.endNode as Y, '5+' as L
            FROM tc5fish, fish
            WHERE fish.label = 5
            AND tc5fish.Y = fish.startNode
)
SELECT * FROM tc5fish;
