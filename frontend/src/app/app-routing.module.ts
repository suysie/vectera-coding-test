import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { MeetingsListComponent } from './meetings-list/meetings-list.component';
import { MeetingDetailComponent } from './meeting-detail/meeting-detail.component';

const routes: Routes = [
  { path: '', redirectTo: '/meetings', pathMatch: 'full' },
  { path: 'meetings', component: MeetingsListComponent },
  { path: 'meetings/:id', component: MeetingDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
