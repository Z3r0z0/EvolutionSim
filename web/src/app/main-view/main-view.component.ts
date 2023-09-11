import { Component, OnInit } from '@angular/core';
import { GlobalService } from '../services/globalservice';

@Component({
  selector: 'app-main-view',
  templateUrl: './main-view.component.html',
  styleUrls: ['./main-view.component.css']
})
export class MainViewComponent implements OnInit {

  constructor(private globalService : GlobalService) { }

  image : any;

  ngOnInit() {
  }

  action(call : string){
      this.globalService.getImageBlob(call).subscribe(res => {
        let reader = new FileReader();
        reader.addEventListener("load", () => {
          this.image = reader.result;
        });

      if(res){
        reader.readAsDataURL(res);
      }
    })
  }

}
