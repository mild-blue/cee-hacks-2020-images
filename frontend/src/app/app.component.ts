import { Component, OnDestroy } from '@angular/core';
import { AuthService } from '@app/services/auth/auth.service';
import { Subscription } from 'rxjs';
import { LoggerService } from '@app/services/logger/logger.service';
import { User } from '@app/model/User';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnDestroy {

  private _userSubscription?: Subscription;
  public user?: User;

  constructor(private _authService: AuthService,
              private _logger: LoggerService,
              private _router: Router) {
    this._userSubscription = this._authService.currentUser.subscribe(user => {
      this.user = user;
      if (user) {
        this._logger.log('Logged in with user', [user]);
      } else {
        this._logger.log('Logged out');
      }
    });
  }

  ngOnDestroy() {
    this._userSubscription?.unsubscribe();
  }
}
