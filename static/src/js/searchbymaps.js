      var map;
      var markers = [];
      var infoWindow;
      var radius = 20;

        function initMap() {
            console.log("Initting...")
          var bkk = {lat: 13.72706590782156, lng: -259.4317136730957};
          map = new google.maps.Map(document.getElementById('map'), {
            center: bkk,
            zoom: 11,
            mapTypeId: 'roadmap',
            mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU}
          });
          google.maps.event.addListener(map, "dragend", function() {
                var center = this.getCenter();
                var latitude = center.lat();
                var longitude = center.lng();
                console.log("current latitude is: " + latitude);
                console.log("current longitude is: " + longitude);
                searchLocationsNear(latitude, longitude)
            });
            google.maps.event.addListener(map, 'zoom_changed', function() {
                var zoom = this.getZoom();
                if(zoom >= 15) {
                    radius = 10
                } else if (zoom < 15 && zoom >=  13) {
                    radius = 20
                } else {
                    radius = 50
                }
                console.log(zoom);
                console.log(radius)
            });
          infoWindow = new google.maps.InfoWindow();
          google.maps.event.addListener(infoWindow,'closeclick',function(){
            var center = map.getCenter();
            var latitude = center.lat();
            var longitude = center.lng();
            searchLocationsNear(latitude, longitude)
         });

          searchLocationsNear(bkk.lat, bkk.lng)
        }

       function clearLocations() {
         infoWindow.close();
         for (var i = 0; i < markers.length; i++) {
           markers[i].setMap(null);
         }
         markers.length = 0;
       }

       function clearAssetsDiv() {
        document.getElementById('assets_list').innerHTML = "";
       }

       function searchLocationsNear(lat, lng) {
         clearLocations();
         clearAssetsDiv();

         var searchUrl = '/api/searchmaps?clat=' + lat + '&clng=' + lng + '&radius=' + radius;
         downloadUrl(searchUrl, function(data) {
           var xml = parseXml(data);
           var markerNodes = xml.documentElement.getElementsByTagName("marker");
           for (var i = 0; i < markerNodes.length; i++) {
             var id = markerNodes[i].getAttribute("id");
             var asset_code = markerNodes[i].getAttribute("asset_code");
             var asset_type = markerNodes[i].getAttribute("asset_type");
             var asset_address = markerNodes[i].getAttribute("asset_address");
             var asset_img = markerNodes[i].getAttribute("asset_img");
             var asset_area = markerNodes[i].getAttribute("asset_area");
             var latlng = new google.maps.LatLng(
                  parseFloat(markerNodes[i].getAttribute("lat")),
                  parseFloat(markerNodes[i].getAttribute("lng")));

             createMarker(id, latlng, asset_code, asset_type, asset_address, asset_area, asset_img);
             createListDiv(id, latlng, asset_code, asset_type, asset_address, asset_area, asset_img);
           }
           //map.fitBounds(bounds);
         });
       }

       function createListDiv(id, latlng, asset_code, asset_type, asset_address, asset_area, asset_img) {
         let content = `<div class="col-12 my-3" id="${asset_code}">
         <div class="card flex-row flex-wrap assets-item">
             <div class="border-0">
                 <img class="card-img-top assets-img" src="data:image/jpeg;base64, ${asset_img}" />
             </div>
             <div class="col p-0">
                 <div class="row p-4">
                     <div class="col">
                         <h4 class="card-title"><span class="badge badge-secondary">รหัสทรัพย์สิน</span> ${asset_code}</h4>
                         <p class="card-text"><span class="badge badge-secondary">ประเภททรัพย์สิน</span> ${asset_type}</p>
                         <p class="card-text"><span class="badge badge-secondary">ที่อยู่</span> ${asset_address}</p>
                         <p class="card-text"><span class="badge badge-secondary">เนื้อที่</span> ${asset_area}</p>
                     </div>
                 </div>
                 <div class="row price-row">
                     <div class="col price-col">
                         <a href="/assets/${id}" class="btn btn-primary btn-lg btn-block" style="border-radius: 0rem !important; color:white;">รายละเอียดเพิ่มเติม</a>
                     </div>
                 </div>
             </div>
         </div>
     </div>`
        document.getElementById('assets_list').innerHTML += content;
       }

       function showOnlyMe(asset_code) {
         allLists = document.getElementById("assets_list")
         membersList = allLists.querySelectorAll('[id]')
         var i;
         for(i = 0; i < membersList.length; i++) {
           element = membersList[i];
           console.log(element.id)
           if(element.id != asset_code) {
             console.log("removing..." + element.id)
             document.getElementById(element.id).remove();
             continue;
           }
         }
       }

       function createMarker(id, latlng, asset_code, asset_type, asset_address, asset_area, asset_img) {
          var html = `<img src="data:image/jpeg;base64, ${asset_img}" style="max-height:150px;"/><br/>
          <a href="/assets/${id}"><b>${asset_code}</b></a></br>
          <b>ประเภท : ${asset_type}</b><br/>
          <b>เนื้อที่ : ${asset_area}</b><br/>
          <b>ที่อยู่ : ${asset_address}</b></br>`;
          var marker = new google.maps.Marker({
            map: map,
            position: latlng,
            asset_code: asset_code
          });
          google.maps.event.addListener(marker, 'click', function() {
            infoWindow.setContent(html);
            infoWindow.open(map, marker);
            showOnlyMe(asset_code);
          });
          markers.push(marker);
        }

       function downloadUrl(url, callback) {
          var request = window.ActiveXObject ?
              new ActiveXObject('Microsoft.XMLHTTP') :
              new XMLHttpRequest;

          request.onreadystatechange = function() {
            if (request.readyState == 4) {
              request.onreadystatechange = doNothing;
              callback(request.responseText, request.status);
            }
          };

          request.open('GET', url, true);
          request.send(null);
       }

       function parseXml(str) {
          if (window.ActiveXObject) {
            var doc = new ActiveXObject('Microsoft.XMLDOM');
            doc.loadXML(str);
            return doc;
          } else if (window.DOMParser) {
            return (new DOMParser).parseFromString(str, 'text/xml');
          }
       }

       function doNothing() {}