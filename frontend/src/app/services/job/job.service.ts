import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';
import { map } from 'rxjs/operators';
import { AuthResponse } from '@app/services/auth/auth.interface';
import * as jwt_decode from 'jwt-decode';
import { DecodedToken, User } from '@app/model/User';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  constructor(private _http: HttpClient) {
  }

  public initJob(file: File): Observable<unknown> {
    const uploadData = new FormData();
    uploadData.append('file', file, file.name);

    return this._http.post<unknown>(
      `${environment.apiUrl}/job/POST`,
      uploadData,
      {
        reportProgress: true,
        observe: 'events'
      });
  }

  public getJobStatus(jobId: number): Observable<unknown> {
    return this._http.get<unknown>(
      `${environment.apiUrl}`
    ).pipe(
      map((r: unknown) => {
        console.log(r);
      })
    );
  }
}
