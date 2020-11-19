import {Injectable} from '@angular/core';
import {environment} from '@environments/environment';
import {map} from 'rxjs/operators';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class JobService {

  constructor(private _http: HttpClient) {
  }

  public createJob(file: File): Observable<unknown> {
    const uploadData = new FormData();
    uploadData.append('file', file, file.name);
    uploadData.append('metadata', JSON.stringify({key: 'value'}))

    return this._http.post<unknown>(
      `${environment.apiUrl}/job`,
      uploadData,
      {
        reportProgress: true,
        observe: 'events'
      });
  }

  public getJobStatus(jobId: string): Observable<unknown> {
    return this._http.get<unknown>(
      `${environment.apiUrl}/job/status/${jobId}`
    ).pipe(
      map((r: unknown) => {
        console.log(r);
        return r;
      })
    );
  }
}
