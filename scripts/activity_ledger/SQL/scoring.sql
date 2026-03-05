CREATE TEMP TABLE scoring (
    Category         VARCHAR,
    SubCategory     VARCHAR,
    ActivityCode    VARCHAR PRIMARY KEY,
    Score            INTEGER,
    Description      VARCHAR
);

-- adm stands for Account Development & Maintenance
INSERT INTO scoring VALUES
    ('event', 'virtual',           'Z01',       5, 'virtual project meeting'),
    ('event', 'virtual',           'Z02',       5, 'virtual training'),
    ('event', 'in_person',         'X01',      10, 'in-person QBR'),
    ('event', 'in_person',         'X02',      10, 'in-person project meeting'),  
    ('event', 'in_person',         'X03',      10, 'in-person training'),
    ('event', 'in_person',         'X04',       7, 'in-person engagement'),
    ('adm',   'development',       'OPP',       4, 'created opportunity'),  
    ('adm',   'development',       'ACCT',      4, 'created account'),
    ('adm',   'development',       'QUOTE',     4, 'created CPQ quote'),
    ('adm',   'maintenance',       'CONTACT',   3, 'created contact'),
    ('adm',   'maintenance',       'LEAD',      3, 'lead converted'),
    ('adm',   'communication',     'CALL',      1, 'call logged')
;