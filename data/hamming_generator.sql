DROP TABLE IF EXISTS sail;

CREATE TABLE sail (
"startNode" INTEGER,
"endNode" INTEGER,
"label" INTEGER
);

INSERT INTO sail (startNode,endNode,label)
WITH RECURSIVE 
    tc2(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc2.Y, 2*tc2.Y, 2
            FROM tc2 WHERE 2*tc2.Y <= 1000
    ),
    tc3(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc3.Y, 3*tc3.Y, 3
            FROM tc3 WHERE 3*tc3.Y <= 1000
    ),
    tc5(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc5.Y, 5*tc5.Y, 5
            FROM tc5 WHERE 5*tc5.Y <= 1000
    ),
    tc23(X,Y,L) AS (
        SELECT * FROM tc2
        UNION ALL
        SELECT tc23.Y, 3*tc23.Y, 3
        FROM tc23 WHERE 3*tc23.Y <= 1000
        ),
    tc235(X,Y,L) AS (
        SELECT * FROM tc23
        UNION ALL
        SELECT tc235.Y, 5*tc235.Y, 5
        FROM tc235 WHERE 5*tc235.Y <= 1000
    )
SELECT * FROM tc235 WHERE L != 1 ORDER BY Y, L ;

DROP TABLE IF EXISTS fish;

CREATE TABLE fish (
	"startNode" INTEGER,
    "endNode" INTEGER,
    "label" INTEGER
);

INSERT INTO fish (startNode,endNode,label)
WITH RECURSIVE 
        tc2(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc2.Y, 2*tc2.Y, 2
            FROM tc2 WHERE 2*tc2.Y <= 1000
),
        tc3(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc3.Y, 3*tc3.Y, 3
            FROM tc3 WHERE 2*tc3.Y <= 1000
),
        tc5(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc5.Y, 5*tc5.Y, 5
            FROM tc5 WHERE 5*tc5.Y <= 1000
),
        tc23(X,Y,L) AS (
            SELECT * FROM tc2
            UNION
            SELECT tc23.Y, 3*tc23.Y, 3
            FROM tc23 WHERE 3*tc23.Y <= 1000
),
        tc32(X,Y,L) AS (
            SELECT * FROM tc3
            UNION
            SELECT tc32.Y, 2*tc32.Y, 2
            FROM tc32 WHERE 2*tc32.Y <= 1000
),
        tc25(X,Y,L) AS (
            SELECT * FROM tc2
            UNION
            SELECT tc25.Y, 5*tc25.Y, 5
            FROM tc25 WHERE 5*tc25.Y <= 1000
),
        tc52(X,Y,L) AS (
            SELECT * FROM tc5
            UNION
            SELECT tc52.Y, 2*tc52.Y, 2
            FROM tc52 WHERE 2*tc52.Y <= 1000
),
        tc35(X,Y,L) AS (
            SELECT * FROM tc3
            UNION
            SELECT tc35.Y, 5*tc35.Y, 5
            FROM tc35 WHERE 5*tc35.Y <= 1000
),
        tc53(X,Y,L) AS (
            SELECT * FROM tc5
            UNION
            SELECT tc53.Y, 3*tc53.Y, 3
            FROM tc53 WHERE 3*tc53.Y <= 1000
),
        tc235(X,Y,L) AS (
            SELECT * FROM tc23
            UNION
            SELECT tc235.Y, 5*tc235.Y, 5
            FROM tc235 WHERE 5*tc235.Y <= 1000
),
        tc352(X,Y,L) AS (
            SELECT * FROM tc35
            UNION
            SELECT tc352.Y, 2*tc352.Y, 2
            FROM tc352 WHERE 2*tc352.Y <= 1000
),
        tc253(X,Y,L) AS (
            SELECT * FROM tc25
            UNION
            SELECT tc253.Y, 3*tc253.Y, 3
            FROM tc253 WHERE 3*tc253.Y <= 1000
),
        star2_or_star3_or_star5(X) AS (
            SELECT Y FROM tc2 UNION 
            SELECT Y FROM tc3 UNION 
            SELECT Y FROM tc5),
        ans(X, Y, L) AS (
            SELECT * FROM tc2 UNION
            SELECT * FROM tc3 UNION
            SELECT * FROM tc5 
            UNION
            SELECT * FROM tc23 UNION
            SELECT * FROM tc25 
            UNION
            SELECT * FROM tc32 UNION
            SELECT * FROM tc35 
            UNION
            SELECT * FROM tc52 UNION
            SELECT * FROM tc53 
            UNION
            SELECT * FROM tc235 UNION
            SELECT * FROM tc253 UNION
            SELECT * FROM tc352
            )
SELECT * FROM ans  WHERE L != 1 ORDER BY Y, L ;

.mode csv
.output fish.csv
SELECT * FROM fish;
.output sail.csv
SELECT * FROM sail;
.output stdout
