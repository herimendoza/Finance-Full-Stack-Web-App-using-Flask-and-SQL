from application import application

# have to test this in pipeline - tbd

# testing root page
def testHomePage():
    response = application.test_client().get('/')
    assert response.status_code == 200

# testing home page
def testHomePage():
    response = application.test_client().get('/home')
    assert response.status_code == 200

# testing buy page
def testBuyPage():
    response = application.test_client().get('/buy')
    assert response.status_code == 200

# testing history page
def testHistoryPage():
    response = application.test_client().get('/history')
    assert response.status_code == 200

# testing login page
def testLoginPage():
    response = application.test_client().get('/login')
    assert response.status_code == 200

# testing logout page
def testLogoutPage():
    response = application.test_client().get('/logout')
    assert response.status_code == 200

# testing quote page
def testQuotePage():
    response = application.test_client().get('/quote')
    assert response.status_code == 200

# testing register page
def testRegisterPage():
    response = application.test_client().get('/register')
    assert response.status_code == 200

# testing sell page
def testSellPage():
    response = application.test_client().get('/sell')
    assert response.status_code == 200
