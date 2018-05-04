# Bring your packages onto the path
import sys, os, json
sys.path.append(os.path.abspath(os.path.join("..", "vms")))

import unittest
from vms import create_app, db
from vms.models import VisitorLog

class VMSTestCase (unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.visitor_info = {
            "visitorName": "john doe",
            "hostName": "jane doe",
            "purpose": "official",
            "cardNumber": "0012"
        }

        with self.app.app_context():
            db.create_all()

    def test_can_create_visitor_log(self):
        res = self.client.post("/api/v1/visitor-logs/",
                                data=json.dumps(self.visitor_info),
                                content_type='application/json')
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        assert res_data['timeIn'] != 'None'
    
    def test_can_view_visitor_logs(self):
        res = self.client.get("/api/v1/visitor-logs/")
        self.assertEqual(res.status_code, 200)
        
    def tearDown(self):
        """Remove resources"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()
