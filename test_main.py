from main import app
from fastapi.testclient import TestClient
import pytest

class CollectionForTestCheck:
    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            self.collected.append(item.nodeid)


client = TestClient(app)



def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_list_endpoints():
    response = client.get("/list-endpoints")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_check_all_endpoints_for_test_function():
    endpoints_response=client.get("/openapi.json").json()
    endpoint_paths=endpoints_response['paths']
    api_endpoint_functions=[]
    for endpoint in endpoint_paths:
        for endpoint_method in endpoint_paths[endpoint]:
            endpoint_slug=endpoint[1:].replace("/","_")
            length_of_suffix=len(f"_{endpoint_slug}_{endpoint_method}")
            api_endpoint_functions.append(endpoint_paths[endpoint][endpoint_method]['operationId'][:-length_of_suffix])
    coll = CollectionForTestCheck()
    pytest.main(['--collect-only'], plugins=[coll])
    test_functions=[]
    for test_coll in coll.collected:
        test_functions.append(str(test_coll).split("::")[-1])

    for api_endpoint_function in api_endpoint_functions:
        assert "test_"+str(api_endpoint_function) in test_functions, f"Test function of {api_endpoint_function} couldn't found"

def test_check_all_endpoints_for_success_response_model():
    endpoints=client.get("/openapi.json").json()['paths']
    for endpoint in endpoints:
        for endpoint_method in endpoints[endpoint]:
            assert "$ref" in endpoints[endpoint][endpoint_method]['responses']['200']['content']['application/json'][
                'schema'] \
                   or "title" in \
                   endpoints[endpoint][endpoint_method]['responses']['200']['content']['application/json'][
                       'schema'], f"response_model isn't defined for method: {endpoint_method} endpoint: {endpoint} "
