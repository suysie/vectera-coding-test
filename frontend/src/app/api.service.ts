import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Meeting, Note, Summary } from './models';

interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = '/api';

  constructor(private http: HttpClient) {}

  getMeetings(): Observable<PaginatedResponse<Meeting>> {
    return this.http.get<PaginatedResponse<Meeting>>(`${this.baseUrl}/meetings/`);
  }

  getMeeting(id: number): Observable<Meeting> {
    return this.http.get<Meeting>(`${this.baseUrl}/meetings/${id}/`);
  }

  createMeeting(meeting: Partial<Meeting>): Observable<Meeting> {
    return this.http.post<Meeting>(`${this.baseUrl}/meetings/`, meeting);
  }

  addNote(meetingId: number, note: Partial<Note>): Observable<Note> {
    return this.http.post<Note>(`${this.baseUrl}/meetings/${meetingId}/notes/`, note);
  }

  getNotes(meetingId: number): Observable<Note[]> {
    return this.http.get<Note[]>(`${this.baseUrl}/meetings/${meetingId}/notes-list/`);  // ← FIXED!
  }

  generateSummary(meetingId: number): Observable<Summary> {
    return this.http.post<Summary>(`${this.baseUrl}/meetings/${meetingId}/summarize/`, {});
  }

  getSummary(meetingId: number): Observable<Summary> {
    return this.http.get<Summary>(`${this.baseUrl}/meetings/${meetingId}/summary/`);
  }
}
