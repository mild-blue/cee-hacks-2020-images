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

  constructor(private _jobService: JobService) {
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
  }

  handleFileInput(target: EventTarget | null) {
    if (!target) {
      return;
    }
    // @ts-ignore
    const files: FileList = target.files;
    this._file = files.item(0);
    console.log(this._file);
  }

  public uploadFile(): void {
    if (!this._file) {
      return;
    }
    this._jobService.initJob(this._file).subscribe((data: unknown) => {
      console.log('Upload returned:', data);
    });
    this._jobService.getJobStatus(1);
  }
}
