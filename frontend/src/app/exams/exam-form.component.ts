import {Component} from '@angular/core';
import {ExamsApiService} from "./exams-api.service";
import {Router} from "@angular/router";


@Component({
  selector: 'exam-form',
  template: `
    <mat-card>
      <h2>New Exam</h2>
        <mat-form-field class="full-width">
          <input matInput
                 placeholder="Title"
                 (keyup)="updateTitle($event)">
        </mat-form-field>

        <mat-form-field class="full-width">
          <input matInput
                 placeholder="Description"
                 (keyup)="updateDescription($event)">
        </mat-form-field>

        <button mat-raised-button
                color="primary"
                (click)="saveExam()">
          Save Exam
        </button>
    </mat-card>
  `,
  styles: [`
    .exams-form {
      min-width: 150px;
      max-width: 500px;
      width: 100%;
    }

    .full-width {
      width: 100%;
    }
  `]
})


export class ExamFormComponent {
    exam = {
        title: '',
        description: '',
    };

    constructor(private examsApi: ExamsApiService, private router: Router)
    {}

    updateTitle(event: any)
    {
        this.exam.title = event.target.value;
    }

    updateDescription(event: any)
    {
        this.exam.description = event.target.value;
    }

    saveExam()
    {
        this.examsApi
            .saveExam(this.exam)
            .subscribe(
                () => this.router.navigate(['/']),
                error => alert(error.message)
            );
    }
}
