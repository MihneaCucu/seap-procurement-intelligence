-- Reference schema for a local SQLite prototype; exact decimals use TEXT.
-- Required on every SQLite connection, before inserting rows.
PRAGMA foreign_keys = ON;

CREATE TABLE source_resources (
    source_resource_id TEXT PRIMARY KEY NOT NULL,
    package_id TEXT NOT NULL,
    source_file TEXT NOT NULL,
    source_url TEXT NOT NULL,
    license_title TEXT NOT NULL,
    source_year INTEGER NOT NULL,
    source_period TEXT NOT NULL CHECK (source_period IN ('annual','s1','s2','t1','t2','t3','t4'))
);

-- One organization may buy in one transaction and supply in another.
-- Names alone are not sufficient for resolving identity across exports.
CREATE TABLE organizations (
    organization_id TEXT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    identifier TEXT,
    identifier_country TEXT,
    legal_form TEXT,
    county TEXT,
    identity_status TEXT NOT NULL DEFAULT 'unresolved'
        CHECK (identity_status IN ('unresolved','verified'))
);

CREATE TABLE cpv_categories (
    cpv_code TEXT NOT NULL,
    scheme_version TEXT NOT NULL DEFAULT 'unknown',
    canonical_label TEXT,
    PRIMARY KEY (cpv_code, scheme_version)
);

-- One source row, not necessarily one unique economic purchase.
CREATE TABLE procurement_records (
    record_id TEXT PRIMARY KEY NOT NULL,
    source_resource_id TEXT NOT NULL REFERENCES source_resources(source_resource_id),
    source_sheet TEXT,
    source_row_number INTEGER CHECK (source_row_number > 0),
    authority_id TEXT REFERENCES organizations(organization_id),
    authority_name_source TEXT,
    record_type TEXT NOT NULL CHECK (record_type IN
        ('direct_purchase','published_contract','subsequent_contract')),
    procurement_reference TEXT,
    published_at_source TEXT,
    contract_or_completion_date_source TEXT,
    title TEXT,
    cpv_code TEXT,
    cpv_scheme_version TEXT,
    cpv_label_source TEXT,
    contract_type TEXT,
    procedure_type TEXT,
    number_of_offers INTEGER CHECK (number_of_offers >= 0),
    amount_source TEXT,
    currency_source TEXT,
    -- Filled after validated numeric/date normalization.
    amount_decimal TEXT,
    published_at TEXT,
    contract_date TEXT,
    award_date TEXT,
    completion_date TEXT,
    FOREIGN KEY (cpv_code, cpv_scheme_version)
        REFERENCES cpv_categories(cpv_code, scheme_version),
    CHECK ((cpv_code IS NULL) = (cpv_scheme_version IS NULL)),
    UNIQUE (source_resource_id, source_sheet, source_row_number)
);

-- Only suppliers explicitly identified as winners in evidence.
CREATE TABLE procurement_suppliers (
    record_id TEXT NOT NULL REFERENCES procurement_records(record_id),
    supplier_id TEXT NOT NULL REFERENCES organizations(organization_id),
    supplier_name_source TEXT,
    PRIMARY KEY (record_id, supplier_id)
);

-- Create items only when the source really identifies purchased items.
-- The total amount on procurement_records is not repeated as an item price.
CREATE TABLE procurement_items (
    item_id TEXT PRIMARY KEY NOT NULL,
    record_id TEXT NOT NULL REFERENCES procurement_records(record_id),
    description TEXT,
    quantity TEXT,
    quantity_unit TEXT,
    unit_price TEXT,
    currency TEXT,
    evidence_reference TEXT NOT NULL
);

-- Official BNR quotes: rate_value RON for unit_multiplier units of currency.
CREATE TABLE bnr_exchange_rates (
    rate_id TEXT PRIMARY KEY NOT NULL,
    currency TEXT NOT NULL CHECK (currency <> 'RON'),
    rate_date TEXT NOT NULL,
    rate_value TEXT NOT NULL,
    unit_multiplier INTEGER NOT NULL DEFAULT 1 CHECK (unit_multiplier > 0),
    source_url TEXT NOT NULL,
    UNIQUE (currency, rate_date)
);

CREATE TABLE currency_conversions (
    conversion_id TEXT PRIMARY KEY NOT NULL,
    record_id TEXT NOT NULL REFERENCES procurement_records(record_id),
    transaction_date TEXT NOT NULL,
    date_basis TEXT NOT NULL CHECK (date_basis IN
        ('contract_date','award_date','completion_date')),
    base_currency TEXT NOT NULL,
    base_amount TEXT NOT NULL,
    target_currency TEXT NOT NULL,
    converted_amount TEXT NOT NULL,
    base_rate_id TEXT REFERENCES bnr_exchange_rates(rate_id),
    target_rate_id TEXT REFERENCES bnr_exchange_rates(rate_id),
    conversion_method TEXT NOT NULL DEFAULT 'bnr_date_or_previous_v1',
    CHECK ((base_currency = 'RON' AND base_rate_id IS NULL)
        OR (base_currency <> 'RON' AND base_rate_id IS NOT NULL)),
    CHECK ((target_currency = 'RON' AND target_rate_id IS NULL)
        OR (target_currency <> 'RON' AND target_rate_id IS NOT NULL)),
    UNIQUE (record_id, target_currency, conversion_method)
);

CREATE INDEX procurement_authority_idx ON procurement_records(authority_id);
CREATE INDEX procurement_cpv_idx ON procurement_records(cpv_code, cpv_scheme_version);
CREATE INDEX supplier_organization_idx ON procurement_suppliers(supplier_id);
