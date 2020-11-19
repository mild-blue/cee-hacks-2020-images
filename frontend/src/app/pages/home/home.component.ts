import { Component, OnDestroy, OnInit } from '@angular/core';
import { Role, User } from '@app/model/User';
import { AuthService } from '@app/services/auth/auth.service';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { AlertService } from '@app/services/alert/alert.service';
import { Subscription } from 'rxjs';
import { LoggerService } from '@app/services/logger/logger.service';
import { JobService } from '@app/services/job/job.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  // eslint-disable-next-line no-null/no-null
  private _file: File | null = null;
  private _jobId: string | null = null;

  constructor(private _jobService: JobService) {
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
  }

  handleFileInput(target: EventTarget | null) {
    if (!target) {
      console.log("File event target is null.")
      return;
    }
    // @ts-ignore
    const files: FileList = target.files;
    this._file = files.item(0);
    console.log(this._file);
  }

  handleJobIdInput(target: EventTarget | null) {
    console.log("!!!.")
    if (!target) {
      console.log("JobId event target is null.")
      return;
    }
    // @ts-ignore
    this._jobId = target.value
    console.log(this._jobId);
  }

  public createJob(): void {
    if (!this._file) {
      console.log("File is null.")
      return;
    }
    this._jobService.createJob(this._file).subscribe((data: unknown) => {
      console.log('Upload returned:', data);
    });
  }

  public getJobStatus(): void {
    if (!this._jobId) {
      console.log("JobId is null.")
      return;
    }
    this._jobService.getJobStatus(this._jobId).subscribe((data: unknown) => {
      console.log('Job status returned:', data);
    });
  }
}

// 75d7d972-00b0-4aaa-90b2-d5173ea68b97
