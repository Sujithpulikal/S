for accommodation in accommodation_list:
        data = (
            request_id,
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
