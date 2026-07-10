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
    ('ADM',       'Outgoing Communication', 'Outbound Email',            'EMAIL',   1,  50,   'outbound email logged'),
    ('SO',        'System Development',     '1 hour System Development', 'SD1',     5,  NULL, 'System Development for 1 hour ex: Collaboration with IT to imporve existing systems'),
    ('SO',        'System Development',     '2 hour System Development', 'SD2',     10, NULL, 'System Development for 2 hours ex: Collaboration with IT to imporve existing systems'),
    ('SO',        'System Development',     '3 hour System Development', 'SD3',     15, NULL, 'System Development for 3 hours ex: Collaboration with IT to imporve existing systems'),
    ('SO',        'Code Development',       '1 hour Code Development',   'CD1',     5,  NULL, 'Code Development for 1 hour'),
    ('SO',        'Code Development',       '2 hour Code Development',   'CD2',     10, NULL, 'Code Development for 2 hours'),
    ('SO',        'Code Development',       '3 hour Code Development',   'CD3',     15, NULL, 'Code Development for 3 hours'),
    ('SO',        'Price Management',       '1 hour Price Management',   'PM1',     5,  NULL, 'Price Management for 1 hour - price lists/agreements/etc'),
    ('SO',        'Price Management',       '2 hour Price Management',   'PM2',     10, NULL, 'Price Management for 2 hour - price lists/agreements/etc'),
    ('SO',        'Price Management',       '3 hour Price Management',   'PM3',     15, NULL, 'Price Management for 3 hour - price lists/agreements/etc'),
    ('SO',        'Team Training',          'Team Training',             'TT1',     10, NULL, 'New hire, salesforce training, acumatica training, etc'),
    ('SO',        'Reporting',              '1 hour Reporting',          'R01',     5,  NULL, 'Ad-hoc and scheduled (EOM, POS) report generation or walk-thru for 1 hour'),
    ('SO',        'Reporting',              '2 hour Reporting',          'R02',     10, NULL, 'Ad-hoc and scheduled (EOM, POS) report generation or walk-thru for 2 hour'),
    ('SO',        'Reporting',              '3 hour Reporting',          'R03',     15, NULL, 'Ad-hoc and scheduled (EOM, POS) report generation or walk-thru for 3 hour'),
    ('SO',        'MAP Enforcement',        'URL Scan',                  'ME1',     10, NULL, 'Search reseller website for all MAP skus and sent to Wayvia'),
    ('SO',        'MAP Enforcement',        'Email Enforcement',         'ME2',     5, NULL,  'Contacted approximatly 3-5 resellers about MAP violations')
;

-- Program Funding - PF3