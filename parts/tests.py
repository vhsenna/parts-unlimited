from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Part


class BasePartTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            "name": "Test Part",
            "sku": "TP123",
            "description": "A test part.",
            "weight_ounces": 10,
            "is_active": True
        }
        self.invalid_data = {
            "name": "",
            "sku": "TP123",
            "description": "A test part.",
            "weight_ounces": 10,
            "is_active": True
        }
        self.part = Part.objects.create(
            name="Existing Part",
            sku="EP123",
            description="An existing part.",
            weight_ounces=5,
            is_active=True
        )


class CreateTests(BasePartTestCase):
    def test_create_valid_part(self):
        response = self.client.post(
            reverse('part-list'),
            self.valid_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_part(self):
        response = self.client.post(reverse(
            'part-list'), self.invalid_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RetrieveTests(BasePartTestCase):
    def test_list_all_parts(self):
        response = self.client.get(reverse('part-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Part.objects.count())

    def test_retrieve_single_part(self):
        response = self.client.get(reverse('part-detail', args=[self.part.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.part.name)

    def test_list_no_parts(self):
        Part.objects.all().delete()
        response = self.client.get(reverse('part-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_retrieve_non_existent_part(self):
        response = self.client.get(reverse('part-detail', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UpdateTests(BasePartTestCase):
    def test_update_part(self):
        updated_data = self.valid_data.copy()
        updated_data['name'] = "Updated Part"
        response = self.client.put(reverse(
            'part-detail', args=[self.part.pk]), updated_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part.refresh_from_db()
        self.assertEqual(self.part.name, "Updated Part")

    def test_partial_update_part(self):
        partial_data = {"name": "Partially Updated Part"}
        response = self.client.patch(reverse(
            'part-detail', args=[self.part.pk]), partial_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part.refresh_from_db()
        self.assertEqual(self.part.name, "Partially Updated Part")

    def test_update_non_existent_part(self):
        response = self.client.put(reverse(
            'part-detail', args=[9999]), self.valid_data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeleteTests(BasePartTestCase):
    def test_delete_part(self):
        response = self.client.delete(reverse(
            'part-detail', args=[self.part.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Part.objects.filter(pk=self.part.pk).exists())

    def test_delete_non_existent_part(self):
        response = self.client.delete(reverse('part-detail', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MostCommonWordsTests(APITestCase):
    def test_no_descriptions_found(self):
        """
        Test the scenario where no descriptions are found in the database.
        """
        response = self.client.get(reverse('most-common-words'))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"message": "No descriptions found"})

    def test_no_words_found_in_descriptions(self):
        """
        Test the scenario where descriptions exist but contain no valid words.
        """
        Part.objects.create(
            name="Part 1",
            sku="SKU1",
            description="the and but",
            weight_ounces=10,
            is_active=True
        )
        response = self.client.get(reverse('most-common-words'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('most_common_words', response.data)
        self.assertEqual(response.data['most_common_words'], {})

    def test_most_common_words(self):
        """
        Test the scenario where descriptions contain valid words and the most
        common words are found.
        """
        Part.objects.create(
            name="Part 1",
            sku="SKU1",
            description="heavy load computing generator",
            weight_ounces=10,
            is_active=True
        )
        Part.objects.create(
            name="Part 2",
            sku="SKU2",
            description="light load computing",
            weight_ounces=20,
            is_active=True
        )
        Part.objects.create(
            name="Part 3",
            sku="SKU3",
            description="heavy computing load",
            weight_ounces=30,
            is_active=True
        )
        response = self.client.get(reverse('most-common-words'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["most_common_words"], {
            "load": 3,
            "heavy": 2,
            "computing": 3,
            "light": 1,
            "generator": 1
        })
