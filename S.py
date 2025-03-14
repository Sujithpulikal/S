accommodation_query = """
INSERT INTO expense_accommodation_mapper (
    expense_request_id,
    location,
    hotel_name,
    check_in,
    check_out,
    accommodation_cost,
    food_cost,
    note,
    total_accommodation_cost,
    created_by
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


attachment_query = """
INSERT INTO expense_attachment (
    expense_request_id,
    file_name,
    file_type,
    file_size,
    created_by
) VALUES (%s, %s, %s, %s, %s)
"""
travel_query = """
INSERT INTO expense_travel_mapper (
    expense_request_id,
    travel_type_id,
    travel_start_date,
    travel_end_date,
    travel_origin,
    travel_destination,
    note,
    travel_total_expense,
    created_by
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
