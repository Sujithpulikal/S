cursor.execute("""
                    INSERT INTO expense_attachments (expense_request_id, file_name, file_size, file_data, file_type,
                                                     created_by, created_on, modified_by, modified_on)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW(), %s, NOW())
                """, (expense_request_id, attachment.file_name, attachment.file_size,
                      attachment.file_data, attachment.file_type, request.user_id, request.user_id))
