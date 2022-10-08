CREATE TABLE aliases
(
    id         SERIAL PRIMARY KEY,
    chat_id    INT          NOT NULL,
    sticker_id VARCHAR(100) NOT NULL,
    alias      VARCHAR(100) NOT NULL,
    UNIQUE (chat_id, alias)
);
