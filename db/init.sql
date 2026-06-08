-- Personal finance data model
-- Historic ledger: transactions + categories
-- Aggregates: monthly_summaries + category_monthly_totals

CREATE TYPE transaction_type AS ENUM ('expense', 'income');

-- ---------------------------------------------------------------------------
-- categories
-- Expense and income labels used when registering movements via the bot.
-- ---------------------------------------------------------------------------
CREATE TABLE categories (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    type        transaction_type NOT NULL,
    description TEXT,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT categories_name_type_unique UNIQUE (name, type)
);

CREATE INDEX idx_categories_type ON categories (type) WHERE is_active = TRUE;

-- ---------------------------------------------------------------------------
-- transactions
-- Immutable historic record of every expense and income entry.
-- amount is always positive; type determines whether it is money in or out.
-- ---------------------------------------------------------------------------
CREATE TABLE transactions (
    id                 BIGSERIAL PRIMARY KEY,
    type               transaction_type NOT NULL,
    category_id        INTEGER NOT NULL REFERENCES categories (id),
    amount             NUMERIC(12, 2) NOT NULL CHECK (amount > 0),
    currency           CHAR(3) NOT NULL DEFAULT 'EUR',
    description        TEXT,
    transaction_date   DATE NOT NULL,
    recorded_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source             VARCHAR(50) NOT NULL DEFAULT 'telegram',
    external_reference VARCHAR(255),

    CONSTRAINT transactions_currency_uppercase CHECK (currency = UPPER(currency))
);

CREATE INDEX idx_transactions_transaction_date ON transactions (transaction_date);
CREATE INDEX idx_transactions_type_date ON transactions (type, transaction_date);
CREATE INDEX idx_transactions_category_id ON transactions (category_id);
CREATE INDEX idx_transactions_year_month ON transactions (
    EXTRACT(YEAR FROM transaction_date),
    EXTRACT(MONTH FROM transaction_date)
);

-- ---------------------------------------------------------------------------
-- monthly_summaries
-- Pre-computed monthly metrics for dashboards and trend monitoring.
-- Recompute when transactions for a month are inserted, updated, or deleted.
-- ---------------------------------------------------------------------------
CREATE TABLE monthly_summaries (
    id                        SERIAL PRIMARY KEY,
    year                      SMALLINT NOT NULL,
    month                     SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    currency                  CHAR(3) NOT NULL DEFAULT 'EUR',

    total_income              NUMERIC(14, 2) NOT NULL DEFAULT 0,
    total_expenses            NUMERIC(14, 2) NOT NULL DEFAULT 0,
    net_balance               NUMERIC(14, 2) NOT NULL DEFAULT 0,

    income_transaction_count  INTEGER NOT NULL DEFAULT 0,
    expense_transaction_count INTEGER NOT NULL DEFAULT 0,

    -- Average amount per individual transaction within the month
    avg_income                NUMERIC(12, 2),
    avg_expense               NUMERIC(12, 2),

    computed_at               TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT monthly_summaries_period_currency_unique UNIQUE (year, month, currency),
    CONSTRAINT monthly_summaries_currency_uppercase CHECK (currency = UPPER(currency))
);

CREATE INDEX idx_monthly_summaries_period ON monthly_summaries (year, month);

-- ---------------------------------------------------------------------------
-- category_monthly_totals
-- Per-category breakdown for monthly spending/income analysis.
-- ---------------------------------------------------------------------------
CREATE TABLE category_monthly_totals (
    year               SMALLINT NOT NULL,
    month              SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    category_id        INTEGER NOT NULL REFERENCES categories (id),
    currency           CHAR(3) NOT NULL DEFAULT 'EUR',

    total_amount       NUMERIC(14, 2) NOT NULL DEFAULT 0,
    transaction_count  INTEGER NOT NULL DEFAULT 0,
    computed_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (year, month, category_id, currency),
    CONSTRAINT category_monthly_totals_currency_uppercase CHECK (currency = UPPER(currency))
);

CREATE INDEX idx_category_monthly_totals_period ON category_monthly_totals (year, month);

-- ---------------------------------------------------------------------------
-- Default categories
-- ---------------------------------------------------------------------------
INSERT INTO categories (name, type, description) VALUES
    ('salary',       'income',  'Regular employment income'),
    ('freelance',    'income',  'Freelance or side income'),
    ('investments',  'income',  'Dividends, interest, capital gains'),
    ('other_income', 'income',  'Uncategorized income'),

    ('housing',      'expense', 'Rent, mortgage, utilities'),
    ('food',         'expense', 'Groceries and dining'),
    ('transport',    'expense', 'Public transit, fuel, rides'),
    ('health',       'expense', 'Medical and wellness'),
    ('entertainment','expense', 'Leisure and subscriptions'),
    ('shopping',     'expense', 'Clothing and general purchases'),
    ('other_expense','expense', 'Uncategorized expenses');
