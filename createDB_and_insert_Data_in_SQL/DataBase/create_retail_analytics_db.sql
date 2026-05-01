-- ============================================================
--  Retail Analytics Database — SQL Server Creation Script
--  Generated for: Nestle Retail Analytics Dataset
--  Compatible with: SQL Server 2016+
-- ============================================================

USE master;
GO

-- Drop and recreate database
IF EXISTS (SELECT name FROM sys.databases WHERE name = N'RetailAnalyticsDB')
BEGIN
    ALTER DATABASE RetailAnalyticsDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE RetailAnalyticsDB;
END
GO

CREATE DATABASE Store_Sales_DataSetDB
    COLLATE SQL_Latin1_General_CP1_CI_AS;
GO

USE Store_Sales_DataSetDB;
GO

-- ============================================================
--  REFERENCE / LOOKUP TABLES  (no foreign keys)
-- ============================================================

-- CATEGORY
CREATE TABLE CATEGORY (
    category_id   VARCHAR(10)  NOT NULL,
    category_name VARCHAR(50)  NOT NULL,
    CONSTRAINT PK_CATEGORY PRIMARY KEY (category_id)
);
GO

-- CHANNEL  (sales / fulfilment channel)
CREATE TABLE CHANNEL (
    channel_id   VARCHAR(10) NOT NULL,
    channel_name VARCHAR(30) NOT NULL,
    CONSTRAINT PK_CHANNEL PRIMARY KEY (channel_id)
);
GO

-- MARKETING_CHANNEL  (campaign / comms channel)
CREATE TABLE MARKETING_CHANNEL (
    channel_id   VARCHAR(10) NOT NULL,
    channel_name VARCHAR(30) NOT NULL,
    channel_type VARCHAR(20) NOT NULL,   -- Owned | Paid | Offline
    cost_tier    VARCHAR(20) NOT NULL,   -- Low | Medium | High | Very High
    CONSTRAINT PK_MARKETING_CHANNEL PRIMARY KEY (channel_id)
);
GO

-- STORE
CREATE TABLE STORE (
    store_id    VARCHAR(10) NOT NULL,
    store_city  VARCHAR(50) NOT NULL,
    store_state VARCHAR(50) NOT NULL,
    store_type  VARCHAR(30) NOT NULL,
    CONSTRAINT PK_STORE PRIMARY KEY (store_id)
);
GO

-- PROMOTION
CREATE TABLE PROMOTION (
    promo_id       VARCHAR(10)    NOT NULL,
    promo_type     VARCHAR(20)    NOT NULL,   -- PCT_OFF | BOGO | FIXED_OFF
    start_date     DATE           NOT NULL,
    end_date       DATE           NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL DEFAULT 0,
    CONSTRAINT PK_PROMOTION    PRIMARY KEY (promo_id),
    CONSTRAINT CK_PROMO_DATES  CHECK (end_date >= start_date)
);
GO

-- ============================================================
--  CORE ENTITY TABLES
-- ============================================================

-- CUSTOMER
CREATE TABLE CUSTOMER (
    customer_id VARCHAR(20) NOT NULL,
    signup_date DATE        NOT NULL,
    city        VARCHAR(50) NULL,
    state       VARCHAR(50) NULL,
    segment     VARCHAR(20) NULL,   -- Value | Mainstream | Premium
    status      VARCHAR(20) NOT NULL DEFAULT 'active',  -- active | churned
    CONSTRAINT PK_CUSTOMER PRIMARY KEY (customer_id)
);
GO

-- PRODUCT
CREATE TABLE PRODUCT (
    product_id  VARCHAR(10)  NOT NULL,
    category_id VARCHAR(10)  NOT NULL,
    brand       VARCHAR(50)  NOT NULL,
    sku_name    VARCHAR(200) NOT NULL,
    CONSTRAINT PK_PRODUCT         PRIMARY KEY (product_id),
    CONSTRAINT FK_PRODUCT_CATEGORY FOREIGN KEY (category_id)
        REFERENCES CATEGORY (category_id)
);
GO

-- ============================================================
--  TRANSACTIONAL TABLES
-- ============================================================

-- ORDER  (reserved word — use square brackets or alias)
CREATE TABLE [ORDER] (
    order_id     VARCHAR(20) NOT NULL,
    customer_id  VARCHAR(20) NOT NULL,
    order_date   DATE        NOT NULL,
    store_id     VARCHAR(10) NOT NULL,
    channel_id   VARCHAR(10) NOT NULL,
    payment_type VARCHAR(30) NULL,
    year         SMALLINT    NOT NULL,
    week         TINYINT     NOT NULL,
    CONSTRAINT PK_ORDER          PRIMARY KEY (order_id),
    CONSTRAINT FK_ORDER_CUSTOMER FOREIGN KEY (customer_id)
        REFERENCES CUSTOMER (customer_id),
    CONSTRAINT FK_ORDER_STORE    FOREIGN KEY (store_id)
        REFERENCES STORE (store_id),
    CONSTRAINT FK_ORDER_CHANNEL  FOREIGN KEY (channel_id)
        REFERENCES CHANNEL (channel_id),
    CONSTRAINT CK_ORDER_WEEK     CHECK (week BETWEEN 1 AND 53)
);
GO

-- ORDER_ITEM
CREATE TABLE ORDER_ITEM (
    order_item_id VARCHAR(20)    NOT NULL,
    order_id      VARCHAR(20)    NOT NULL,
    product_id    VARCHAR(10)    NOT NULL,
    promo_id      VARCHAR(10)    NULL,   -- NULL when no promotion applied
    quantity      INT            NOT NULL DEFAULT 1,
    item_discount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    CONSTRAINT PK_ORDER_ITEM          PRIMARY KEY (order_item_id),
    CONSTRAINT FK_OI_ORDER            FOREIGN KEY (order_id)
        REFERENCES [ORDER] (order_id),
    CONSTRAINT FK_OI_PRODUCT          FOREIGN KEY (product_id)
        REFERENCES PRODUCT (product_id),
    CONSTRAINT FK_OI_PROMOTION        FOREIGN KEY (promo_id)
        REFERENCES PROMOTION (promo_id),
    CONSTRAINT CK_OI_QUANTITY         CHECK (quantity > 0),
    CONSTRAINT CK_OI_DISCOUNT         CHECK (item_discount >= 0)
);
GO

-- ============================================================
--  PRICING DIMENSION
-- ============================================================

-- PRICE_CHANGE  (composite PK — product + year + week)
CREATE TABLE PRICE_CHANGE (
    product_id VARCHAR(10)    NOT NULL,
    year       SMALLINT       NOT NULL,
    week       TINYINT        NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    CONSTRAINT PK_PRICE_CHANGE         PRIMARY KEY (product_id, year, week),
    CONSTRAINT FK_PC_PRODUCT           FOREIGN KEY (product_id)
        REFERENCES PRODUCT (product_id),
    CONSTRAINT CK_PC_UNIT_PRICE        CHECK (unit_price > 0),
    CONSTRAINT CK_PC_WEEK              CHECK (week BETWEEN 1 AND 53)
);
GO

-- ============================================================
--  EXTERNAL / CONTEXTUAL TABLES
-- ============================================================

-- EXTERNAL_FACTOR  (weather, macro indicators per store per week)
CREATE TABLE EXTERNAL_FACTOR (
    factor_id    VARCHAR(20)   NOT NULL,
    store_id     VARCHAR(10)   NOT NULL,
    factor_date  DATE          NOT NULL,
    is_holiday   BIT           NOT NULL DEFAULT 0,
    temp_c       DECIMAL(5, 2) NULL,
    rainfall_mm  DECIMAL(6, 2) NULL,
    trend_index  DECIMAL(6, 2) NULL,
    cpi_index    DECIMAL(6, 2) NULL,
    year         SMALLINT      NOT NULL,
    week         TINYINT       NOT NULL,
    CONSTRAINT PK_EXTERNAL_FACTOR     PRIMARY KEY (factor_id),
    CONSTRAINT FK_EF_STORE            FOREIGN KEY (store_id)
        REFERENCES STORE (store_id),
    CONSTRAINT UQ_EF_STORE_WEEK       UNIQUE (store_id, year, week),
    CONSTRAINT CK_EF_WEEK             CHECK (week BETWEEN 1 AND 53)
);
GO

-- ============================================================
--  CUSTOMER ENGAGEMENT TABLES
-- ============================================================

-- SESSION  (digital browsing sessions)
CREATE TABLE SESSION (
    session_id           VARCHAR(20) NOT NULL,
    customer_id          VARCHAR(20) NOT NULL,
    session_start        DATETIME    NOT NULL,
    session_duration_sec INT         NULL,
    pages_viewed         INT         NULL,
    device               VARCHAR(20) NULL,   -- Mobile | Desktop | Tablet
    referrer             VARCHAR(50) NULL,
    CONSTRAINT PK_SESSION          PRIMARY KEY (session_id),
    CONSTRAINT FK_SESSION_CUSTOMER FOREIGN KEY (customer_id)
        REFERENCES CUSTOMER (customer_id)
);
GO

-- CAMPAIGN_TOUCH  (marketing touchpoints per customer)
CREATE TABLE CAMPAIGN_TOUCH (
    touch_id      VARCHAR(20)  NOT NULL,
    customer_id   VARCHAR(20)  NOT NULL,
    touch_date    DATE         NOT NULL,
    channel       VARCHAR(20)  NOT NULL,   -- Email | SMS | Push | WhatsApp …
    campaign_name VARCHAR(100) NULL,
    outcome       TINYINT      NOT NULL DEFAULT 0,  -- 0 = no action, 1 = conversion
    CONSTRAINT PK_CAMPAIGN_TOUCH         PRIMARY KEY (touch_id),
    CONSTRAINT FK_CT_CUSTOMER            FOREIGN KEY (customer_id)
        REFERENCES CUSTOMER (customer_id)
);
GO

-- SUPPORT_TICKET  (customer service interactions)
CREATE TABLE SUPPORT_TICKET (
    ticket_id            VARCHAR(20)   NOT NULL,
    customer_id          VARCHAR(20)   NOT NULL,
    created_date         DATE          NOT NULL,
    issue_type           VARCHAR(50)   NULL,
    status               VARCHAR(20)   NOT NULL DEFAULT 'Open',  -- Open | Resolved | Pending
    resolution_time_hr   DECIMAL(6, 2) NULL,
    csat_score           TINYINT       NULL,  -- 1–5 scale
    resolution_time_days DECIMAL(6, 2) NULL,
    CONSTRAINT PK_SUPPORT_TICKET         PRIMARY KEY (ticket_id),
    CONSTRAINT FK_ST_CUSTOMER            FOREIGN KEY (customer_id)
        REFERENCES CUSTOMER (customer_id),
    CONSTRAINT CK_ST_CSAT               CHECK (csat_score BETWEEN 1 AND 5 OR csat_score IS NULL)
);
GO

-- ============================================================
--  INDEXES FOR COMMON QUERY PATTERNS
-- ============================================================

-- Order lookups by customer and date
CREATE INDEX IX_ORDER_CUSTOMER    ON [ORDER] (customer_id, order_date);
CREATE INDEX IX_ORDER_STORE_WEEK  ON [ORDER] (store_id, year, week);

-- Order item lookups
CREATE INDEX IX_OI_ORDER          ON ORDER_ITEM (order_id);
CREATE INDEX IX_OI_PRODUCT        ON ORDER_ITEM (product_id);

-- Product lookups by category / brand
CREATE INDEX IX_PRODUCT_CATEGORY  ON PRODUCT (category_id);
CREATE INDEX IX_PRODUCT_BRAND     ON PRODUCT (brand);

-- Price lookups by time window
CREATE INDEX IX_PC_YEAR_WEEK      ON PRICE_CHANGE (year, week);

-- External factor lookups by store and week
CREATE INDEX IX_EF_STORE_WEEK     ON EXTERNAL_FACTOR (store_id, year, week);

-- Session and engagement lookups
CREATE INDEX IX_SESSION_CUSTOMER  ON SESSION (customer_id, session_start);
CREATE INDEX IX_CT_CUSTOMER_DATE  ON CAMPAIGN_TOUCH (customer_id, touch_date);
CREATE INDEX IX_ST_CUSTOMER_DATE  ON SUPPORT_TICKET (customer_id, created_date);
GO


