import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

@Injectable({
    providedIn: 'root'
})
export class GlobalService {
    constructor(private http: HttpClient) {

    }

    getImageBlob() {
        return this.http.get("http://localhost:8080", {responseType: 'blob'});
    }
}
