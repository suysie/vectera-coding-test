import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { AppRoutingModule } from './app-routing.module';

import { AppComponent } from './app.component';
import { MeetingsListComponent } from './meetings-list/meetings-list.component';
import { MeetingDetailComponent } from './meeting-detail/meeting-detail.component';
import { ApiService } from './api.service';

@NgModule({
  declarations: [
    AppComponent,
    MeetingsListComponent,
    MeetingDetailComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule.forRoot([]),
    AppRoutingModule
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
