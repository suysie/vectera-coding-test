from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.utils import timezone
from meetings.models import Meeting, Note, Summary

class MeetingAPITest(APITestCase):
    def setUp(self):
        self.meeting = Meeting.objects.create(
            title="Test Meeting",
            started_at=timezone.now()
        )

    def test_list_meetings(self):
        url = reverse('meeting-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_get_meeting_detail(self):
        url = reverse('meeting-detail', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Meeting")

    def test_create_meeting(self):
        url = reverse('meeting-list')
        data = {'title': 'New Meeting', 'started_at': timezone.now().isoformat()}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 2)

    def test_add_note(self):
        url = reverse('meeting-add-note', args=[self.meeting.id])
        data = {'author': 'John', 'text': 'Test note'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)

    def test_list_notes(self):
        Note.objects.create(meeting=self.meeting, author="John", text="Note 1")
        url = reverse('meeting-list-notes', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_generate_summary(self):
        Note.objects.create(meeting=self.meeting, author="John", text="Test note")
        url = reverse('meeting-summarize', args=[self.meeting.id])
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Summary.objects.count(), 1)

    def test_get_summary(self):
        Summary.objects.create(
            meeting=self.meeting,
            status=Summary.READY,
            content="Test summary"
        )
        url = reverse('meeting-get-summary', args=[self.meeting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], "Test summary")
