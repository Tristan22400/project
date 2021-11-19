import {Injectable} from '@angular/core';
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import { throwError } from 'rxjs';
import {catchError} from 'rxjs/operators';
import {API_URL} from '../env';
import {Auth} from './auth.model';

@Injectable()
export class AuthApiService
{
    constructor(private http: HttpClient)
    {}

    private static handleError(err: HttpErrorResponse | any)
    {
        return throwError(err.message || 'Error: Unable to complete request.');
    }

    login(auth: Auth): Observable<any>
    {
        return this.http
            .post(`${API_URL}/login`, auth)
            .pipe(catchError(AuthApiService.handleError));
    }

    register(auth: Auth): Observable<any>
    {
        return this.http
            .post(`${API_URL}/register`, auth)
            .pipe(catchError(AuthApiService.handleError));
    }


}
