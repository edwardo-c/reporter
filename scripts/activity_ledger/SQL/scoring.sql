CREATE TEMP TABLE scoring (
    Type            VARCHAR,
    SubType         VARCHAR,
    Activity        VARCHAR,
    ActivityCode    VARCHAR NOT NULL PRIMARY KEY,
    Score           INTEGER,
    Description     VARCHAR
);

-- adm stands for Account Development & Maintenance
INSERT INTO scoring VALUES
    ('in_person', 'Event',                  'Shows',                     'Z01',    20, 'regional events, small shows, distributor shows, etc'),
    ('in_person', 'Conference',             'In-Person Training',        'Z02',    10, 'group of 2+ with content/presentation, ex: LnL, BnL'),
    ('in_person', 'Conference',             'In-Person Project Meeting', 'Z03',    10, 'site visit, presales call, project meeting'),
    ('in_person', 'Conference',             'In-Person QBR',             'Z04',    10, 'in person QBR meeting'),
    ('in_person', 'Client Engagement',      'Client Engagement',         'Z05',    10, 'Dinners, shows, golf events, co-sponsored happy hours, etc'),
    ('in_person', 'Client Engagement',      'Customer Meal',             'Z06',    10, 'Taking customer out for a meal'),
    ('virtual',   'virtual',                'Virtual Training',          'X01',     5, 'virtual training'),
    ('virtual',   'virtual',                'Virtual Project Meeting',   'X02',     5, 'virtual project meeting'), 
    ('ADM',       'Account Development',    'Created Account',           'ACCT',    4, 'created account'),
    ('ADM',       'Account Development',    'Created Opportunity',       'OPP',     4, 'created opportunity'),
    ('ADM',       'Account Development',    'Created Quote',             'QUOTE',   4, 'created CPQ quote'),
    ('ADM',       'Contact Maintenance',    'Created Contact',           'CONTACT', 3, 'created contact'),
    ('ADM',       'Contact Maintenance',    'Converted Leads',           'LEAD',    3, 'a lead you own had status updated to "Convterted"'),
    ('ADM',       'Outgoing Communication', 'Call Logged',               'CALL',    1, 'task entered with Subtype = Call'),
    ('ADM',       'Outgoing Communication', 'Outbound Email',            'EMAIL',   1, 'outbound email logged')
;
