import logging
from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Meeting, Note, Summary
from .serializers import MeetingSerializer, NoteSerializer, SummarySerializer
from .services.ai import summarize

log = logging.getLogger(__name__)

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all().annotate(note_count=Count("notes"))
    serializer_class = MeetingSerializer

    @action(detail=True, methods=["post"], url_path="notes")
    def add_note(self, request, pk=None):
        meeting = self.get_object()
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(meeting=meeting)
            log.info("note_added", extra={"meeting_id": pk, "note_count": meeting.notes.count()})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="notes-list")
    def list_notes(self, request, pk=None):
        meeting = self.get_object()
        notes = meeting.notes.all().order_by('created_at')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="summarize")
    def summarize(self, request, pk=None):
        meeting = self.get_object()
        summary, created = Summary.objects.get_or_create(meeting=meeting, defaults={'status': Summary.PENDING})
        
        if created:
            notes_text = " ".join([note.text for note in meeting.notes.all()])
            try:
                summary.content = summarize(notes_text)
                summary.status = Summary.READY
                log.info("summary_generated", extra={"meeting_id": pk, "note_count": meeting.notes.count()})
            except Exception as e:
                summary.status = Summary.FAILED
                summary.content = f"Summary failed: {str(e)}"
                log.error("summary_failed", extra={"meeting_id": pk, "error": str(e)})
            summary.save()
        
        serializer = SummarySerializer(summary)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=["get"], url_path="summary")
    def get_summary(self, request, pk=None):
        meeting = self.get_object()
        if not hasattr(meeting, 'summary') or meeting.summary is None:
            return Response({"detail": "No summary available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = SummarySerializer(meeting.summary)
        return Response(serializer.data)
