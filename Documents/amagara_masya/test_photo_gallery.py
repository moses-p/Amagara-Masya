import os
import requests
from datetime import datetime
from create_test_image import create_test_image

# API Configuration
BASE_URL = 'http://localhost:8000/api'
TOKEN = None  # Will be set after login

def login(username, password):
    global TOKEN
    try:
        response = requests.post(f'{BASE_URL}/token/', data={
            'username': username,
            'password': password
        })
        if response.status_code == 200:
            TOKEN = response.json()['access']
            print("✅ Login successful")
            return True
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure Django server is running.")
        return False

def get_headers():
    return {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

def create_test_child():
    try:
        child_data = {
            'first_name': 'Test',
            'last_name': 'Child',
            'date_of_birth': '2010-01-01',
            'gender': 'M',
            'status': 'active'
        }
        response = requests.post(
            f'{BASE_URL}/children/children/',
            json=child_data,
            headers=get_headers()
        )
        if response.status_code == 201:
            print("✅ Test child created")
            return response.json()
        print(f"❌ Failed to create test child: {response.status_code} - {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error creating test child: {str(e)}")
        return None

def upload_test_photo(child_id):
    try:
        # Create a test image file
        test_image_path = 'test_image.jpg'
        create_test_image(test_image_path)

        # Upload the photo
        with open(test_image_path, 'rb') as f:
            files = {'photo': f}
            data = {
                'description': f'Test photo uploaded at {datetime.now()}',
                'child': child_id
            }
            response = requests.post(
                f'{BASE_URL}/children/children/{child_id}/photos/',
                files=files,
                data=data,
                headers={'Authorization': f'Bearer {TOKEN}'}
            )

        # Clean up test image
        os.remove(test_image_path)

        if response.status_code == 201:
            print("✅ Test photo uploaded")
            return response.json()
        print(f"❌ Failed to upload test photo: {response.status_code} - {response.text}")
        return None
    except Exception as e:
        print(f"❌ Error uploading test photo: {str(e)}")
        return None

def get_child_photos(child_id):
    try:
        response = requests.get(
            f'{BASE_URL}/children/children/{child_id}/photos/',
            headers=get_headers()
        )
        if response.status_code == 200:
            print("✅ Retrieved child photos")
            return response.json()
        print(f"❌ Failed to retrieve child photos: {response.status_code} - {response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error retrieving child photos: {str(e)}")
        return None

def delete_photo(child_id, photo_id):
    try:
        response = requests.delete(
            f'{BASE_URL}/children/children/{child_id}/photos/{photo_id}/',
            headers=get_headers()
        )
        if response.status_code == 204:
            print("✅ Photo deleted")
            return True
        print(f"❌ Failed to delete photo: {response.status_code} - {response.text}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error deleting photo: {str(e)}")
        return False

def test_photo_gallery():
    print("\n🔍 Testing Photo Gallery Implementation")
    print("=====================================")

    # 1. Login
    if not login('genius', 'genius'):  # Updated credentials
        return

    # 2. Create test child
    child = create_test_child()
    if not child:
        return

    # 3. Upload test photos
    photo1 = upload_test_photo(child['id'])
    photo2 = upload_test_photo(child['id'])
    if not photo1 or not photo2:
        return

    # 4. Get and verify photos
    photos = get_child_photos(child['id'])
    if not photos:
        return

    print(f"\n📸 Found {len(photos)} photos for child {child['first_name']} {child['last_name']}")
    for photo in photos:
        print(f"- Photo ID: {photo['id']}")
        print(f"  URL: {photo['url']}")
        print(f"  Date: {photo['date']}")
        print(f"  Description: {photo['description']}")

    # 5. Delete a photo
    if photos:
        delete_photo(child['id'], photos[0]['id'])

    # 6. Verify deletion
    remaining_photos = get_child_photos(child['id'])
    print(f"\n📸 Remaining photos: {len(remaining_photos)}")

    print("\n✅ Photo gallery test completed!")

if __name__ == '__main__':
    test_photo_gallery() 