import unittest
import json

from main import app


class PastebinUnitTest(unittest.TestCase):

    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the home route
    def test_home(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    # get not supported
    def test_register_get_fail1(self):
        response = self.app.get("/register")
        self.assertEqual(response.status_code, 405)

    # post with no content fails
    def test_register_post_fail1(self):
        response = self.app.post("/register")
        self.assertEqual(response.status_code, 415)

    def test_register_post_valid(self):
        response = self.app.post(
            "/register", json={"id": "ajit1@ajit.com", "name": "Ajit S"}
        )
        json_data = response.get_json()
        self.assertEqual(response.status_code, 200)
        print("Response - " + str(response.data))

    def test_get_all_notes_without_token(self):
        response = self.app.get("/get_all_notes")
        self.assertEqual(response.status_code, 403)

    def test_add_note_without_token(self):
        response = self.app.post("/add_note")
        self.assertEqual(response.status_code, 403)

    def test_delete_note_without_token(self):
        response = self.app.post("/delete_note")
        self.assertEqual(response.status_code, 403)

    def test_update_note_without_token(self):
        response = self.app.post("/update_note")
        self.assertEqual(response.status_code, 403)

    def test_get_all_notes_with_invalid_token(self):
        headers = {"Content-Type": "application/json", "token": "invalid_token"}
        response = self.app.get("/get_all_notes", headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403)

    def test_add_note_with_invalid_token(self):
        headers = {"Content-Type": "application/json", "token": "invalid_token"}
        response = self.app.get("/add_note", headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 405)

    def test_delete_note_with_invalid_token(self):
        headers = {"Content-Type": "application/json", "token": "invalid_token"}
        response = self.app.post("/delete_note", headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403)

    def test_update_note_with_invalid_token(self):
        headers = {"Content-Type": "application/json", "token": "invalid_token"}
        response = self.app.post("/update_note", headers=headers)
        print("test_get_all_notes_with_invalid_token Response - " + str(response.data))
        self.assertEqual(response.status_code, 403)

    def test_integration_register_post_and_update(self):
        _name = "Ajit S"
        _id = "ajit1@ajit.com"

        # Registration phase
        reg_resp = self.app.post("/register", json={"id": _id, "name": _name})
        r_dict = json.loads(reg_resp.get_json())
        _token = r_dict["token"]

        self.assertEqual(reg_resp.status_code, 200)

        headers = {"Content-Type": "application/json", "token": _token}
        # Posting phase
        note_payload = {"note": "test note", "is_public": False}
        add_resp = self.app.post("/add_note", headers=headers, json=note_payload)
        note_response_payload = json.loads(add_resp.get_json())

        _note_id = note_response_payload["note_id"]

        self.assertEqual(add_resp.status_code, 200)
        self.assertEqual(note_response_payload["note"], note_payload["note"])
        self.assertEqual(note_response_payload["owner_id"], _id)

        # Updating phase
        update_payload = {"note_id": _note_id, "note": "updated test note"}
        upd_resp = self.app.post("/update_note", headers=headers, json=update_payload)
        update_response_payload = json.loads(upd_resp.get_json())

        self.assertEqual(upd_resp.status_code, 200)
        self.assertEqual(update_response_payload["status"], "success")

    def test_integration_register_post_set_public(self):
        _name = "Roman P"
        _id = "roman@roman.com"

        # Registration phase
        reg_resp = self.app.post("/register", json={"id": _id, "name": _name})
        print(reg_resp.get_json())
        r_dict = json.loads(reg_resp.get_json())
        _token = r_dict["token"]

        headers = {"Content-Type": "application/json", "token": _token}

        # Posting phase
        note_payload = {"note": "test note", "is_public": False}
        add_resp = self.app.post("/add_note", headers=headers, json=note_payload)
        note_response_payload = json.loads(add_resp.get_json())

        _note_id = note_response_payload["note_id"]

        self.assertEqual(add_resp.status_code, 200)
        self.assertEqual(note_response_payload["note"], note_payload["note"])
        self.assertEqual(note_response_payload["owner_id"], _id)

        # Updating phase
        update_payload = {"note_id": _note_id, "is_public": True}
        upd_resp = self.app.post("/update_note", headers=headers, json=update_payload)
        update_response_payload = json.loads(upd_resp.get_json())

        self.assertEqual(upd_resp.status_code, 200)
        self.assertEqual(update_response_payload["status"], "success")

        list_resp = self.app.get("/get_all_notes", headers=headers)

        test_note = json.loads(list_resp.get_json()[0])

        self.assertTrue(test_note["is_public"])
        self.assertEqual(test_note["note_id"], _note_id)

    def test_integration_register_post_public_list_and_delete(self):
        _name = "Stephen S"
        _id = "stephen@stephen.com"

        # Registration phase
        reg_resp = self.app.post("/register", json={"id": _id, "name": _name})
        reg_resp_payload = json.loads(reg_resp.get_json())
        _token = reg_resp_payload["token"]

        headers = {"Content-Type": "application/json", "token": _token}

        # Posting phase
        note_payload = {"note": "test public note", "is_public": True}
        add_resp = self.app.post("/add_note", headers=headers, json=note_payload)
        note_response_payload = json.loads(add_resp.get_json())

        _note_id = note_response_payload["note_id"]

        self.assertEqual(add_resp.status_code, 200)
        self.assertEqual(note_response_payload["note"], note_payload["note"])
        self.assertEqual(note_response_payload["owner_id"], _id)

        # Listing public notes
        headers_no_jwt = {"Content-Type": "application/json"}

        list_resp = self.app.get("/", headers=headers_no_jwt)

        # Since the note created was public, it should be accessible at root URL
        test_note = json.loads(
            [n for n in list_resp.get_json() if f'"note_id": {_note_id}' in n][0]
        )

        self.assertEqual(test_note["note_id"], _note_id)

        # Delete phase
        del_payload = {"note_id": _note_id}
        del_resp = self.app.post("/delete_note", headers=headers, json=del_payload)
        del_resp_payload = json.loads(del_resp.get_json())

        self.assertEqual(del_resp_payload["status"], "success")

        list_resp = self.app.get("/", headers=headers_no_jwt)
        self.assertEqual(
            len([n for n in list_resp.get_json() if f'"note_id": {_note_id}' in n]), 0
        )


if __name__ == "__main__":
    unittest.main()
