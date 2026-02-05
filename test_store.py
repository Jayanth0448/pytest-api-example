from jsonschema import validate
import time
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_

@pytest.fixture
def create_order():
    # Generate unique pet_id using timestamp to avoid conflicts
    # Available pets: 0 (cat), 1 (dog), 2 (fish)
    unique_pet_id = int(time.time() * 1000) % 3  # Returns 0-2
    order_data = {"pet_id": unique_pet_id}
    response = api_helpers.post_api_data("/store/order", order_data)
    assert response.status_code == 201
    return response.json()

'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
def test_patch_order_by_id(create_order):
    order = create_order
    order_id = order['id']
    
    # Validate created order against schema
    validate(instance=order, schema=schemas.order)
    
    # Update the order status to 'sold'
    update_data = {"status": "sold"}
    
    # Validate update data against schema
    validate(instance=update_data, schema=schemas.order_update)
    
    response = api_helpers.patch_api_data(f"/store/order/{order_id}", update_data)
    
    # Validate response code
    assert response.status_code == 200
    
    # Validate response contains the success message
    response_data = response.json()
    assert_that(response_data['message'], contains_string("Order and pet status updated successfully"))