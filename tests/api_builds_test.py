from for_all_tests import test_with_auth


test_with_auth("1", url = "http://127.0.0.1:5000/data/builds")
test_with_auth("2", url = "http://127.0.0.1:5000/data/builds", params={'name':'', 'id_build':'' })
test_with_auth("3", url = "http://127.0.0.1:5000/data/build/test", params={'name':'', 'id_build':'' })
test_with_auth("4", url = "http://127.0.0.1:5000/data/build/1", params={'name':'', 'id_build':'' , 'ihp': ''})
