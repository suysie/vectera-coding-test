from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from meetings.models import Meeting

class ValidationTest(APITestCase):
    def test_create_meeting_missing_title(self):
        url = reverse('meeting-list')
        data = {'started_at': timezone.now().isoformat()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_meeting_missing_started_at(self):
        url = reverse('meeting-list')
        data = {'title': 'Test Meeting'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_note_missing_author(self):
        meeting = Meeting.objects.create(title="Test", started_at=timezone.now())
        url = reverse('meeting-add-note', args=[meeting.id])
        data = {'text': 'Note without author'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_note_missing_text(self):
        meeting = Meeting.objects.create(title="Test", started_at=timezone.now())
        url = reverse('meeting-add-note', args=[meeting.id])
        data = {'author': 'John'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_meeting(self):
        url = reverse('meeting-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_summary_when_none_exists(self):
        meeting = Meeting.objects.create(title="Test", started_at=timezone.now())
        url = reverse('meeting-get-summary', args=[meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
