SELECT_STICKER_QUERY = """
SELECT sticker_id
FROM aliases
WHERE sticker_alias=%s AND chat_id=%s
"""

SELECT_ALIASES_FOR_CHAT_QUERY = """
SELECT sticker_alias
FROM aliases
WHERE chat_id=%s
"""

INSERT_ALIAS_QUERY = """
INSERT INTO aliases (chat_id, sticker_id, sticker_alias)
VALUES (%s, %s, %s)
"""
