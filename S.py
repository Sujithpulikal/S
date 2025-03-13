query = """
INSERT INTO expense_accommodation_mapper (
    location,
    hotel_name,
    check_in,
    check_out,
    accommodation_cost,
    food_cost,
    total_accommodation_cost,
    created_by,
    created_on,
    modified_by,
    modified_on
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, NOW())
"""

def add_accommodation_mapper(conn, accommodation: ExpenseAccommodationMapper, user_id: str):
    cursor = conn.cursor()

    data = (
        accommodation.location,
        accommodation.hotel_name,
        accommodation.check_in,
        accommodation.check_out,
        accommodation.accommodation_cost,
        accommodation.food_cost,
        accommodation.total_accommodation_cost,
        user_id,
        user_id
    )

    cursor.execute(query, data)
    conn.commit()
    cursor.close()
