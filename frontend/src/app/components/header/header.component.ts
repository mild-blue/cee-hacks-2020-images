import { Component, EventEmitter, Input, Output } from '@angular/core';
import { User } from '@app/model/User';
import { faQuestionCircle, faUserAlt } from '@fortawesome/free-solid-svg-icons';
import { AuthService } from '@app/services/auth/auth.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent {

  @Input() user?: User;
  @Output() downloadAction: EventEmitter<void> = new EventEmitter<void>();

  constructor(private _authService: AuthService) {
  }

  public logOut(): void {
    this._authService.logout();
  }
}
