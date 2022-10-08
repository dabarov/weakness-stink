CREATE TABLE aliases
(
    id            SERIAL PRIMARY KEY,
    chat_id       INT          NOT NULL,
    sticker_id    VARCHAR(100) NOT NULL,
    sticker_alias VARCHAR(100) NOT NULL,
    UNIQUE (chat_id, sticker_alias)
);
