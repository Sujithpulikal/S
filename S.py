query = """
INSERT INTO expense_travel_mapper (
    expense_request_id,
    expense_travel_type_id,
    travel_start_date,
    travel_end_date,
    travel_origin,
    travel_destination,
    note,
    travel_total_expense,
    created_by,
    created_on,
    modified_by,
    modified_on
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())
"""

# Sample Data Insertion
def add_travel_mapper(conn, request: ExpenseRequest):
    cursor = conn.cursor()

    if request.Travel:
        for travel in request.Travel:
            data = (
                request.expense_request_id,
                travel.expense_travel_type_id,
                travel.travel_start_date,
                travel.travel_end_date,
                travel.travel_origin,
                travel.travel_destination,
                travel.note,
                travel.travel_total_expense,
                request.user_id,
                request.user_id
            )
            cursor.execute(query, data)

    conn.commit()
    cursor.close()
