import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VeiculoPage } from './home.page';

describe('VeiculoPage', () => {
  let component: VeiculoPage;
  let fixture: ComponentFixture<VeiculoPage>;

  beforeEach(async () => {
    fixture = TestBed.createComponent(VeiculoPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
