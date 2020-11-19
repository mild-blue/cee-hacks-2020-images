import { Component, OnDestroy, OnInit } from '@angular/core';
import { Role, User } from '@app/model/User';
import { AuthService } from '@app/services/auth/auth.service';
import { faCog } from '@fortawesome/free-solid-svg-icons';
import { AlertService } from '@app/services/alert/alert.service';
import { Subscription } from 'rxjs';
import { LoggerService } from '@app/services/logger/logger.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit, OnDestroy {

  public loading: boolean = false;
  public user?: User;

  constructor(private _authService: AuthService,
              private _alertService: AlertService,
              private _logger: LoggerService) {
  }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
  }
}
