import {NoopAnimationsModule} from '@angular/platform-browser/animations';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatInputModule} from '@angular/material/input';

import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {HttpClientModule} from '@angular/common/http';
import {RouterModule, Routes} from '@angular/router';

import {AppComponent} from './app.component';
import {ExamsApiService} from './exams/exams-api.service';
import {ExamFormComponent} from './exams/exam-form.component';
import {ExamsComponent} from './exams/exams.component';
import {AboutComponent} from './about.component';

const appRoutes: Routes = [
    { path: 'new-exam', component: ExamFormComponent },
    { path: 'about', component: AboutComponent },
    { path: '', component: ExamsComponent },
];


@NgModule({
  declarations: [
      AppComponent,
      ExamFormComponent,
      ExamsComponent,
      AboutComponent,
  ],
  imports: [
      BrowserModule,
      HttpClientModule,
      RouterModule.forRoot(appRoutes,),
      NoopAnimationsModule,
      MatToolbarModule,
      MatButtonModule,
      MatCardModule,
      MatInputModule,
  ],
    providers: [ExamsApiService],
    bootstrap: [AppComponent]
})
export class AppModule { }
