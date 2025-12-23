import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';
import { Meeting } from '../models';

@Component({
  selector: 'app-meetings-list',
  templateUrl: './meetings-list.component.html',
  styleUrls: ['./meetings-list.component.css']
})
export class MeetingsListComponent implements OnInit {
  meetings: Meeting[] = [];
  loading = true;
  error: string | null = null;

  constructor(private api: ApiService, private router: Router) {}

  ngOnInit() {
    console.log('MeetingsList: Loading...');
    this.loadMeetings();
  }

  loadMeetings() {
    this.loading = true;
    this.error = null;
    this.api.getMeetings().subscribe({
      next: (response) => {
        console.log('MeetingsList: API response:', response);
        this.meetings = response.results || [];
        this.loading = false;
        console.log('MeetingsList: Loaded', this.meetings.length, 'meetings');
      },
      error: (err) => {
        console.error('MeetingsList: API error:', err);
        this.error = 'Failed to load meetings: ' + err.message;
        this.loading = false;
      }
    });
  }

  createDemo() {
    this.api.createMeeting({ title: 'Demo Meeting', started_at: new Date().toISOString() }).subscribe({
      next: (meeting) => {
        this.router.navigate(['/meetings', meeting.id]);
      },
      error: (err) => {
        console.error('Create demo failed:', err);
        this.error = 'Failed to create demo';
      }
    });
  }
}
