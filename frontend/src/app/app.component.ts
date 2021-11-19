import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {catchError} from 'rxjs/operators';
import {API_URL} from './env';

@Component({
  selector: 'app-root',
  template: `
    <mat-toolbar color="primary" class="mat-elevation-z10">
      <button mat-button routerLink="/">Online Exams</button>
      <button mat-button routerLink="/about"> About</button>

      <!-- This fills the remaining space of the current row -->
      <span class="fill-remaining-space"></span>

      <button mat-button routerLink="login" *ngIf="!authenticated">Sign In</button>
      <button mat-button routerLink="register" *ngIf="!authenticated">Sign Up</button>
      <button mat-button (click)="signOut()" *ngIf="authenticated">Sign Out</button>
    </mat-toolbar>

<div style="text-align:center">

<div class="view-container">
    <router-outlet></router-outlet>
</div>
  `,
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
    constructor(private http: HttpClient) {}

    private static _handleError(err: HttpErrorResponse | any)
    {
        return Observable.throw(err.message || 'Error: Unable to complete request.');
    }

    authenticated = false;

    signOut = false;

    about()
    {
        return this.http
            .get(`${API_URL}/about`)
            .pipe(catchError(AppComponent._handleError));
    }

    ngOnInit()
    {
        const self = this;
    }
}
