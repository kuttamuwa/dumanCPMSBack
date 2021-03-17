import { Component, ElementRef, OnInit, ViewChild, ViewEncapsulation } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { AppService } from '../app.service';

@Component({
  selector: 'app-risk-analysis',
  templateUrl: './risk-analysis.component.html',
  styleUrls: ['./risk-analysis.component.css']
})
export class RiskAnalysisComponent {

  filePath = new FormControl('', [Validators.required]);

  @ViewChild('fileDialog') fileDialog: ElementRef;

  constructor(private appService: AppService) { }

  FileInputOnClick = () => {
    this.fileDialog.nativeElement.click();
  }

  FileDialogOnChange = (ev: Event) => {
    let fullPath = (ev.target as HTMLInputElement).value;
    let filename = fullPath.split('\\')[fullPath.split('\\').length - 1]
    if (filename.split('.')[1] == 'xls' || filename.split('.')[1] == 'xlsx') {
      this.filePath.setValue(filename);
      this.filePath.setErrors({'format': false});
    }
    else {
      this.filePath.setErrors({'format': true});
    }
  }

  getErrorMessage = () => {
    if (this.filePath.hasError('required') || this.filePath.hasError('format'))
      return 'Excel formatında dosya yükleyiniz!'
  }

  SubmitOnClick = () => {
    let file = this.fileDialog.nativeElement.files[0];
    let reader = new FileReader();
    reader.readAsDataURL(file);
    let fileBlob = new Blob([reader.result], {type: file.type});
    this.appService.postRiskDataset(fileBlob).subscribe(res => {
      console.log(res);
    });
  }

  ResetOnClick = () => {
    this.filePath.setValue('');
  }
}
