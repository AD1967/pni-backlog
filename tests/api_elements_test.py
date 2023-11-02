from for_all_tests import test_with_auth


test_with_auth("1", url = "http://127.0.0.1:5000/data/elements/volume")
test_with_auth("2", url = "http://127.0.0.1:5000/data/elements/period", params={'name':'', 'id_period':'' })
test_with_auth("3", url = "http://127.0.0.1:5000/data/element/convector/1")
test_with_auth("4", url = "http://127.0.0.1:5000/data/element/airheater/1", params={'name':''})
