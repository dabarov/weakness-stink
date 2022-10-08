SELECT_ALIAS_QUERY = "SELECT sticker_id FROM aliases WHERE sticker_alias=%s and chat_id=%s"
INSERT_ALIAS_QUERY = "INSERT INTO aliases (chat_id, sticker_id, sticker_alias) values (%s, %s, %s)"
