var count=0;
var count1 = 1;
var position_x;
var position_y;
var d = document.getElementById("rect");
var toggle=0;
//-----------------------modal window activation---------------------//
var modal = document.getElementById('myModal');
var hold=document.getElementById("holder");
// Get the image and insert it inside the modal - use its "alt" text as a caption
var form_img = document.getElementById('upload');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
var area= document.getElementById('sub-area');
area.onclick = function(){
    modal.style.display = "block";
    modalImg.src = form_img.src;
    captionText.innerHTML = form_img.alt;
}


// Get the <span> element that closes the modal
var close = document.getElementsByClassName("close")[0];
var close1 = document.getElementsByClassName("close-btn")[0];

// When the user clicks on <span> (x), close the modal
close.onclick = function() { 
    modal.style.display = "none";
}
close1.onclick = function() { 
    toggle=0;
    document.getElementById("modal-crop-btn").style.color="black";
    modal.style.display = "none";
}

//----------------------------------modal-window-closed----------------------------//
document.getElementById("img01").addEventListener("wheel",zoomfunction());
function zoomfunction(e){

//-----------------to do zoomin and zoomout on ousewheel-------------------------
}



function zoom(zm){  //for zooming in and out with help of buttons
img=document.getElementById("img01");
wid=img.width;
ht=img.height;
var _CONTAINER_WIDTH = $("#holder").outerWidth();
var _CONTAINER_HEIGHT = $("#holder").outerHeight();
_IMAGE_WIDTH = $("#img01").width();
_IMAGE_HEIGHT = $("#img01").height();

if(wid*zm< _CONTAINER_WIDTH || ht*zm< _CONTAINER_HEIGHT ){
    return;}
    else{
img.style.width=(wid*zm)+"px";
img.style.height=(ht*zm)+"px";}
     }


//--------------for image panning--------------------------------//

        //------if users select region other than in crop area than allow image panning---------//

var _DRAGGGING_STARTED = 0;
var _LAST_MOUSEMOVE_POSITION = { x: null, y: null };
var _DIV_OFFSET = $('#holder').offset();
var _CONTAINER_WIDTH = $("#holder").outerWidth();
var _CONTAINER_HEIGHT = $("#holder").outerHeight();
var _IMAGE_WIDTH;
var _IMAGE_HEIGHT;
var _IMAGE_LOADED = 0;

// Check whether image is cached or wait for the image to load 
// This is necessary before calculating width and height of the image
if($('#img01').get(0).complete) {
  ImageLoaded();
}
else {
  $('#img01').on('load', function() {
    ImageLoaded();
  });
}

// Image is loaded
function ImageLoaded() {
  _IMAGE_WIDTH = $("#img01").width();
  _IMAGE_HEIGHT = $("#img01").height();
  _IMAGE_LOADED = 1;  
}

$('#holder').on('mousedown', function(event) {
  /* Image should be loaded before it can be dragged */
  if(toggle==0){
  if(_IMAGE_LOADED == 1) { 
    _DRAGGGING_STARTED = 1;

    /* Save mouse position */
    _LAST_MOUSE_POSITION = { x: event.pageX - _DIV_OFFSET.left, y: event.pageY - _DIV_OFFSET.top };
  }             }
   if(toggle==1){
                  d = document.getElementById("rect");
                  position_x = event.offsetX ;
                  position_y = event.offsetY ;
                  document.pointform.form1_x.value = position_x;
                  document.pointform.form1_y.value = position_y;

                  var imgage = document.getElementById("img01");

                  var d = document.getElementById("rect");
                  d.style.display = "absolute";  
                  d.style.left = position_x+'px';
                  d.style.top = position_y+'px';
                  d.style.opacity = "0.1";
                  imgage.style.opacity="0.";

              }
  
});

$('#holder').on('mouseup', function(event) {
  if (toggle==0){
  _DRAGGGING_STARTED = 0;
                }

  if (toggle==1){
                count=1;
                position_x1 = event.offsetX;
                position_y1 = event.offsetY;
                document.pointform.form2_x.value = position_x1;
                document.pointform.form2_y.value = position_y1;
                var d = document.getElementById("rect");
                d.style.width = position_x1 - position_x + 'px';
                d.style.height = position_y1 - position_y + 'px';

            }
});

$('#holder').on('mousemove', function(event) {
  if(toggle==0){
  if(_DRAGGGING_STARTED == 1) {
    var current_mouse_position = { x: event.pageX - _DIV_OFFSET.left, y: event.pageY - _DIV_OFFSET.top };
    var change_x = current_mouse_position.x - _LAST_MOUSE_POSITION.x;
    var change_y = current_mouse_position.y - _LAST_MOUSE_POSITION.y;

    /* Save mouse position */
    _LAST_MOUSE_POSITION = current_mouse_position;

    var img_top = parseInt($("#img01").css('top'), 10);
    var img_left = parseInt($("#img01").css('left'), 10);
    var img_right= parseInt($("#img01").css('right'), 10);
    var img_bottom= parseInt($("#img01").css('bottom'), 10);

    var img_top_new = img_top + change_y;
    var img_left_new = img_left + change_x;
    var img_right_new = img_right - change_x;
    var img_bottom_new = img_bottom - change_y;
    
    /* Validate top and left do not fall outside the image, otherwise white space will be seen */
    if(img_top_new > 0)
      img_top_new = 0;
     _CONTAINER_WIDTH = $("#holder").outerWidth();
     _CONTAINER_HEIGHT = $("#holder").outerHeight();
      _IMAGE_WIDTH = $("#img01").width();
      _IMAGE_HEIGHT = $("#img01").height();
    if(img_top_new < (_CONTAINER_HEIGHT - _IMAGE_HEIGHT))
      img_top_new = _CONTAINER_HEIGHT - _IMAGE_HEIGHT;

    if(img_left_new > 0)
      img_left_new = 0;

    if(img_left_new < (_CONTAINER_WIDTH - _IMAGE_WIDTH))
      img_left_new = _CONTAINER_WIDTH - _IMAGE_WIDTH;
      console.log( img_top_new + '- '+img_bottom_new);
    $("#img01").css({ top: img_top_new + 'px', left: img_left_new + 'px' });
  }
}

if (toggle==1){


            position_x2 = event.offsetX;
            position_y2 = event.offsetY;
            document.pointform.form3_x.value = position_x2;
            document.pointform.form3_y.value = position_y2;
            if(count==0){
            var d = document.getElementById("rect");
            // // d.style.position = "absolut
            d.style.opacity = "0.1";

            
            d.style.width = position_x2 - position_x + 'px';
            d.style.height = position_y2 - position_y + 'px';
                        }

              }

    });


function cropbox(){
toggle=1;
document.getElementById("modal-crop-btn").style.color="blue";

}
//----------------------------------------for cropbox events--------------------------------------------//

