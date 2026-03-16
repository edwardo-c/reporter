CREATE TEMP TABLE scoring (
    Type            VARCHAR NOT NULL,
    SubType         VARCHAR NOT NULL,
    Activity        VARCHAR NOT NULL,
    ActivityCode    VARCHAR NOT NULL PRIMARY KEY,
    Score           INTEGER NOT NULL,
    ScoreCap        INTEGER,
    Description     VARCHAR
);

-- adm stands for Account Development & Maintenance
INSERT INTO scoring VALUES
    ('in_person', 'Event',                  'Shows',                     'Z01',    20,  NULL, 'regional events, small shows, distributor shows, etc'),
    ('in_person', 'Conference',             'In-Person Training',        'Z02',    10,  NULL, 'group of 2+ with content/presentation, ex: LnL, BnL'),
    ('in_person', 'Conference',             'In-Person Project Meeting', 'Z03',    10,  NULL, 'site visit, presales call, project meeting'),
    ('in_person', 'Conference',             'In-Person QBR',             'Z04',    10,  NULL, 'in person QBR meeting'),
    ('in_person', 'Client Engagement',      'Client Engagement',         'Z05',    10,  NULL, 'Dinners, shows, golf events, co-sponsored happy hours, etc'),
    ('in_person', 'Client Engagement',      'Customer Meal',             'Z06',    10,  NULL, 'Taking customer out for a meal'),
    ('virtual',   'virtual',                'Virtual Training',          'X01',     5,  NULL, 'virtual training'),
    ('virtual',   'virtual',                'Virtual Project Meeting',   'X02',     5,  NULL, 'virtual project meeting'), 
    ('ADM',       'Account Development',    'Created Account',           'ACCT',    4,  NULL, 'created account'),
    ('ADM',       'Account Development',    'Created Opportunity',       'OPP',     4,  NULL, 'created opportunity'),
    ('ADM',       'Account Development',    'Created Quote',             'QUOTE',   4,  NULL, 'created CPQ quote'),
    ('ADM',       'Contact Maintenance',    'Created Contact',           'CONTACT', 3,  NULL, 'created contact'),
    ('ADM',       'Contact Maintenance',    'Converted Leads',           'LEAD',    3,  NULL, 'a lead you own had status updated to "Convterted"'),
    ('ADM',       'Outgoing Communication', 'Call Logged',               'CALL',    1,  NULL, 'task entered with Subtype = Call'),
    ('ADM',       'Outgoing Communication', 'Outbound Email',            'EMAIL',   1,  50,   'outbound email logged')
;
