import {Component} from '@angular/core';
import {AuthApiService} from './auth-api.service';
import {Router} from "@angular/router";


@Component({
    selector: 'login-form',
    template: `
<mat-card>
<h2>Login</h2>
<mat-form-field class="full-width">
<input matInput
placeholder="login"
(keyup)="updateLogin($event)">
</mat-form-field>

<mat-form-field class="full-width">
<input type="password" matInput
placeholder="password"
(keyup)="updatePassword($event)">
</mat-form-field>

<button mat-raised-button
color="primary"
(click)="login()">
Sign In
</button>
</mat-card>
`,
    styles: [`
.login-form {
min-width: 150px;
max-width: 500px;
width: 100%;
}

.full-width {
width: 100%;
}
`]
})


export class LoginComponent {
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

    login()
    {
        this.authApi
            .login(this.authentication)
            .subscribe(
                () => this.router.navigate(['/']),
                error => alert(error.message)
            );

        sessionStorage.setItem('login', this.authentication.login);
    }
}
