from datetime import date
import pytest
from main import app, db, User, Car


# Fixtures
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()


# Helper functions
def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


# Tests
def test_register(client):
    response = client.post('/register', data=dict(
        name='Test User',
        email='test@example.com',
        password='test_password',
        role='uploader'
    ), follow_redirects=True)

    assert response.status_code == 200


def test_login_logout(client):
    login(client, 'john@example.com', 'password123')

    response = logout(client)
    assert response.status_code == 200


def test_add_new_post(client):
    login(client, 'john@example.com', 'password123')

    response = client.post('/new-post', data=dict(
        Mark='Toyota',
        Model='Camry',
        body='Sedan',
        img_url='https://example.com/toyota.jpg',
        Transmission='Automatic',
        Category='Compact'
    ), follow_redirects=True)

    assert response.status_code == 200


def test_show_post(client):
    car = Car(
        mark='Toyota',
        model='Camry',
        body='Sedan',
        img_url='https://example.com/toyota.jpg',
        transmission='Automatic',
        category='Compact',
        date=date.today().strftime("%B %d, %Y")
    )
    db.session.add(car)
    db.session.commit()

    response = client.get(f'/post/{car.id}')
    assert response.status_code == 200


def test_reserve_car(client):
    login(client, 'john@example.com', 'password123')

    user = User.query.filter_by(email='john@example.com').first()

    car = Car(
        mark='Toyota',
        model='Camry',
        body='Sedan',
        owner=user,
        img_url='https://example.com/toyota.jpg',
        transmission='Automatic',
        category='Compact',
        date=date.today().strftime("%B %d, %Y")
    )
    db.session.add(car)
    db.session.commit()

    reserved_car = Car.query.get(car.id)
    assert reserved_car.is_rented != True
