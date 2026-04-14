-- Synapse SQLite schema
-- This database is fully derived from notes/. It can be deleted and rebuilt
-- at any time with `python tools/build_index.py`.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS papers (
    id                       TEXT PRIMARY KEY,
    title                    TEXT NOT NULL,
    year                     INTEGER,
    journal                  TEXT,
    doi                      TEXT,
    volume                   TEXT,
    issue                    TEXT,
    pages                    TEXT,
    paper_type               TEXT,
    methods                  TEXT,
    industry                 TEXT,
    country                  TEXT,
    time_period              TEXT,
    units                    TEXT,
    n_sample                 TEXT,
    research_question        TEXT,
    mechanism_summary        TEXT,
    iv                       TEXT,
    dv                       TEXT,
    mediators                TEXT,
    moderators               TEXT,
    theoretical_contribution TEXT,
    practical_implication    TEXT,
    limitations              TEXT,
    future_research          TEXT,
    abstract                 TEXT,
    apa_citation             TEXT,
    -- Custom analytic fields (v1 extension)
    unit_of_analysis         TEXT,   -- e.g., firm, individual, dyad, team, country
    level_of_theory          TEXT,   -- micro / meso / macro
    dependent_variable_family TEXT,  -- financial / social / environmental / mixed / n-a
    source                   TEXT,
    pdf_path                 TEXT,
    text_path                TEXT,
    note_path                TEXT,
    extraction_model         TEXT,
    extraction_version       TEXT,
    ingested_at              TEXT
);

CREATE TABLE IF NOT EXISTS authors (
    paper_id                 TEXT NOT NULL,
    position                 INTEGER NOT NULL,
    name                     TEXT NOT NULL,
    PRIMARY KEY (paper_id, position),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS theories (
    paper_id                 TEXT NOT NULL,
    theory                   TEXT NOT NULL,
    PRIMARY KEY (paper_id, theory),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS keywords (
    paper_id                 TEXT NOT NULL,
    keyword                  TEXT NOT NULL,
    PRIMARY KEY (paper_id, keyword),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);

-- Controlled-vocabulary topic tags. The allowed set lives in index/topics.json
-- and is enforced by tools/validate_note.py. One paper can belong to multiple topics.
CREATE TABLE IF NOT EXISTS topics (
    paper_id                 TEXT NOT NULL,
    topic                    TEXT NOT NULL,
    PRIMARY KEY (paper_id, topic),
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE
);

-- Full-text search across the analytic body of every paper.
CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
    id UNINDEXED,
    title,
    abstract,
    research_question,
    mechanism_summary,
    theoretical_contribution,
    practical_implication
);

CREATE INDEX IF NOT EXISTS idx_papers_year      ON papers(year);
CREATE INDEX IF NOT EXISTS idx_papers_journal   ON papers(journal);
CREATE INDEX IF NOT EXISTS idx_papers_source    ON papers(source);
CREATE INDEX IF NOT EXISTS idx_authors_name     ON authors(name);
CREATE INDEX IF NOT EXISTS idx_theories_theory  ON theories(theory);
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_topics_topic    ON topics(topic);
CREATE INDEX IF NOT EXISTS idx_papers_unit     ON papers(unit_of_analysis);
CREATE INDEX IF NOT EXISTS idx_papers_level    ON papers(level_of_theory);
CREATE INDEX IF NOT EXISTS idx_papers_dv_fam   ON papers(dependent_variable_family);
