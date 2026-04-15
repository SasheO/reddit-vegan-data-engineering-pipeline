CREATE TABLE POSTS (
    post_id CHAR(7) NOT NULL UNIQUE,
    created_utc TIMESTAMP NOT NULL, -- MySQL uses TIMESTAMP without timezone, store UTC
    post_title VARCHAR(300) NOT NULL, -- changed
    author_id VARCHAR(20) NOT NULL,
    author_username VARCHAR(15) NOT NULL, -- changed
    upvote_count INT NOT NULL,
    downvote_count INT NOT NULL,
    comments_count INT NOT NULL,
    crossposts_count SMALLINT NOT NULL,
    awards_received_count SMALLINT NOT NULL,
    post_text VARCHAR(10000), -- changed
    post_url VARCHAR(130) NOT NULL,
    has_media BOOLEAN NOT NULL, -- MySQL uses BOOLEAN (alias for TINYINT(1))
    media_type VARCHAR(20),
    media_title VARCHAR(300), -- changed
    media_src VARCHAR(300), -- changed
    media_url VARCHAR(130),
    PRIMARY KEY (post_id)
);