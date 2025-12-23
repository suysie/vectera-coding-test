from django.test import TestCase
from django.utils import timezone
from meetings.models import Meeting, Note, Summary

class MeetingModelTest(TestCase):
    def test_meeting_creation(self):
        meeting = Meeting.objects.create(
            title="Test Meeting",
            started_at=timezone.now()
        )
        self.assertEqual(meeting.title, "Test Meeting")
        self.assertIsNotNone(meeting.created_at)

    def test_note_creation(self):
        meeting = Meeting.objects.create(title="Test", started_at=timezone.now())
        note = Note.objects.create(meeting=meeting, author="John", text="Note text")
        self.assertEqual(note.meeting, meeting)
        self.assertEqual(note.author, "John")

    def test_summary_creation(self):
        meeting = Meeting.objects.create(title="Test", started_at=timezone.now())
        summary = Summary.objects.create(
            meeting=meeting,
            status=Summary.READY,
            content="Test summary"
        )
        self.assertEqual(summary.meeting, meeting)
        self.assertEqual(summary.status, Summary.READY)
