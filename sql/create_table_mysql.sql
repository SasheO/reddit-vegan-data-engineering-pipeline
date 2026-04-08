CREATE TABLE POSTS (
    post_id CHAR(7) NOT NULL UNIQUE,
    created_utc TIMESTAMP NOT NULL, -- MySQL uses TIMESTAMP without timezone, store UTC
    post_title VARCHAR(130) NOT NULL,
    author_id VARCHAR(20) NOT NULL,
    author_username VARCHAR(30) NOT NULL,
    upvote_count INT NOT NULL,
    downvote_count INT NOT NULL,
    comments_count INT NOT NULL,
    crossposts_count SMALLINT NOT NULL,
    awards_received_count SMALLINT NOT NULL,
    post_text VARCHAR(1000),
    post_url VARCHAR(130) NOT NULL,
    has_media BOOLEAN NOT NULL, -- MySQL uses BOOLEAN (alias for TINYINT(1))
    media_type VARCHAR(20),
    media_title VARCHAR(130),
    media_src VARCHAR(130),
    media_url VARCHAR(130),
    PRIMARY KEY (post_id)
);