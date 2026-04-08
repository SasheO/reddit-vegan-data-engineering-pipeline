-- post_id,created_utc,post_title,author_id,author_username,upvote_count,downvote_count,comments_count,crossposts_count,awards_received_count,post_text,post_url,has_media,media_type,media_title,media_src,media_url
CREATE TABLE POSTS (
post_id CHAR(7) NOT NULL UNIQUE,
created_utc TIMESTAMPTZ NOT NULL, -- utc time
post_title VARCHAR(130) NOT NULL, -- truncate title to given varchar characters
author_id VARCHAR(20) NOT NULL, -- truncate title to given varchar characters
author_username VARCHAR(30) NOT NULL, -- truncate title to given varchar characters
upvote_count INTEGER NOT NULL,
downvote_count INTEGER NOT NULL,
comments_count INTEGER NOT NULL,
crossposts_count SMALLINT NOT NULL,
awards_received_count SMALLINT NOT NULL,
post_text VARCHAR(1000), -- truncate title to given varchar characters
post_url VARCHAR(130) NOT NULL, -- truncate title to given varchar characters
has_media BIT NOT NULL, -- boolean data type
media_type VARCHAR(20), -- truncate title to given varchar characters
media_title VARCHAR(130), -- truncate title to given varchar characters
media_src VARCHAR(130), -- truncate title to given varchar characters
media_url VARCHAR(130), -- truncate title to given varchar characters
PRIMARY KEY (POST_ID));