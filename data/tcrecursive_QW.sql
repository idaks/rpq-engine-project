DROP TABLE IF EXISTS tc2star;

CREATE TABLE tc2star (
	"startNode" INTEGER,
    "endNode" INTEGER,
    "label" TEXT
);

INSERT INTO tc2star (startNode,endNode,label)
WITH RECURSIVE tc2(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc2.Y, 2*tc2.Y, '2+'
            FROM tc2 WHERE 2*tc2.Y <= 1000
)
SELECT * FROM tc2;

DROP TABLE IF EXISTS tc3star;

CREATE TABLE tc3star (
	"startNode" INTEGER,
    "endNode" INTEGER,
    "label" TEXT
);

INSERT INTO tc3star (startNode,endNode,label)
WITH RECURSIVE tc3(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc3.Y, 3*tc3.Y, '3+'
            FROM tc3 WHERE 3*tc3.Y <= 1000
)
SELECT * FROM tc3;


DROP TABLE IF EXISTS tc5star;

CREATE TABLE tc5star (
	"startNode" INTEGER,
    "endNode" INTEGER,
    "label" TEXT
);

INSERT INTO tc5star (startNode,endNode,label)
WITH RECURSIVE tc5(X,Y,L) AS (
            VALUES(1,1,1)
        UNION
            SELECT tc5.Y, 5*tc5.Y, '5+'
            FROM tc5 WHERE 5*tc5.Y <= 1000
)
SELECT * FROM tc5;



DROP TABLE IF EXISTS tc23star;

CREATE TABLE tc23star (
    "startNode" INTEGER,
    "endNode" INTEGER,
    "label" TEXT
);

INSERT INTO tc23star (startNode,endNode,label)
    WITH RECURSIVE tc23(X,Y,L) AS (
        SELECT * FROM tc2star
        UNION ALL
        SELECT tc23.Y, 3*tc23.Y,
            CASE L
            WHEN '1' THEN
            '3+'
            ELSE
            '2+3+'
            END L
        FROM tc23 WHERE 3*tc23.Y <= 1000
)
SELECT * FROM tc23 ORDER BY Y;


DROP TABLE IF EXISTS tc235star;

CREATE TABLE tc235star (
    "startNode" INTEGER,
    "endNode" INTEGER,
    "label" TEXT
);

INSERT INTO tc235star (startNode,endNode,label)
    WITH RECURSIVE tc235(X,Y,L) AS (
    SELECT * FROM tc23star
    UNION ALL
    SELECT tc235.Y, 5*tc235.Y,
        CASE L
        WHEN '1' THEN
        '5+'
        WHEN '2+' THEN
        '2+5+'
        ELSE
        '2+3+5+'
        END L
    FROM tc235 WHERE 5*tc235.Y <= 1000
)
SELECT * FROM tc235 ORDER BY Y, L;

DROP TABLE IF EXISTS tc235star_fish;

CREATE TABLE tc235star_fish (
	"startNode" TEXT,
    "endNode" TEXT,
    "label" TEXT
);

INSERT INTO tc235star_fish (startNode,endNode,label)
WITH RECURSIVE 
        tc2(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc2.Y, 2*tc2.Y, '2'
            FROM tc2 WHERE 2*tc2.Y <= 1000
),
        tc3(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc3.Y, 3*tc3.Y, '3'
            FROM tc3 WHERE 2*tc3.Y <= 1000
),
        tc5(X,Y,L) AS (
            VALUES(1,1,1)
            UNION
            SELECT tc5.Y, 5*tc5.Y, '5'
            FROM tc5 WHERE 5*tc5.Y <= 1000
),
        tc23(X,Y,L) AS (
            SELECT * FROM tc2
            UNION
            SELECT tc23.Y, 3*tc23.Y, '3'
            FROM tc23 WHERE 3*tc23.Y <= 1000
),
        tc32(X,Y,L) AS (
            SELECT * FROM tc3
            UNION
            SELECT tc32.Y, 2*tc32.Y, '2'
            FROM tc32 WHERE 2*tc32.Y <= 1000
),
        tc25(X,Y,L) AS (
            SELECT * FROM tc2
            UNION
            SELECT tc25.Y, 5*tc25.Y, '5'
            FROM tc25 WHERE 5*tc25.Y <= 1000
),
        tc52(X,Y,L) AS (
            SELECT * FROM tc5
            UNION
            SELECT tc52.Y, 2*tc52.Y, '2'
            FROM tc52 WHERE 2*tc52.Y <= 1000
),
        tc35(X,Y,L) AS (
            SELECT * FROM tc3
            UNION
            SELECT tc35.Y, 5*tc35.Y, '5'
            FROM tc35 WHERE 5*tc35.Y <= 1000
),
        tc53(X,Y,L) AS (
            SELECT * FROM tc5
            UNION
            SELECT tc53.Y, 3*tc53.Y, '3'
            FROM tc53 WHERE 3*tc53.Y <= 1000
),
        tc235(X,Y,L) AS (
            SELECT * FROM tc23
            UNION
            SELECT tc235.Y, 5*tc235.Y, '5'
            FROM tc235 WHERE 5*tc235.Y <= 1000
),
        tc352(X,Y,L) AS (
            SELECT * FROM tc35
            UNION
            SELECT tc352.Y, 2*tc352.Y, '2'
            FROM tc352 WHERE 2*tc352.Y <= 1000
),
        tc253(X,Y,L) AS (
            SELECT * FROM tc25
            UNION
            SELECT tc253.Y, 3*tc253.Y, '3'
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
            /*
            UNION ALL
            SELECT X,
            CASE left
            WHEN 30 THEN 2*Y
            WHEN 15 THEN 3*Y
            WHEN 5 THEN 5*Y
            ELSE Y
            END Y,
            CASE left
            WHEN 30 THEN 2
            WHEN 15 THEN 3
            WHEN 5 THEN 5
            ELSE 1
            END L,
            CASE left
            WHEN 30 THEN 15 
            WHEN 15 THEN 5
            WHEN 5 THEN 1
            ELSE 1
            END
            FROM ans,star2_or_star3_or_star5
            */
            )
SELECT * FROM ans ORDER BY Y, L;

.mode csv
.output tc_fish_QW.csv
SELECT * FROM tc235star_fish;
.output tc_sail_QW.csv
SELECT * FROM tc235star;
.output stdout
