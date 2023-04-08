from django.test import TestCase
from .models import User
from .models import Business, Review
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.test import Client
# Create your tests here.


def create_test_user(id_, name, email='test@gmail.com'):
    return User(
        id=id_,
        username=id_,
        name=name,
        email=email,
    )


def create_test_business(id_, name, city):
    return Business(
        id=id_,
        alias='Test Business Alias',
        name=name,
        image_url='https:://test.com/image_url',
        url='https://test.com/url',
        is_closed=False,
        review_count=0,
        latitude=34.5,
        longitude=45.6,
        rating=5,
        price='$',
        city=city,
        zip_code='95000',
        country='US',
        state='CA',
        address='Test Address, Test City',
        phone='1111111'
    )


def create_test_review(id_, user, business, rating):
    return Review(
        id=id_,
        url='https://test.com/url',
        text='Text Text',
        rating=rating,
        time_created=timezone.now(),
        user=user,
        business=business
    )


class UserModelTests(TestCase):
    def test_str(self):
        user = create_test_user('test_user', 'Test Name')
        self.assertEqual(str(user), 'Test Name')

    def test_rated_businesses(self):
        user = create_test_user('test_user', 'Test Name')
        business1 = create_test_business('test_business_1', 'Test Business 1', 'City 1')
        business2 = create_test_business('test_business_2', 'Test Business 2', 'City 2')
        business3 = create_test_business('test_business_3', 'Test Business 3', 'City 3')
        user.save()
        business1.save()
        business2.save()
        business3.save()
        review1 = create_test_review('test_review_1', user, business1, 5)
        review2 = create_test_review('test_review_2', user, business2, 5)
        review3 = create_test_review('test_review_3', user, business3, 5)
        review1.save()
        review2.save()
        review3.save()

        self.assertQuerysetEqual(user.rated_businesses(), [business1, business2, business3], ordered=False)

    def test_content_based_recommendations(self):
        user = create_test_user('test_user', 'Test Name')
        user.save()
        business1 = create_test_business('test_business_1', 'Test Business 1', 'Visited City')
        business2 = create_test_business('test_business_2', 'Test Business 2', 'Visited City')
        business3 = create_test_business('test_business_3', 'Test Business 3', 'New City')
        business1.save()
        business2.save()
        business3.save()
        review = create_test_review('test_review', user, business1, 5)
        review.save()

        self.assertQuerysetEqual(user.content_based_recommended_businesses(), [business2], ordered=False)

    def test_collaborative_based_recommendation(self):

        user1 = create_test_user('test_user1', 'Test Name1')
        user2 = create_test_user('test_user2', 'Test Name2')
        # save instance to database
        # assign id
        user1.save()
        user2.save()
        business1 = create_test_business('test_business_1', 'Test Business 1', 'Visited City')
        business2 = create_test_business('test_business_2', 'Test Business 2', 'Visited City')
        business3 = create_test_business('test_business_3', 'Test Business 3', 'Visited City')
        business1.save()
        business2.save()
        business3.save()
        user1_business1_review = create_test_review('u1b1_review', user1, business1, 5)
        user2_business1_review = create_test_review('u2b1_review', user2, business1, 5)
        user2_business2_review = create_test_review('u2b2_review', user2, business2, 5)
        user1_business1_review.save()
        user2_business1_review.save()
        user2_business2_review.save()

        # save into database collaborative_based_recommended_businesses() call database
        self.assertQuerysetEqual(user1.collaborative_based_recommended_businesses(), [business2], ordered=False)


class BusinessModelTests(TestCase):
    def test_str(self):
        business = create_test_business('test_business', 'Test Business', 'Test City')
        self.assertEqual(str(business), 'Test Business')


class ReviewModelTests(TestCase):
    def test_str(self):
        user = create_test_user('test_user', 'Test Name')
        business = create_test_business('test_business', 'Test Business', 'Test City')
        user_business_review = create_test_review('u1b1_review', user, business, 5)

        # no save into database
        self.assertEqual(str(user_business_review), str(user) + ' rates ' + str(business) + ' at ' + \
                         str(user_business_review.rating) + ' Star.')


class BusinessIndexViewTests(TestCase):
    def test_no_businesses(self):
        response = self.client.get(reverse('business_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No businesses are available.')
        self.assertQuerysetEqual(response.context['business_list'], [])

    def test_two_businesses(self):
        business1 = create_test_business('test_business_1', 'Test Business 1', 'Visited City')
        business2 = create_test_business('test_business_2', 'Test Business 2', 'Visited City')
        business1.save()
        business2.save()
        response = self.client.get(reverse('business_index'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'No businesses are available.')
        self.assertQuerysetEqual(response.context['business_list'], [business1, business2], ordered=False)

    def test_business_detail_exist(self):
        business = create_test_business('test_business', 'Test Business', 'City')
        business.save()
        response = self.client.get(reverse('business_detail', args=('test_business',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['business'], business)


class LoginViewTests(TestCase):

    def setUp(self):
        # create one test user
        user = create_test_user('test_user', 'test_user')
        # must use user.set_password, requires using hashing!
        user.set_password('102030aa')
        user.save()

    def test_login_success(self):
        login = self.client.login(username='test_user', password='102030aa')
        self.assertTrue(login)

    def test_login_fail_with_wrong_password(self):
        login = self.client.login(username='test_user', password='102030')
        self.assertFalse(login)

    def test_login_redirect_page(self):
        response = self.client.post(reverse('login'), {'username': 'test_user', 'password': '102030aa'},
                                    follow=True)
        print(response.redirect_chain)
        self.assertEqual(response.status_code, 200)
        # redirect to 'business_index
        self.assertRedirects(response, expected_url=reverse('business_index'))






    # class RegisterViewTests(TestCase):
#     """
#      Base class for the test cases; this sets up two active users
#     """
#     def setUp(self):
#         self.sample_user1 = create_test_user('test_user1', 'Test Name1')
#         self.sample_user2 = create_test_user('test_user2', 'Test Name2')
#         self.sample_user1.save()
#         self.sample_user2.save()








