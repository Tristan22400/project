import {Component} from '@angular/core';
import {AuthApiService} from './auth-api.service';
import {Router} from "@angular/router";


@Component({
    selector: 'register-form',
    template: `
<mat-card>
<h2>Register</h2>
<mat-form-field class="full-width">
<input matInput
placeholder="login"
(keyup)="updateLogin($event)">
</mat-form-field>

<mat-form-field class="full-width">
<input matInput
placeholder="password"
(keyup)="updatePassword($event)">
</mat-form-field>

<button mat-raised-button
color="primary"
(click)="register()">
Sign Up
</button>
</mat-card>
`,
    styles: [`
.register-form {
min-width: 150px;
max-width: 500px;
width: 100%;
}

.full-width {
width: 100%;
}
`]
})


export class RegisterComponent {
    authentication = {
        login: '',
        password: ''
    };

    constructor(private authApi: AuthApiService, private router: Router)
    {}

    updateLogin(event: any)
    {
        this.authentication.login = event.target.value;
    }

    updatePassword(event: any)
    {
        this.authentication.password = event.target.value;
    }

    register()
    {
        this.authApi
            .register(this.authentication)
            .subscribe(
                () => this.router.navigate(['/login']),
                error => alert(error.message)
            );
    }
}
