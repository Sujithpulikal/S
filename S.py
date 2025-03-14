
def insert_expense_data(conn, data: ExpenseRequest):
    cursor = conn.cursor()

    try:
        # ✅ Insert into Travel Table
        if data.Travel and len(data.Travel) > 0:
            travel_data = [
                (
                    data.expense_request_id,
                    travel.travel_type_id,
                    travel.travel_start_date,
                    travel.travel_end_date,
                    travel.travel_origin,
                    travel.travel_destination,
                    travel.note or None,
                    travel.travel_total_expense,
                    data.user_id
                )
                for travel in data.Travel
            ]
            cursor.executemany(travel_query, travel_data)
            print(f"{len(travel_data)} Travel records inserted.")

        # ✅ Insert into Attachment Table
        if data.Attachment and len(data.Attachment) > 0:
            attachment_data = [
                (
                    data.expense_request_id,
                    attachment.file_name,
                    attachment.file_type,
                    attachment.file_size,
                    data.user_id
                )
                for attachment in data.Attachment
            ]
            cursor.executemany(attachment_query, attachment_data)
            print(f"{len(attachment_data)} Attachment records inserted.")

        # ✅ Insert into Accommodation Table
        if data.Accommodation and len(data.Accommodation) > 0:
            accommodation_data = [
                (
                    data.expense_request_id,
                    accommodation.location,
                    accommodation.hotel_name or None,
                    accommodation.check_in,
                    accommodation.check_out,
                    accommodation.accommodation_cost,
                    accommodation.food_cost or None,
                    accommodation.note or None,
                    accommodation.total_accommodation_cost,
                    data.user_id
                )
                for accommodation in data.Accommodation
            ]
            cursor.executemany(accommodation_query, accommodation_data)
            print(f"{len(accommodation_data)} Accommodation records inserted.")

        # ✅ Commit if all inserts succeed
        conn.commit()
        print("All data inserted successfully.")

    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")

    finally:
        cursor.close()
