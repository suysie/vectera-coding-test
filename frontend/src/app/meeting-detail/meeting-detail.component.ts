import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Subject, interval, switchMap, takeUntil } from 'rxjs';
import { ApiService } from '../api.service';
import { Meeting, Note, Summary } from '../models';

@Component({
  selector: 'app-meeting-detail',
  templateUrl: './meeting-detail.component.html',
  styleUrls: ['./meeting-detail.component.css']
})
export class MeetingDetailComponent implements OnInit, OnDestroy {
  meeting: Meeting | null = null;
  notes: Note[] = [];
  summary: Summary | null = null;
  loading = true;
  error: string | null = null;
  summaryLoading = false;
  generatingSummary = false;

  newNote = { author: '', text: '' };

  private destroy$ = new Subject<void>();
  private pollingInterval = 3000;

  constructor(
    private route: ActivatedRoute,
    private api: ApiService
  ) {}

  ngOnInit() {
    const meetingId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadMeeting(meetingId);
  }

  ngOnDestroy() {
    this.destroy$.next();
    this.destroy$.complete();
  }

  loadMeeting(id: number) {
    this.loading = true;
    this.api.getMeeting(id).subscribe({
      next: (meeting) => {
        this.meeting = meeting;
        this.loadNotes(id);
        this.loadSummary(id);
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load meeting';
        this.loading = false;
      }
    });
  }

  loadNotes(meetingId: number) {
    this.api.getNotes(meetingId).subscribe({
      next: (notes) => this.notes = notes,
      error: () => this.notes = []
    });
  }

  loadSummary(meetingId: number) {
    this.summaryLoading = true;
    this.api.getSummary(meetingId).subscribe({
      next: (summary) => {
        this.summary = summary;
        this.summaryLoading = false;
        if (summary.status !== 'ready') {
          this.startPolling(meetingId);
        }
      },
      error: () => {
        this.summary = null;
        this.summaryLoading = false;
        this.startPolling(meetingId);
      }
    });
  }

  addNote() {
    if (!this.meeting?.id || !this.newNote.text.trim()) return;
    
    this.api.addNote(this.meeting.id, this.newNote).subscribe({
      next: (note) => {
        this.notes.unshift(note);
        this.newNote = { author: '', text: '' };
        this.loadSummary(this.meeting!.id);
      },
      error: (err) => {
        this.error = 'Failed to add note';
      }
    });
  }

  generateSummary() {
    if (!this.meeting?.id) return;
    
    this.generatingSummary = true;
    this.api.generateSummary(this.meeting.id).subscribe({
      next: () => {
        this.generatingSummary = false;
        this.startPolling(this.meeting!.id);
      },
      error: () => {
        this.generatingSummary = false;
        this.error = 'Failed to generate summary';
      }
    });
  }

  private startPolling(meetingId: number) {
    interval(this.pollingInterval)
      .pipe(
        takeUntil(this.destroy$),
        switchMap(() => this.api.getSummary(meetingId))
      )
      .subscribe({
        next: (summary) => {
          this.summary = summary;
          if (summary.status === 'ready') {
            this.destroy$.next();
          }
        },
        error: () => {}
      });
  }
}
